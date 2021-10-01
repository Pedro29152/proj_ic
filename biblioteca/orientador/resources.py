from flask import request, jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError, IntegrityError

from .schemas import Orientadores
from biblioteca.db import Db
from biblioteca import mailer, response_messages
from biblioteca.projeto import projetos_dao
from biblioteca.usuarios import usuario_orientado_dao
from biblioteca.usuarios.usuario_dao import UsuarioDAO
from biblioteca.autor import autores_dao
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
    TiposUsuario
)
from . import orientadores_dao

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
        count = orientadores_dao.get_count()
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
        ret = orientadores_dao.buscar_revisoes()
        if ret:
            return get_response_code(ret, 200)
        return get_no_content()

class GetRevisaoResource(Resource):
    @secretaria_aluno_token_required
    def get(self, id, user_info):
        if user_info['tipoUsuario'] == TiposUsuario.Aluno.value:
            ret = orientadores_dao.get_revisao_codUsuario_autor(id, user_info['codUsuario'])    
        else:
            ret = orientadores_dao.get_revisao(id)
        
        if ret:
            return get_response_code(ret, 200)
        return get_not_found(response_messages.NAO_ENCONTRADO('Revisão'))

def cadastro_orientador():
    try:
        orientadores = Orientadores(
            nomeOrientador=request.form['nomeOrientador'],
            raOrientador=request.form['raOrientador'],
            email=request.form['email'],
            currLattes=request.form['linkCurrLattes']
        )
        try:
            orientadores.grava_orientador()
        except DataError:
            return get_erro(response_messages.VALIDACAO_DEVE('raOrientador', 'ter no maximo 5 caracteres e seu nome no maximo 200')), 400

        return get_ok(response_messages.ENTIDADE_GRAVADA('Orientador')), 201
    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"')), 400
    except IntegrityError:
        return get_erro(response_messages.ERRO_INTEGRIDADE('Email ou raAutor')), 400

def edita_orientador(codOrientador):
    ori = orientadores_dao.get_orientador_codigo(codOrientador)
    if not ori:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404

    try:
        nomeOrientador = request.form['nomeOrientador']
        raOrientador = request.form['raOrientador']
        email = request.form['email']
        currLattes = request.form['linkCurrLattes']

        if nomeOrientador:
            ori.nomeOrientador = nomeOrientador
        if raOrientador:
            ori.raOrientador = raOrientador
        if email:
            ori.email = email
            if not is_valid_email(email):
                raise AttributeError(response_messages.VALIDACAO_DEVE('email', 'ser um email valido'))
        if currLattes:
            if not is_valid_http_link(currLattes):
                raise AttributeError(response_messages.VALIDACAO_DEVE('currLattes', 'ser um link http/https valido'))
            ori.currLattes = currLattes

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

def get_orientador(codOrientador):
    ori = orientadores_dao.get_orientador_codigo(codOrientador, False)
    if not ori:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404
    return ori, 200

def busca_orientadores():
    query = request.args.get('nomeOrientador')

    if query:
        ret = orientadores_dao.busca_orientadores_nome(query)
    else:
        ret = orientadores_dao.busca_orientadores()
    
    if ret:
        return get_data(ret), 200
    else:
        return None, 204

def busca_todos_orientadores():
    query = request.args.get('nomeOrientador')

    if query:
        ret = orientadores_dao.busca_todos_orientadores_nome(query)
    else:
        ret = orientadores_dao.busca_todos_orientadores()
    
    if ret:
        return get_data(ret), 200
    else:
        return None, 204

def ativa_orientador(id):
    if orientadores_dao.exists(id):
        orientadores_dao.ativa_orientador(id)
    else:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404
    return get_ok(response_messages.ENTIDADE_ATIVADA('Orientador')), 200

def desativa_orientador(id):
    if orientadores_dao.exists(id):
        orientadores_dao.desativa_orientador(id)
    else:
        return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 404
    return get_ok(response_messages.ENTIDADE_DESATIVADA('Orientador')), 200

def solicitar_revisao(codProjeto, professor_user_info):
    with Db() as db:
        usuarioDao = UsuarioDAO(db)

        orientador = orientadores_dao.get_orientador_codUsuario(professor_user_info['codUsuario'])
        if not orientador:
            return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400
        
        proj = projetos_dao.get_projeto_novo(codProjeto, True)
        if not proj:
            return get_erro(response_messages.NAO_ENCONTRADO('Trabalho')), 404

        try:
            mensagem = request.form['mensagem']
        except BadRequestKeyError:
            return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"mensagem"')), 400


        usuarioOrientado = usuario_orientado_dao.get_usuario_orientado_codProjeto_codOrientador(codProjeto, orientador['codOrientador'])
        if usuarioOrientado:
            usuarioDao.gerar_solitacao(usuarioOrientado['codUsuarioOrientado'], mensagem)

            for autor in proj['autores']:
                enviar_email_revisao(autor, proj['tituloProjeto'], mensagem)

            return get_ok(response_messages.SOLICITACAO_REVISAO_ENVIADA()), 200
        return get_erro(response_messages.ORIENTACAO_NECESSARIA()), 400

def verificar_revisoes(user_info):
    with Db() as db:
        usuarioDao = UsuarioDAO(db)

        usuarioOrientado = usuario_orientado_dao.get_usuario_orientado_aluno(user_info['codUsuario'])
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



