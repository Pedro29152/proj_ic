from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequestKeyError
from os import getenv
from biblioteca import mailer, response_messages
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
    TiposUsuario,
    TiposOrientador,
    StatusProjeto,
    LinguagemProjeto,
    ModalidadeProjeto,
    token_required,
    TiposUsuario,
    is_valid_email,
    get_enum_obj
)

class AllCountsResource(Resource):
    @token_required
    def get(self, user_info):
        if (user_info['tipoUsuario'] == TiposUsuario.Aluno.value):
            return get_unauthorized(response_messages.SEM_AUTORIZACAO())
        if (user_info['tipoUsuario'] == TiposUsuario.Professor.value):
            orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

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
            return get_bad_request(response_messages.CAMPOS_OBRIGATORIOS('"email", "nome", "mensagem" e "assunto"'))

        if not (email and nome and assunto and mensagem):
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"email", "nome", "mensagem" e "assunto"'))
        if not is_valid_email(email):
            return get_bad_request(response_messages.VALIDACAO_DEVE('email', 'ser um e-mail válido'))

        CONTACT_MAIL = getenv('CONTACT_EMAIL')

        msg = mailer.generate_message_html(
            'Contato BTA', 
            CONTACT_MAIL, 
            '''
                <h3>Email: {0}</h3>
                <h3>Nome: {1}</h3>

                <p>{2}</p>

                <p>{3}</p>
            '''.format(email, nome, assunto, mensagem))
        mailer.send_email(CONTACT_MAIL, msg)

        return get_success(response_messages.EMAIL_ENVIADO())

class GetTiposUsuarioEnumResource(Resource):
    @token_required
    def get(self, user_info):
        separate = True
        if not request.args.get('separate') == None:
            separate = False if request.args.get('separate') == 'false' else True

        ret = get_enum_obj(TiposUsuario, separate=separate)
        return get_success(ret)
class GetTiposOrientadorEnumResource(Resource):
    def get(self):
        separate = True
        if not request.args.get('separate') == None:
            separate = False if request.args.get('separate') == 'false' else True

        ret = get_enum_obj(TiposOrientador, separate=separate)
        return get_success(ret)
class GetStatusProjetoEnumResource(Resource):
    @token_required
    def get(self, user_info):
        separate = True
        if not request.args.get('separate') == None:
            separate = False if request.args.get('separate') == 'false' else True
        
        ret = get_enum_obj(StatusProjeto, separate=separate)
        return get_success(ret)
class GetLinguagemProjetoEnumResource(Resource):
    def get(self):
        separate = True
        if not request.args.get('separate') == None:
            separate = False if request.args.get('separate') == 'false' else True
        
        ret = get_enum_obj(LinguagemProjeto, separate=separate)
        return get_success(ret)

class GetModalidadeProjetoEnumResource(Resource):
    def get(self):
        separate = True
        if not request.args.get('separate') == None:
            separate = False if request.args.get('separate') == 'false' else True
        
        ret = get_enum_obj(ModalidadeProjeto, separate=separate)
        return get_success(ret)
