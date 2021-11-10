from smtplib import SMTPAuthenticationError
from flask_restful import Resource, request
from werkzeug import exceptions
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import IntegrityError

from biblioteca.db import get_db
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
    get_request_form_data_attributes,
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
        try:
            attr = get_request_form_data_attributes(['codUsuario'])
        except Exception as ex:
            return get_erro(ex.__str__()), 400

        if not (attr['codUsuario']):
            return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400

        db = get_db()
        cursosDao = CursosDAO(db)
        usuarioDao = UsuarioDAO(db)

        user = usuarioDao.get_usuario_ativo(attr['codUsuario'])
        if not user:
            return get_falha(response_messages.USUARIO_NAO_EXISTE()), 400

        if not user['tipoUsuario'] == TiposUsuario.Coordenador.value:
            return  get_falha(response_messages.TIPO_USUARIO_ERRADO('Coordenador')), 400

        cursosDao.ativa_curso(id, user['codUsuario'])

        return get_ok(response_messages.ENTIDADE_ATIVADA('Curso'))

class DesativaCursoResource(Resource):
    @secretaria_token_required
    def post(self, id):
        db = get_db()
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
        db = get_db()
        cursosDao = CursosDAO(db)

        count = cursosDao.get_count()

        return get_count_res(count)


def cadastro_curso():
    try:
        attr = get_request_form_data_attributes(['nomeCurso', 'abreviacao', 'nome', 'email'])
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    if not (attr['nomeCurso'] and attr['abreviacao'] and attr['nome'] and attr['email']):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
    if len(attr['abreviacao']) > 3:
        return get_erro(response_messages.VALIDACAO_DEVE('abreviação', 'ter no máximo 3 caracteres'))
    
    username = 'coordenador_{}'.format(attr['abreviacao'].lower())
    password = generate_random_password()

    db = get_db()
    usuarioDao = UsuarioDAO(db)
    cursosDao = CursosDAO(db)

    try:
        user = usuarioDao.add_usr(username, password, TiposUsuario.Coordenador.value, attr['nome'], attr['email'])
        if not user:
            db.rollback()
            return get_erro(response_messages.ERRO_INESPERADO()), 500
    except IntegrityError as ie:
        db.rollback()
        return get_erro(ie.__str__()), 400

    curso = Cursos(
        attr['nomeCurso'], 
        attr['abreviacao'],
        user['codUsuario'],
        db=db
    )

    try:
        curso.grava_curso()

        __enviar_email_cadastro_curso(attr['email'], attr['abreviacao'], attr['nomeCurso'], username, password)

        return get_ok(response_messages.ENTIDADE_GRAVADA('Curso')), 201
    except IntegrityError:
        if not cursosDao.is_ativo(curso):
            try:
                cursosDao.reativa_curso(curso)

                __enviar_email_cadastro_curso(attr['email'], attr['abreviacao'], attr['nomeCurso'], username, password)                        

                return get_ok(response_messages.CURSO_REATIVADO()), 200
            except SMTPAuthenticationError as se:
                db.rollback()
                return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL()), 500
            except Exception as ex:
                db.rollback()
                return get_erro(response_messages.ERRO_INESPERADO()), 500
        else:
            db.rollback()
            return get_erro(response_messages.ERRO_INTEGRIDADE('Nome ou breviacao')), 400
    except SMTPAuthenticationError as se:
        db.rollback()
        return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL()), 500

def buscar_cursos():
        db = get_db()
        cursosDao = CursosDAO(db)

        cursos = cursosDao.busca_cursos()
        
        if cursos:
            return get_data(cursos), 200
        return None, 204

def get_curso(codCurso):
    db = get_db()
    usuarioDao = UsuarioDAO(db)
    cursosDao = CursosDAO(db)

    curso = cursosDao.get_curso_codCurso(codCurso, False)
    coord = usuarioDao.get_user_coordenador(curso['codCurso'])
    curso.update(coord)
    if not curso:
        return get_erro(response_messages.NAO_ENCONTRADO('Codigo de curso')), 404
    return curso, 200

def edita_curso(codCurso):
    db = get_db()
    cursosDao = CursosDAO(db)

    curso = cursosDao.get_curso_codCurso(codCurso)
    if not curso:
        return get_erro(response_messages.NAO_ENCONTRADO('Codigo de curso')), 404

    try:
        attr = get_request_form_data_attributes(['nomeCurso', 'abreviacao'])

        if attr['nomeCurso']:
            curso.descricaoCurso = attr['nomeCurso']
        if attr['abreviacao']:
            curso.abreviacao = attr['abreviacao']

        curso.edita_curso()
        
        return get_ok(response_messages.ENTIDADE_EDITADA('Curso')), 200

    except AttributeError as ex:
        return get_erro(ex.__str__()), 400
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"nomeCurso" e "abreviacao"')), 400
    except IntegrityError:
        return get_erro(response_messages.ERRO_INTEGRIDADE('Abreviacao ou Nome do Curso')), 400
    except Exception as ex:
        return get_erro(ex.__str__()), 400

def buscar_todos_cursos():
    db = get_db()
    cursosDao = CursosDAO(db)

    cursos = cursosDao.busca_cursos_inativo()
    if cursos:
        return get_data(cursos), 200
    return None, 204

def __enviar_email_cadastro_curso(email, abreviacao, nomeCurso, username, password):
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
