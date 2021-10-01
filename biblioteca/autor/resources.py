from flask import jsonify
from flask_restful import Resource, request

from .autores_dao import AutoresDAO
from biblioteca.db import Db
from biblioteca import response_messages
from biblioteca.responses import (
    get_data,
    get_response_code,
    get_not_found,
    get_success
)
from biblioteca.extensions import (
    token_required,
    aluno_token_required
)

class BuscaAlunosResource(Resource):
    @token_required
    def get(self, user_info):
        with Db() as db:
            autoresDao = AutoresDAO(db)

            nomeAutor = request.args.get('nomeAutor')
            ret = autoresDao.busca_autores(nomeAutor)
            if ret:
                return get_data(ret)
            return get_response_code(None, 204)

class GetAlunoResource(Resource):
    @token_required
    def get(self, id, user_info):
        with Db() as db:
            autoresDao = AutoresDAO(db)

            ret = autoresDao.get_autor(id)
            if ret:
                return get_data(ret)
            return get_not_found(response_messages.NAO_ENCONTRADO('Autor'))

class GetSelfAlunoResource(Resource):
    @aluno_token_required
    def get(self, user_info):
        with Db() as db:
            autoresDao = AutoresDAO(db)

            autor = autoresDao.get_autor_codUsuario(user_info['codUsuario'])
            orientador = autoresDao.get_orientador_codAutor(autor['codAutor'])
            if autor:
                return get_success({
                    'autor': autor, 
                    'orientador':orientador
                })
            return get_not_found(response_messages.NAO_ENCONTRADO('Autor'))

