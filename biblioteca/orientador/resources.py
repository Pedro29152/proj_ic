from flask import request
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError

from .schemas import Orientadores
from biblioteca.responses import (
    get_erro,
    get_ok,
    get_data,
    get_falha,
    get_count as get_count_res
)
from biblioteca.extensions import(
    admin_token_required,
    token_required
)
from .orientadores_dao import (
    busca_orientadores_nome,
    busca_orientadores,
    get_count
)

class OrientadorResource(Resource):
    @admin_token_required
    def post(self):
        try:
            orientadores = Orientadores(
                nomeOrientador=request.form['nomeOrientador'],
                raOrientador=request.form['raOrientador']
            )
            try:
                orientadores.grava_orientador()
            except DataError:
                return get_erro('O codigo do orientador deve ter no maximo 20 caracteres e seu nome no maximo 200')

            return get_ok('Orientador gravado com sucesso')
        except AttributeError:
            return get_erro('Valores invalidos para "nomeOrientador" e "raOrientador"')
        except BadRequestKeyError:
            return get_erro('Os campos "nomeOrientador" e "raOrientador" devem ser enviados no corpo da requisicao')

    @token_required
    def get(self):
        query = request.args.get('nomeOrientador')

        if query:
            ret = busca_orientadores_nome(query)
        else:
            ret = busca_orientadores()
        
        if ret:
            return get_data(ret)
        else:
            return get_falha('Nenhum orientador listado')

class CountOrientadoresResource(Resource):
    @token_required
    def get(self):
        count = get_count()

        return get_count_res(count)
