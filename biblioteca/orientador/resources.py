from flask import request, jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError, IntegrityError

from .schemas import Orientadores
from biblioteca.responses import (
    get_erro,
    get_ok,
    get_data,
    get_falha,
    get_count
)
from biblioteca.extensions import(
    admin_token_required,
    secretaria_token_required,
    professor_token_required
)
from . import orientadores_dao

class OrientadorResource(Resource):
    @admin_token_required
    def post(self):
        res, cod = cadastro_orientador()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

    @secretaria_token_required
    def get(self):
        res, cod = busca_orientadores()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class TodosOrientadoresResource(Resource):
    @secretaria_token_required
    def get(self):
        res, cod = busca_todos_orientadores()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class EditaOrientadorResource(Resource):
    @professor_token_required
    def put(self, id):
        res, cod = edita_orientador(id)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class GetOrientadorResource(Resource):
    def get(self, id):
        res, cod = get_orientador(id)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class AtivaOrientadorResource(Resource):
    @admin_token_required
    def post(self, id):
        res, cod = ativa_orientador(id)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class DesativaOrientadorResource(Resource):
    @admin_token_required
    def delete(self, id):
        res, cod = desativa_orientador(id)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class CountOrientadoresResource(Resource):
    @secretaria_token_required
    def get(self):
        count = orientadores_dao.get_count()

        return get_count(count)


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
            return get_erro('O codigo do orientador deve ter no maximo 20 caracteres e seu nome no maximo 200'), 400

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
        if currLattes:
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
        return get_erro('O codigo do orientador deve ter no maximo 20 caracteres e seu nome no maximo 200'), 400

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
