from flask import jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import IntegrityError

from biblioteca.usuarios import usuario_dao
from biblioteca.responses import (
    get_erro,
    get_falha,
    get_ok,
    get_data,
    get_count as get_count_res,
    get_response_code
)
from biblioteca.extensions import (
    secretaria_token_required,
    token_required,
    admin_token_required,
    TiposUsuario
)
from . import cursos_dao
from .schemas import Cursos

class CursoResource(Resource):
    @secretaria_token_required
    def post(self):
        res, cod = cadastro_curso()
        return get_response_code(res, cod)

    @token_required
    def get(self, user_info):
        res, cod = buscar_cursos()
        return get_response_code(res, cod)

class CursoIdResource(Resource):
    def get(self, id):
        res, cod = get_curso(id)
        return get_response_code(res, cod)

    @secretaria_token_required
    def put(self, id):
        res, cod = edita_curso(id)
        return get_response_code(res, cod)

class AtivaCursoResource(Resource):
    @secretaria_token_required
    def post(self, id):    
        cursos_dao.ativa_curso(id)

        return get_ok('Curso ativado com sucesso')

class DesativaCursoResource(Resource):
    @secretaria_token_required
    def post(self, id):    
        cursos_dao.desativa_curso(id)

        return get_ok('Curso desativado com sucesso')

class TodosCursosResource(Resource):
    @secretaria_token_required
    def get(self):
        res, cod = buscar_todos_cursos()
        return get_response_code(res, cod)

class CountCursosResource(Resource):
    @secretaria_token_required
    def get(self):
        count = cursos_dao.get_count()

        return get_count_res(count)


def cadastro_curso():
    try:
        nomeCurso = request.form['nomeCurso'] 
        abreviacao = request.form['abreviacao']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['password']
    except BadRequestKeyError:
        return get_erro('A requisicao deve conter os campos "nome", "email", "password", "nomeCurso" e "abreviacao" em seu corpo'), 400

    if not (nomeCurso and abreviacao and nome and email and senha):
        return get_falha('Os campos enviados devem sem preenchidos'), 400
    if len(abreviacao) > 3:
        return get_erro('A abreviação deve ter no máximo 3 caracteres')

    user = usuario_dao.add_usr('coordenador_{}'.format(abreviacao.lower()), senha, TiposUsuario.Coordenador.value, nome, email)

    curso = Cursos(
        nomeCurso, 
        abreviacao,
        user['codUsuario']
    )
    try:
        curso.grava_curso()
        return get_ok('Curso gravado com suscesso'), 201
    except IntegrityError:
        if not cursos_dao.is_ativo(curso):
            cursos_dao.reativa_curso(curso)
            return get_ok('O curso ja existia, porem esta inativo. O curso foi reativado com os dados novos'), 400
        else:
            return get_erro('O nome ou a breviacao desse curso ja foi cadastrado'), 400

def buscar_cursos():
        cursos = cursos_dao.busca_cursos()
        
        if cursos:
            return get_data(cursos), 200
        return get_falha("Nenhum curso listado"), 204

def get_curso(codCurso):
    curso = cursos_dao.get_curso_codCurso(codCurso, False)
    if not curso:
        return get_erro('Codigo de curso nao encontrado'), 404
    return curso, 200

def edita_curso(codCurso):
    curso = cursos_dao.get_curso_codCurso(codCurso)
    if not curso:
        return get_erro('Codigo de curso nao encontrado'), 404

    try:
        descricaoCurso = request.form['nomeCurso'] 
        abreviacao = request.form['abreviacao']

        if descricaoCurso:
            curso.descricaoCurso = descricaoCurso
        if abreviacao:
            curso.abreviacao = abreviacao

        curso.edita_curso()
        
        return get_ok('Curso editado com sucesso'), 200

    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro('A requisicao deve conter os campos "nomeCurso" e "abreviacao" em seu corpo'), 400
    except IntegrityError:
        return get_erro('Os campos "abreviacao" e "nomeCurso" devem ser unicos'), 400

def buscar_todos_cursos():
        cursos = cursos_dao.busca_cursos_inativo()
    
        if cursos:
            return get_data(cursos), 200
        return get_falha("Nenhum curso listado"), 204




