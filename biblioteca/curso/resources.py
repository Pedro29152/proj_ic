from flask import jsonify
from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import IntegrityError

from biblioteca import mailer, response_messages
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
    generate_random_password,
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
    @secretaria_token_required
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

        return get_ok(response_messages.ENTIDADE_ATIVADA.format('Curso'))

class DesativaCursoResource(Resource):
    @secretaria_token_required
    def post(self, id):    
        cursos_dao.desativa_curso(id)

        return get_ok(response_messages.ENTIDADE_DESATIVADA.format('Curso'))

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
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS.format('"nome", "email", "nomeCurso" e "abreviacao"')), 400

    if not (nomeCurso and abreviacao and nome and email):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO), 400
    if len(abreviacao) > 3:
        return get_erro(response_messages.VALIDACAO_DEVE.format('abreviação', 'ter no máximo 3 caracteres'))
    username = 'coordenador_{}'.format(abreviacao.lower())
    password = generate_random_password()
    user = usuario_dao.add_usr(username, password, TiposUsuario.Coordenador.value, nome, email)
    if not user:
        return get_erro(response_messages.ERRO_INTEGRIDADE.format('Email ou abreviação')), 400

    curso = Cursos(
        nomeCurso, 
        abreviacao,
        user['codUsuario']
    )
    try:
        curso.grava_curso()

        msg = mailer.generate_message_html(
            'BTA - Nova conta de Coordenador',
            email,
            '''
                <h2>Você foi cadastrado no sistema BTA</h2>

                <p>Você foi cadastrado como um novo coordenador do sistema BTA - Biblioteca de Trabalhos Acadêmicos no curso: <b>{0}</b>, <b>{1}</b>.</p>
                <p>Veja abaixo os dados de login do seu usuário:</p>

                <p>Nome de usuário: <b>{2}</b></p>
                <p>Senha: <b>{3}</b></p>
            '''.format(abreviacao, nomeCurso, username, password)
        )
        mailer.send_email(email, msg)

        return get_ok(response_messages.ENTIDADE_GRAVADA.format('Curso')), 201
    except IntegrityError:
        if not cursos_dao.is_ativo(curso):
            cursos_dao.reativa_curso(curso)
            return get_ok('O curso ja existia, porem esta inativo. O curso foi reativado com os dados novos'), 400
        else:
            usuario_dao.deleta_usuario(user['codUsuario'])
            return get_erro(response_messages.ERRO_INTEGRIDADE.format('Nome ou breviacao')), 400

def buscar_cursos():
        cursos = cursos_dao.busca_cursos()
        
        if cursos:
            return get_data(cursos), 200
        return None, 204

def get_curso(codCurso):
    curso = cursos_dao.get_curso_codCurso(codCurso, False)
    coord = usuario_dao.get_user_coordenador(curso['codCurso'])
    curso.update(coord)
    if not curso:
        return get_erro(response_messages.NAO_ENCONTRADO.format('Codigo de curso')), 404
    return curso, 200

def edita_curso(codCurso):
    curso = cursos_dao.get_curso_codCurso(codCurso)
    if not curso:
        return get_erro(response_messages.NAO_ENCONTRADO.format('Codigo de curso')), 404

    try:
        descricaoCurso = request.form['nomeCurso'] 
        abreviacao = request.form['abreviacao']

        if descricaoCurso:
            curso.descricaoCurso = descricaoCurso
        if abreviacao:
            curso.abreviacao = abreviacao

        curso.edita_curso()
        
        return get_ok(response_messages.ENTIDADE_EDITADA.format('Curso')), 200

    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS.format('"nomeCurso" e "abreviacao"')), 400
    except IntegrityError:
        return get_erro(response_messages.ERRO_INTEGRIDADE.format('Abreviacao ou Nome do Curso')), 400

def buscar_todos_cursos():
        cursos = cursos_dao.busca_cursos_inativo()
    
        if cursos:
            return get_data(cursos), 200
        return None, 204
