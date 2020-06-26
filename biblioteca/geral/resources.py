from flask_restful import Resource

from biblioteca.usuarios import usuario_dao
from biblioteca.projeto import projetos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.curso import cursos_dao
from biblioteca.responses import (
    get_data,
    get_unauthorized,
    get_bad_request
)
from biblioteca.extensions import (
    token_required,
    TiposUsuario
)

class AllCountsResource(Resource):
    @token_required
    def get(self, user_info):
        if (user_info['tipoUsuario'] == TiposUsuario.Aluno.value):
            return get_unauthorized('Seu nível de acesso não lhe permite essa ação')
        if (user_info['tipoUsuario'] == TiposUsuario.Professor.value):
            orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request('O usuário utilizado não possui um orientador ligado a ele')

            usuarios_count = usuario_dao.get_count(codOrientador=orientador['codOrientador'])
            projetos_count = projetos_dao.get_count(codOrientador=orientador['codOrientador'])
            cursos_count = cursos_dao.get_count()

            return get_data({
                'usuariosCount': usuarios_count,
                'projetosCount': projetos_count,
                'cursosCount': cursos_count,
            })
        if (user_info['tipoUsuario'] == TiposUsuario.Secretaria.value):
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
        if (user_info['tipoUsuario'] == TiposUsuario.Coordenador.value):
            return "WIP"
        if (user_info['tipoUsuario'] == TiposUsuario.Administrador.value):
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
