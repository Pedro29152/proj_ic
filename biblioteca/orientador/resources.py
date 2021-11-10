from smtplib import SMTPAuthenticationError
from flask import request, jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError, IntegrityError

from .schemas import Orientadores
from .orientadores_dao import OrientadoresDAO
from biblioteca.db import get_db
from biblioteca import mailer, response_messages
from biblioteca.usuarios.usuario_orientado_dao import UsuarioOrientadoDAO
from biblioteca.projeto.projetos_dao import ProjetosDAO
from biblioteca.usuarios.usuario_dao import UsuarioDAO
from biblioteca.responses import (
    get_erro,
    get_ok,
    get_data,
    get_falha,
    get_count,
    get_response_code,
    get_no_content,
    get_not_found
)
from biblioteca.extensions import(
    admin_token_required,
    secretaria_token_required,
    professor_token_required,
    professor_admin_token_required,
    aluno_token_required,
    secretaria_aluno_token_required,
    token_required,
    is_valid_email,
    is_valid_http_link,
    get_request_form_data_attributes,
    TiposUsuario
)

class OrientadorResource(Resource):
    @admin_token_required
    def post(self):
        res, cod = cadastro_orientador()
        return get_response_code(res, cod)

    @token_required
    def get(self, user_info):
        res, cod = busca_orientadores()
        return get_response_code(res, cod)

class TodosOrientadoresResource(Resource):
    @secretaria_token_required
    def get(self):
        res, cod = busca_todos_orientadores()
        return get_response_code(res, cod)

class OrientadorIdResource(Resource):
    def get(self, id):
        res, cod = get_orientador(id)
        return get_response_code(res, cod)

    @professor_admin_token_required
    def put(self, id):
        res, cod = edita_orientador(id)
        return get_response_code(res, cod)

class AtivaOrientadorResource(Resource):
    @admin_token_required
    def post(self, id):
        res, cod = ativa_orientador(id)
        return get_response_code(res, cod)

class DesativaOrientadorResource(Resource):
    @admin_token_required
    def delete(self, id):
        res, cod = desativa_orientador(id)
        return get_response_code(res, cod)

class CountOrientadoresResource(Resource):
    @secretaria_token_required
    def get(self):
        db = get_db()
        orientadoresDao = OrientadoresDAO(db)

        count = orientadoresDao.get_count()
        return get_count(count)

class SolicitarRevisaoResource(Resource):
    @professor_token_required
    def post(self, id, user_info):
        data, cod = solicitar_revisao(id, user_info)
        return get_response_code(data, cod)

class VerificarRevisoesResource(Resource):
    @aluno_token_required
    def get(self, user_info):
        ret, cod = verificar_revisoes(user_info)
        return get_response_code(ret, cod)

class BuscarRevisoesResource(Resource):
    @secretaria_token_required
    def get(self):
        db = get_db()
        orientadoresDao = OrientadoresDAO(db)
            
        ret = orientadoresDao.buscar_revisoes()
        if ret:
            return get_response_code(ret, 200)
        return get_no_content()

class GetRevisaoResource(Resource):
    @secretaria_aluno_token_required
    def get(self, id, user_info):
        db = get_db()
        orientadoresDao = OrientadoresDAO(db)
            
        if user_info['tipoUsuario'] == TiposUsuario.Aluno.value:
            ret = orientadoresDao.get_revisao_codUsuario_autor(id, user_info['codUsuario'])    
        else:
            ret = orientadoresDao.get_revisao(id)
        
        if ret:
            return get_response_code(ret, 200)
        return get_not_found(response_messages.NAO_ENCONTRADO('Revisão'))

def cadastro_orientador():
    try:
        attr = get_request_form_data_attributes(['nomeOrientador', 'raOrientador', 'email', 'linkCurrLattes'])

        orientadores = Orientadores(
            nomeOrientador=attr['nomeOrientador'],
            raOrientador=attr['raOrientador'],
            email=attr['email'],
            currLattes=attr['linkCurrLattes'],
            db=get_db()
        )
        
        orientadores.grava_orientador()

        return get_ok(response_messages.ENTIDADE_GRAVADA('Orientador')), 201
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"')), 400
    except Exception as ex:
        return get_erro(ex.__str__()), 400

