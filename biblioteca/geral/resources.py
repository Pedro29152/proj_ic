from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequestKeyError
from os import getenv

from biblioteca import mailer
from biblioteca.usuarios import usuario_dao
from biblioteca.projeto import projetos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.curso import cursos_dao
from biblioteca.responses import (
    get_data,
    get_unauthorized,
    get_bad_request,
    get_erro,
    get_success
)
from biblioteca.extensions import (
    token_required,
    TiposUsuario,
    is_valid_email
)

class AllCountsResource(Resource):
    @token_required
    def get(self, user_info):
        if (user_info['tipoUsuario'] == TiposUsuario.Aluno.value):
            return get_unauthorized('Seu nível de acesso não lhe permite essa ação')
        if (user_info['tipoUsuario'] == TiposUsuario.Professor.value):
            orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request('O usuário utilizado não possui um orientador ligado a ele')

            usuarios_count = usuario_dao.get_count(codOrientador=orientador['codOrientador'])
            projetos_count = projetos_dao.get_count(codOrientador=orientador['codOrientador'])
            cursos_count = cursos_dao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'cursosCount': cursos_count,
            })
        if (user_info['tipoUsuario'] == TiposUsuario.Secretaria.value):
            usuarios_count = usuario_dao.get_count()
            projetos_count = projetos_dao.get_count()
            orientadores_count = orientadores_dao.get_count()
            cursos_count = cursos_dao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'orientadoresCount': orientadores_count,
                'cursosCount': cursos_count,
            })
        if (user_info['tipoUsuario'] == TiposUsuario.Coordenador.value):
            return "WIP"
        if (user_info['tipoUsuario'] == TiposUsuario.Administrador.value):
            usuarios_count = usuario_dao.get_count()
            projetos_count = projetos_dao.get_count()
            orientadores_count = orientadores_dao.get_count()
            cursos_count = cursos_dao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'orientadoresCount': orientadores_count,
                'cursosCount': cursos_count,
            })

class ContatoResource(Resource):
    def post(self):
        try:
            email = request.form['email']
            nome = request.form['nome']
            assunto = request.form['assunto']
            mensagem = request.form['mensagem']
        except BadRequestKeyError:
            return get_bad_request('A requsição deve ter os campos "email", "nome", "mensagem" e "assunto" em seu corpo.')

        if not (email and nome and assunto and mensagem):
            return get_bad_request('Os campos enviados devem ser preenchidos')
        if not is_valid_email(email):
            return get_bad_request('O campo email deve ser um e-mail válido')

        CONTACT_MAIL = getenv('CONTACT_EMAIL')

        msg = mailer.generate_message_html(
            'Contato BTA', 
            CONTACT_MAIL, 
            '''
            <html>
                <head></head>
                <body>
                    <h3>Email: {0}</h3>
                    <h3>Nome: {1}</h3>

                    <p>{2}</p>

                    <p>{3}</p>

                    <p>Sistema de Contato BTA</p>
                </body>
            </html>
            '''.format(email, nome, assunto, mensagem))
        mailer.send_email(CONTACT_MAIL, msg)

        return get_success('Email enviado com sucesso')
