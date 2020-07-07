from flask import jsonify
from flask_restful import Resource, request

from . import autores_dao 
from biblioteca.responses import (
    get_data,
    get_response_code
)

class BuscaAlunosResource(Resource):
    def get(self):
        nomeAutor = request.args.get('nomeAutor')
        ret = autores_dao.busca_autores(nomeAutor)
        if ret:
            return get_data(ret)
        return get_response_code(None, 204)