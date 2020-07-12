from flask_restful import Resource
from flask import request, jsonify

from biblioteca.responses import (
    get_response_code,
    get_no_content,
    get_not_found,
    get_data,
    get_count
)
from biblioteca.extensions import (
    secretaria_token_required,
    coordenador_secretaria_token_required
) 
from . import coordenador_dao

class CoordenadorResource(Resource):
    @secretaria_token_required
    def get(self):
        nomeCoord = request.args.get('nomeCoordenador')
        if not nomeCoord:
            nomeCoord = ''
        
        coords = coordenador_dao.buscar_coordenadores(nomeCoord)
        if coords:
            return get_response_code(get_data(coords), 200)
        return get_no_content()

class GetCoordenadorResource(Resource):
    @coordenador_secretaria_token_required
    def get(self, id, user_info):
        coord = coordenador_dao.get_coordenador(id)
        if coord:
            return get_response_code(get_data(coord), 200)
        return get_not_found('Coordenador não encontrado')
        
class CountCoordenadoresResource(Resource):
    @secretaria_token_required
    def get(self):
        count = coordenador_dao.get_count()
        return get_count(count)