def edita_orientador(codOrientador):
    db = get_db()
    orientadoresDao = OrientadoresDAO(db)
        
    ori = orientadoresDao.get_orientador_codigo(codOrientador)
    if not ori:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404

    try:
        attr = get_request_form_data_attributes(['nomeOrientador', 'raOrientador', 'email', 'linkCurrLattes'])
        
        if attr['nomeOrientador']:
            ori.nomeOrientador = attr['nomeOrientador']
        if attr['raOrientador']:
            ori.raOrientador = attr['raOrientador']
        if attr['email']:
            if not is_valid_email(attr['email']):
                raise AttributeError(response_messages.VALIDACAO_DEVE('email', 'ser um email valido'))
            ori.email = attr['email']
        if attr['linkCurrLattes']:
            if not is_valid_http_link(attr['linkCurrLattes']):
                raise AttributeError(response_messages.VALIDACAO_DEVE('currLattes', 'ser um link http/https valido'))
            ori.currLattes = attr['linkCurrLattes']

        ori.edita_orientador()

        return get_ok(response_messages.ENTIDADE_EDITADA('Orientador')), 200

    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"')), 400
    except IntegrityError:
        return get_erro(response_messages.ERRO_INTEGRIDADE('Email ou raAutor')), 400
    except DataError:
        return get_erro(response_messages.VALIDACAO_DEVE('raOrientador', 'ter no maximo 5 caracteres e seu nome no maximo 200')), 400
    except Exception as ex:
        return get_erro(ex.__str__()), 400

def get_orientador(codOrientador):
    db = get_db()
    orientadoresDao = OrientadoresDAO(db)
        
    ori = orientadoresDao.get_orientador_codigo(codOrientador, False)
    if not ori:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404
    return ori, 200

def busca_orientadores():
    db = get_db()
    orientadoresDao = OrientadoresDAO(db)
        
    query = request.args.get('nomeOrientador')

    if query:
        ret = orientadoresDao.busca_orientadores_nome(query)
    else:
        ret = orientadoresDao.busca_orientadores()
    
    if ret:
        return get_data(ret), 200
    else:
        return None, 204

def busca_todos_orientadores():
    db = get_db()
    orientadoresDao = OrientadoresDAO(db)
        
    query = request.args.get('nomeOrientador')

    if query:
        ret = orientadoresDao.busca_todos_orientadores_nome(query)
    else:
        ret = orientadoresDao.busca_todos_orientadores()
    
    if ret:
        return get_data(ret), 200
    else:
        return None, 204

def ativa_orientador(id):
    db = get_db()
    orientadoresDao = OrientadoresDAO(db)
        
    if orientadoresDao.exists(id):
        orientadoresDao.ativa_orientador(id)
    else:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404
    return get_ok(response_messages.ENTIDADE_ATIVADA('Orientador')), 200

def desativa_orientador(id):
    db = get_db()
    orientadoresDao = OrientadoresDAO(db)
        
    if orientadoresDao.exists(id):
        orientadoresDao.desativa_orientador(id)
    else:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404
    return get_ok(response_messages.ENTIDADE_DESATIVADA('Orientador')), 200

def solicitar_revisao(codProjeto, professor_user_info):
    db = get_db()
    usuarioDao = UsuarioDAO(db)
    projetosDao = ProjetosDAO(db)
    orientadoresDao = OrientadoresDAO(db)
    usuarioOrientadoDao = UsuarioOrientadoDAO(db)

    orientador = orientadoresDao.get_orientador_codUsuario(professor_user_info['codUsuario'])
    if not orientador:
        return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400
    
    proj = projetosDao.get_projeto_novo(codProjeto, True)
    if not proj:
        return get_erro(response_messages.NAO_ENCONTRADO('Trabalho')), 404

    try:
        attr = get_request_form_data_attributes(['mensagem'])
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    usuarioOrientado = usuarioOrientadoDao.get_usuario_orientado_codProjeto_codOrientador(codProjeto, orientador['codOrientador'])
    if not usuarioOrientado:
        return get_erro(response_messages.ORIENTACAO_NECESSARIA()), 400

    usuarioDao.gerar_solitacao(usuarioOrientado['codUsuarioOrientado'], attr['mensagem'])

    for autor in proj['autores']:
        try:
            enviar_email_revisao(autor, proj['tituloProjeto'], attr['mensagem'])
        except SMTPAuthenticationError:
            db.rollback()
            return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL())

    return get_ok(response_messages.SOLICITACAO_REVISAO_ENVIADA()), 200

def verificar_revisoes(user_info):
    db = get_db()
    usuarioDao = UsuarioDAO(db)
    usuarioOrientadoDao = UsuarioOrientadoDAO(db)

    usuarioOrientado = usuarioOrientadoDao.get_usuario_orientado_aluno(user_info['codUsuario'])
    revisao = usuarioDao.verificar_revisao(usuarioOrientado['codUsuarioOrientado'])
    if revisao:
        return get_data(revisao), 200
    return None, 204

def enviar_email_revisao(autor, titulo_projeto, mensagem):
    msg = mailer.generate_message_html(
        'Solicitação de Revisão',
        autor['email'],
        '''
            <h2>Houve uma solocitação de revisão.</h2>

            <p>Olá, {0}.</p>

            <p>O seu projeto: <b>{1}</b>, recebeu uma solocitação de revisão pelo seu orientador com a seguinte mensagem:</p>

            <q>{2}</q>
        '''.format(autor['nomeAutor'], titulo_projeto, mensagem)
    )
    mailer.send_email(autor['email'], msg)
