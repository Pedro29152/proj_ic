from flask import request
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
    token_required
)
from . import orientadores_dao

class OrientadorResource(Resource):
    @admin_token_required
    def post(self):
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
                return get_erro('O codigo do orientador deve ter no maximo 20 caracteres e seu nome no maximo 200')

            return get_ok('Orientador gravado com sucesso')
        except AttributeError as ex:
            return get_erro(ex.__str__())
        except BadRequestKeyError:
            return get_erro('Os campos "nomeOrientador", "raOrientador", "email" e "linkCurrLattes" devem ser enviados no corpo da requisicao')
        except IntegrityError:
            return get_erro('Os campos "email" e "raAutor" devem ser unicos')

    @token_required
    def get(self):
        query = request.args.get('nomeOrientador')

        if query:
            ret = orientadores_dao.busca_orientadores_nome(query)
        else:
            ret = orientadores_dao.busca_orientadores()
        
        if ret:
            return get_data(ret)
        else:
            return get_falha('Nenhum orientador listado')

class TodosOrientadoresResource(Resource):
    @token_required
    def get(self):
        query = request.args.get('nomeOrientador')

        if query:
            ret = orientadores_dao.busca_todos_orientadores_nome(query)
        else:
            ret = orientadores_dao.busca_todos_orientadores()
        
        if ret:
            return get_data(ret)
        else:
            return get_falha('Nenhum orientador listado')

class AtivaOrientadorResource(Resource):
    @admin_token_required
    def post(self, id):
        if orientadores_dao.exists(id):
            orientadores_dao.ativa_orientador(id)
        else:
            return get_erro('Codigo do orientador enviado não esta cadastrado no sistema')
        return get_ok('Orientador ativado com sucesso')

class DesativaOrientadorResource(Resource):
    @admin_token_required
    def delete(self, id):
        if orientadores_dao.exists(id):
            orientadores_dao.desativa_orientador(id)
        else:
            return get_erro('Codigo do orientador enviado não esta cadastrado no sistema')
        return get_ok('Orientador desativado com sucesso')

class CountOrientadoresResource(Resource):
    @token_required
    def get(self):
        count = orientadores_dao.get_count()

        return get_count(count)
