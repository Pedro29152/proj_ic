from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequestKeyError
from os import getenv

from biblioteca.db import DB_CTX
from biblioteca import mailer, response_messages
from biblioteca.usuarios.usuario_dao import UsuarioDAO
from biblioteca.projeto.projetos_dao import ProjetosDAO
from biblioteca.orientador.orientadores_dao import OrientadoresDAO
from biblioteca.curso.cursos_dao import CursosDAO
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
    get_request_form_data_attributes,
    get_enum_obj
)

class AllCountsResource(Resource):
    @token_required
    def get(self, user_info):
        usuarioDao = UsuarioDAO(DB_CTX)
        projetosDao = ProjetosDAO(DB_CTX)
        orientadoresDao = OrientadoresDAO(DB_CTX)
        cursosDao = CursosDAO(DB_CTX)

        if (user_info['tipoUsuario'] == TiposUsuario.Aluno.value):
            return get_unauthorized(response_messages.SEM_AUTORIZACAO())
        if (user_info['tipoUsuario'] == TiposUsuario.Professor.value):
            orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

            usuarios_count = usuarioDao.get_count(codOrientador=orientador['codOrientador'])
            projetos_count = projetosDao.get_count(codOrientador=orientador['codOrientador'])
            cursos_count = cursosDao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'cursosCount': cursos_count,
            })
        if (user_info['tipoUsuario'] == TiposUsuario.Secretaria.value):
            usuarios_count = usuarioDao.get_count()
            projetos_count = projetosDao.get_count()
            orientadores_count = orientadoresDao.get_count()
            cursos_count = cursosDao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'orientadoresCount': orientadores_count,
                'cursosCount': cursos_count,
            })
        if (user_info['tipoUsuario'] == TiposUsuario.Coordenador.value):
            return "WIP"
        if (user_info['tipoUsuario'] == TiposUsuario.Administrador.value):
            usuarios_count = usuarioDao.get_count()
            projetos_count = projetosDao.get_count()
            orientadores_count = orientadoresDao.get_count()
            cursos_count = cursosDao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'orientadoresCount': orientadores_count,
                'cursosCount': cursos_count,
            })

class ContatoResource(Resource):
    def post(self):
        try:
            attr = get_request_form_data_attributes(['email', 'nome', 'assunto', 'mensagem'])
        except Exception as ex:
            return get_erro(ex.__str__()), 400

        if not (attr['email'] and attr['nome'] and attr['assunto'] and attr['mensagem']):
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"email", "nome", "mensagem" e "assunto"'))
        if not is_valid_email(attr['email']):
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
            '''.format(attr['email'], attr['nome'], attr['assunto'], attr['mensagem']))
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
