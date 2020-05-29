from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import IntegrityError

from biblioteca.responses import (
    get_erro,
    get_falha,
    get_ok,
    get_data,
    get_count as get_count_res
)
from biblioteca.extensions import (
    secretaria_token_required,
    admin_token_required
)
from . import cursos_dao
from .schemas import Cursos

class CursoResource(Resource):
    @admin_token_required
    def post(self):
        try:
            nomeCurso = request.form['nomeCurso'] 
            abreviacao = request.form['abreviacao']
        except BadRequestKeyError:
            return get_erro('A requisicao deve conter os campos "nomeCurso" e "abreviacao" em seu corpo')

        if not (nomeCurso and abreviacao):
            return get_falha('Os campos enviados devem sem preenchidos')

        curso = Cursos(
            nomeCurso, 
            abreviacao
        )
        try:
            curso.grava_curso()
            return get_ok('Curso gravado com suscesso')
        except IntegrityError:
            if not cursos_dao.is_ativo(curso):
                cursos_dao.reativa_curso(curso)
                return get_ok('O curso ja existia, porem esta inativo. O curso foi reativado com os dados novos')
            else:
                return get_erro('O nome ou a breviacao desse curso ja foi cadastrado')

    @secretaria_token_required
    def get(self):
        cursos = cursos_dao.busca_cursos()
        
        return get_data(cursos)

class AtivaCursoResource(Resource):
    @admin_token_required
    def post(self, id):    
        cursos_dao.ativa_curso(id)

        return get_ok('Curso ativado com sucesso')

class DesativaCursoResource(Resource):
    @admin_token_required
    def post(self, id):    
        cursos_dao.desativa_curso(id)

        return get_ok('Curso desativado com sucesso')

class TodosCursosResource(Resource):
    @admin_token_required
    def get(self):
        cursos = cursos_dao.busca_cursos_inativo()
    
        return get_data(cursos)

class CountCursosResource(Resource):
    @secretaria_token_required
    def get(self):
        count = cursos_dao.get_count()

        return get_count_res(count)