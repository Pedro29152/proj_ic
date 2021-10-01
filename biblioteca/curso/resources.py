from flask_restful import Resource, request
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import IntegrityError

from biblioteca.db import Db
from biblioteca import mailer, response_messages
from biblioteca.usuarios.usuario_dao import UsuarioDAO
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
from .cursos_dao import CursosDAO
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
        with Db() as db:
            cursosDao = CursosDAO(db)

            cursosDao.ativa_curso(id)

            return get_ok(response_messages.ENTIDADE_ATIVADA('Curso'))

class DesativaCursoResource(Resource):
    @secretaria_token_required
    def post(self, id):
        with Db() as db:
            cursosDao = CursosDAO(db)
                
            cursosDao.desativa_curso(id)

            return get_ok(response_messages.ENTIDADE_DESATIVADA('Curso'))

class TodosCursosResource(Resource):
    @secretaria_token_required
    def get(self):
        res, cod = buscar_todos_cursos()
        return get_response_code(res, cod)

class CountCursosResource(Resource):
    @secretaria_token_required
    def get(self):
        with Db() as db:
            cursosDao = CursosDAO(db)

            count = cursosDao.get_count()

            return get_count_res(count)


def cadastro_curso():
    try:
        nomeCurso = request.form['nomeCurso'] 
        abreviacao = request.form['abreviacao']
        nome = request.form['nome']
        email = request.form['email']
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"nome", "email", "nomeCurso" e "abreviacao"')), 400

    if not (nomeCurso and abreviacao and nome and email):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
    if len(abreviacao) > 3:
        return get_erro(response_messages.VALIDACAO_DEVE('abreviação', 'ter no máximo 3 caracteres'))
    
    username = 'coordenador_{}'.format(abreviacao.lower())
    password = generate_random_password()

    with Db() as db:
        usuarioDao = UsuarioDAO(db)
        cursosDao = CursosDAO(db)

        user = usuarioDao.add_usr(username, password, TiposUsuario.Coordenador.value, nome, email)
        if not user:
            return get_erro(response_messages.ERRO_INTEGRIDADE('Email ou abreviação')), 400

        curso = Cursos(
            nomeCurso, 
            abreviacao,
            user['codUsuario']
        )
        try:
            curso.grava_curso()

            msg = mailer.generate_message_html(
                'Nova conta de Coordenador',
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

            return get_ok(response_messages.ENTIDADE_GRAVADA('Curso')), 201
        except IntegrityError:
            if not cursosDao.is_ativo(curso):
                cursosDao.reativa_curso(curso)
                return get_ok('O curso ja existia, porem esta inativo. O curso foi reativado com os dados novos'), 400
            else:
                usuarioDao.deleta_usuario(user['codUsuario'])
                return get_erro(response_messages.ERRO_INTEGRIDADE('Nome ou breviacao')), 400

def buscar_cursos():
        with Db() as db:
            cursosDao = CursosDAO(db)

            cursos = cursosDao.busca_cursos()
            
            if cursos:
                return get_data(cursos), 200
            return None, 204

def get_curso(codCurso):
    with Db() as db:
        usuarioDao = UsuarioDAO(db)
        cursosDao = CursosDAO(db)

        curso = cursosDao.get_curso_codCurso(codCurso, False)
        coord = usuarioDao.get_user_coordenador(curso['codCurso'])
        curso.update(coord)
        if not curso:
            return get_erro(response_messages.NAO_ENCONTRADO('Codigo de curso')), 404
        return curso, 200

def edita_curso(codCurso):
    with Db() as db:
        cursosDao = CursosDAO(db)

        curso = cursosDao.get_curso_codCurso(codCurso)
        if not curso:
            return get_erro(response_messages.NAO_ENCONTRADO('Codigo de curso')), 404

        try:
            descricaoCurso = request.form['nomeCurso'] 
            abreviacao = request.form['abreviacao']

            if descricaoCurso:
                curso.descricaoCurso = descricaoCurso
            if abreviacao:
                curso.abreviacao = abreviacao

            curso.edita_curso()
            
            return get_ok(response_messages.ENTIDADE_EDITADA('Curso')), 200

        except AttributeError as ex:
            return get_erro(ex.__str__()), 400
        except BadRequestKeyError:
            return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"nomeCurso" e "abreviacao"')), 400
        except IntegrityError:
            return get_erro(response_messages.ERRO_INTEGRIDADE('Abreviacao ou Nome do Curso')), 400

def buscar_todos_cursos():
    with Db() as db:
        cursosDao = CursosDAO(db)

        cursos = cursosDao.busca_cursos_inativo()
        if cursos:
            return get_data(cursos), 200
        return None, 204
