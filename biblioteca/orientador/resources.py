from flask import request, jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError, IntegrityError

from .schemas import Orientadores
from biblioteca.usuarios import usuario_dao, usuario_orientado_dao
from biblioteca.autor import autores_dao
from biblioteca.responses import (
    get_erro,
    get_ok,
    get_data,
    get_falha,
    get_count,
    get_response_code
)
from biblioteca.extensions import(
    admin_token_required,
    secretaria_token_required,
    professor_token_required,
    professor_admin_token_required,
    aluno_token_required,
    token_required,
    is_valid_email,
    is_valid_http_link
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
            return get_erro('O codigo do orientador deve ter no maximo 13 caracteres e seu nome no maximo 200'), 400

        return get_ok('Orientador gravado com sucesso'), 201
    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro('Os campos "nomeOrientador", "raOrientador", "email" e "linkCurrLattes" devem ser enviados no corpo da requisicao'), 400
    except IntegrityError:
        return get_erro('Os campos "email" e "raAutor" devem ser unicos'), 400

def edita_orientador(codOrientador):
    ori = orientadores_dao.get_orientador_codigo(codOrientador)
    if not ori:
        return get_erro('Codigo de orientador enviado não existe'), 404

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
                raise AttributeError('O campo "email" deve ser um email valido')
        if currLattes:
            if not is_valid_http_link(currLattes):
                raise AttributeError('O campo "currLattes" deve ser um link http/https valido')
            ori.currLattes = currLattes

        ori.edita_orientador()

        return get_ok('Orientador editado com sucesso'), 200

    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro('Os campos "nomeOrientador", "raOrientador", "email" e "linkCurrLattes" devem ser enviados no corpo da requisicao'), 400
    except IntegrityError:
        return get_erro('Os campos "email" e "raAutor" devem ser unicos'), 400
    except DataError:
        return get_erro('O codigo do orientador deve ter no maximo 13 caracteres e seu nome no maximo 200'), 400

def get_orientador(codOrientador):
    ori = orientadores_dao.get_orientador_codigo(codOrientador, False)
    if not ori:
        return get_erro('Codigo de orientador enviado não existe'), 404
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
        return get_falha('Nenhum orientador listado'), 204

def busca_todos_orientadores():
    query = request.args.get('nomeOrientador')

    if query:
        ret = orientadores_dao.busca_todos_orientadores_nome(query)
    else:
        ret = orientadores_dao.busca_todos_orientadores()
    
    if ret:
        return get_data(ret), 200
    else:
        return get_falha('Nenhum orientador listado'), 204

def ativa_orientador(id):
    if orientadores_dao.exists(id):
        orientadores_dao.ativa_orientador(id)
    else:
        return get_erro('Codigo do orientador enviado não esta cadastrado no sistema'), 404
    return get_ok('Orientador ativado com sucesso'), 200

def desativa_orientador(id):
    if orientadores_dao.exists(id):
        orientadores_dao.desativa_orientador(id)
    else:
        return get_erro('Codigo do orientador enviado não esta cadastrado no sistema'), 404
    return get_ok('Orientador desativado com sucesso'), 200

def solicitar_revisao(codUsuario, professor_user_info):
    orientador = orientadores_dao.get_orientador_codUsuario(professor_user_info['codUsuario'])
    if not orientador:
        return get_erro('O usuario utilizado não está ligado a nenhum orientador'), 400
    
    try:
        mensagem = request.form['mensagem']
    except BadRequestKeyError:
        return get_erro('O campo "mensagem" devem ser enviados no corpo da requisicao'), 400


    usuarioOrientado = usuario_orientado_dao.get_usuario_orientado(orientador['codOrientador'], codUsuario)
    if usuarioOrientado:
        usuario_dao.gerar_solitacao(usuarioOrientado['codUsuarioOrientado'], mensagem)
        return get_ok('Solicitação de revisao enviada'), 200
    return get_erro('Você não esta orientando este usuário'), 400

def verificar_revisoes(user_info):
    usuarioOrientado = usuario_orientado_dao.get_usuario_orientado_aluno(user_info['codUsuario'])
    revisao = usuario_dao.verificar_revisao(usuarioOrientado['codUsuarioOrientado'])
    if revisao:
        return get_data(revisao), 200
    return None, 204
