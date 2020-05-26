from flask_restful import Resource

from biblioteca.usuarios import usuario_dao
from biblioteca.projeto import projetos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.curso import cursos_dao
from biblioteca.responses import get_data
from biblioteca.extensions import (
    token_required
)

class AllCountsResource(Resource):
    @token_required
    def get(self):
        usuarios_count = usuario_dao.get_count()
        projetos_count = projetos_dao.get_count()
        orientadores_count = orientadores_dao.get_count()
        cursos_count = cursos_dao.get_count()

        return get_data({
            'usuariosCount': usuarios_count,
            'projetosCount': projetos_count,
            'orientadoresCount': orientadores_count,
            'cursosCount': cursos_count,
        })
        
        