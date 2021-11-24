import jwt
from flask import jsonify, current_app as app
from flask_restful import Resource, request, current_app
from smtplib import SMTPAuthenticationError
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError, IntegrityError
from datetime import datetime, timedelta

from . import util
from .usuario_orientado_dao import UsuarioOrientadoDAO
from .usuario_dao import UsuarioDAO
from biblioteca.db import get_db
from biblioteca import mailer, response_messages
from biblioteca.orientador.schemas import Orientadores
from biblioteca.curso.cursos_dao import CursosDAO
from biblioteca.autor.autores_dao import AutoresDAO
from biblioteca.projeto.projetos_dao import ProjetosDAO
from biblioteca.orientador.orientadores_dao import OrientadoresDAO
from biblioteca.extensions import (
    secretaria_token_required,
    admin_token_required,
    user_admin_token_required,
    professor_token_required,
    is_valid_email,
    is_valid_username,
    get_request_form_data_attributes,
    admin_is_user_token_required,
    secretaria_token_required_user_info,
    secretaria_token_required_is_user,
    coordenador_secretaria_token_required,
    coordenador_token_required,
    token_required,
    generate_random_password,
    TiposUsuario
)
from biblioteca.responses import (
    get_falha,
    get_erro,
    get_ok,
    get_data,
    get_count,
    get_response_code,
    get_not_found
)

class LoginResource(Resource):
    def post(self):
        res, cod = login()
        return get_response_code(res, cod)

class UsuarioIdResource(Resource):
    @user_admin_token_required
    def get(self, id, is_user, is_admin):
        res, cod = get_usuario_ativo(id)
        return get_response_code(res, cod)

    @user_admin_token_required
    def delete(self, id, is_user, is_admin):
        res, cod = deleta_usuario(id, is_user)
        return get_response_code(res, cod)

    @user_admin_token_required
    def put(self, id, is_user, is_admin):
        res, cod = edita_usuario(id, is_admin, is_user)
        return get_response_code(res, cod)

class CadastroUsuarioResource(Resource):
    @admin_token_required
    def post(self):
        res, cod = cadastro_usuario()
        return get_response_code(res, cod)

class CadastroAlunoResource(Resource):
    @professor_token_required
    def post(self, user_info):
        res, cod = cadastro_aluno(user_info)
        return get_response_code(res, cod)

class CadastroProfessorExistenteResource(Resource):
    @secretaria_token_required
    def post(self):
        data, cod = cadastro_professor(True)
        return get_response_code(data, cod)

class CadastroProfessorNovoResource(Resource):
    @secretaria_token_required
    def post(self):
        data, cod = cadastro_professor(False)
        return get_response_code(data, cod)

class DesativaUsuarioResource(Resource):
    @admin_is_user_token_required
    def delete(self, id, is_user):
        res, cod = desativa_usuario(id, is_user)
        return get_response_code(res, cod)

class AtivaUsuarioResource(Resource):
    @admin_is_user_token_required
    def post(self, id, is_user):
        res, cod = ativa_usuario(id, is_user)
        return get_response_code(res, cod)

class AlterarOrientadorDoAlunoResource(Resource):
    @coordenador_token_required
    def put(self, id, user_info):
        res, cod = altera_orientador_aluno(id, user_info)
        return get_response_code(res, cod)

class CountUsuariosResource(Resource):
    @secretaria_token_required
    def get(self):
        db = get_db()
        usuarioDao = UsuarioDAO(db)

        count = usuarioDao.get_count()
        return get_count(count)

class BuscaUsuariosResource(Resource):
    @admin_token_required
    def get(self):
        res, cod = busca_usuarios()
        return get_response_code(res, cod)

class BuscaUsuariosInativosResource(Resource):
    @admin_token_required
    def get(self):
        res, cod = busca_usuarios_inativos()
        return get_response_code(res, cod)

class BuscaUsuariosOrientadosResource(Resource):
    @professor_token_required
    def get(self, user_info):
        res, cod = buscar_usuarios_orientados(user_info)
        return get_response_code(res, cod)

class BuscarUsuariosSecretariaAdmResource(Resource):
    @secretaria_token_required_user_info
    def get(self, user_info):
        ret, cod = busca_usuarios_secretaria_adm(user_info)
        return get_response_code(ret, cod)

class MudarSenhaUsuarioResource(Resource):
    @user_admin_token_required
    def put(self, id, is_user, is_admin):
        res, cod = mudar_senha(id)
        return get_response_code(res, cod)

class MudarSenhaResource(Resource):
    @token_required
    def put(self, user_info):
        ret, cod = mudar_senha(user_info['codUsuario'])
        return get_response_code(ret, cod)

class AlterarUsuarioResource(Resource):
    @token_required
    def put(self, user_info):
        is_admin = False
        if TiposUsuario.Administrador.value:
            is_admin = True

        ret, cod = edita_usuario(user_info['codUsuario'], is_admin, True)
        return get_response_code(ret, cod)

class GetUsuarioProprioREsource(Resource):
    @token_required
    def get(self, user_info):
        return get_data(user_info)

class RecuperaraSenha(Resource):
    def post(self):
        data, cod = recuperar_senha()
        return get_response_code(data, cod)

def login():
    try:
        attr = get_request_form_data_attributes(['username', 'password'])
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    db = get_db()
    usuarioDao = UsuarioDAO(db)

    usr = usuarioDao.verifica_usr(attr['username'], attr['password'])
    if not usr:
        return get_erro(response_messages.USUARIO_SENHA_INCORRETOS()), 401

    extDt = datetime.now() + timedelta(hours=1)
    extDt = extDt.__str__()
    token_data = {
        'username': usr['nomeUsuario'], 
        'tipoUsuario': str(usr['tipoUsuario']),
        'nome': usr['nome'],
        'ext': extDt
    }

    token = jwt.encode(
        token_data,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    ret = get_ok("Usuario logado com sucesso")
    ret['token'] = token
    ret['data'] = token_data
    return ret, 200

def cadastro_usuario():
    try:
        attr = get_request_form_data_attributes(['username', 'password', 'tipoUsuario', 'nome', 'email'])
        attr['tipoUsuario'] = int(attr['tipoUsuario'])
    except ValueError:
        return get_erro(response_messages.VALIDACAO_DEVE('tipoUsuario', 'ser do tipo inteiro')), 400
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    if not (attr['username'] and attr['tipoUsuario'] and attr['password'] and attr['email'] and attr['nome']):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
    if not is_valid_email(attr['email']):
        return get_erro(response_messages.VALIDACAO_DEVE('email',  'ser um email valido')), 400
    if not is_valid_username(attr['username']):
        return get_erro(response_messages.VALIDACAO_DEVE('username', 'ser um nome de usuario valido')), 400
    if not (attr['tipoUsuario'] - 1) in range(TiposUsuario.Coordenador.value):
        return get_falha(response_messages.ATRIBUTO_INVALIDO('tipoUsuario')), 400
    if attr['tipoUsuario'] == TiposUsuario.Aluno.value:
        return get_falha(response_messages.NOVA_ROTA_CADASTRO('aluno', '"/api/usuarios/cadastro/aluno"')), 400
    if attr['tipoUsuario'] == TiposUsuario.Professor.value:
        return get_falha(response_messages.NOVA_ROTA_CADASTRO('orientador' '"/api/usuarios/cadastro/orientador/novo"')), 400

    db = get_db()
    usuarioDao = UsuarioDAO(db)

    try:
        usuarioDao.add_usr(attr['username'], attr['password'], attr['tipoUsuario'], attr['nome'], attr['email'])
        return get_ok(response_messages.ENTIDADE_GRAVADA('Usuario')), 201
    except IntegrityError as ie:
        db.rollback()
        return get_erro(ie.__str__()), 400

def cadastro_professor(existente=True):
    try:
        base = ['nome', 'email']
        if existente:
            attr = get_request_form_data_attributes(base + ['codOrientador'])

            if not (attr['email'] and attr['nome'] and attr['codOrientador']):
                return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
        else:
            attr = get_request_form_data_attributes(base + ['currLattes', 'ra'])

            if not (attr['email'] and attr['nome'] and attr['currLattes'] and attr['ra']):
                return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    if not is_valid_email(attr['email']):
        return get_erro(response_messages.VALIDACAO_DEVE('email', 'ser um email valido')), 400

    db = get_db()
    try:
        usuarioDao = UsuarioDAO(db)
        orientadoresDao = OrientadoresDAO(db)

        if not existente:
            orientador = Orientadores(
                nomeOrientador=attr['nome'],
                raOrientador=attr['ra'],
                email=attr['email'],
                currLattes=attr['currLattes'],
                db=db
            )
            orientador.grava_orientador()

            attr['codOrientador'] = orientador.codOrientador
        else:
            if not orientadoresDao.exists(attr['codOrientador']):
                return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 400
                
        orientador = orientadoresDao.get_orientador_codigo(attr['codOrientador'], is_instance= False)
        user = orientador['raOrientador']
        password = generate_random_password()

        usuarioDao.add_orientador(user, password, attr['nome'], attr['email'], attr['codOrientador'])
        
        msg = mailer.generate_message_html(
            'Nova conta de Orientador',
            attr['email'],
            '''
                <h2>Você foi cadastrado no sistema BTA</h2>

                <p>Você foi cadastrado como um novo orientador do sistema BTA - Biblioteca de Trabalhos Acadêmicos.</p>
                <p>Veja abaixo os dados de login do seu usuário:</p>

                <p>Nome de usuário: <b>{0}</b></p>
                <p>Senha: <b>{1}</b></p>
            '''.format(user, password)
        )
        mailer.send_email(attr['email'], msg)
       
        ret = get_ok(response_messages.ENTIDADE_GRAVADA('Usuario'))
        if app.config['FLASK_ENV'] == 'testing':
            ret['password'] = password
        return ret, 201
    except SMTPAuthenticationError as se:
        db.rollback()
        return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL()), 500
    except Exception as ex:
        db.rollback()
        return get_erro(ex.__str__()), 400

def cadastro_aluno(professor_user_info):
    try:
        attr = get_request_form_data_attributes(['nome', 'email', 'ra_aluno', 'codCurso'])
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    if not (attr['email'] and attr['nome'] and attr['ra_aluno'] and attr['codCurso']):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
    if not is_valid_email(attr['email']):
        return get_erro(response_messages.VALIDACAO_DEVE('email', 'ser um email valido')), 400

    try:
        db = get_db()
        usuarioDao = UsuarioDAO(db)
        orientadoresDao = OrientadoresDAO(db)
        cursosDao = CursosDAO(db)
        autoresDao = AutoresDAO(db)

        curso = cursosDao.get_curso_codCurso(attr['codCurso'], False)
        if not curso:
            return get_falha(response_messages.NAO_ENCONTRADO('Curso')), 400

        autor = autoresDao.get_autor_ra(attr['ra_aluno'])
        if not autor:
            autor = autoresDao.cadastra_autor(attr['nome'], attr['email'], attr['ra_aluno'])
            if not autor:
                return get_erro(response_messages.ERRO_INESPERADO()), 500

        orientador = orientadoresDao.get_orientador_codUsuario(professor_user_info['codUsuario'])
        if not orientador:
            return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400

        password = generate_random_password()
        usuarioDao.add_aluno(attr['ra_aluno'], password, attr['nome'], attr['email'], autor['codAutor'], orientador['codOrientador'], attr['codCurso'])

        msg = mailer.generate_message_html(
            'Nova conta de Autor',
            attr['email'],
            '''
                <h2>Você foi cadastrado no sistema BTA</h2>

                <p>Você foi cadastrado como um novo autor do sistema BTA - Biblioteca de Trabalhos Acadêmicos.</p>
                <p>Veja abaixo os dados de login do seu usuário:</p>

                <p>Nome de usuário: <b>{0}</b></p>
                <p>Senha: <b>{1}</b></p>
            '''.format(attr['ra_aluno'], password)
        )
        mailer.send_email(attr['email'], msg)

        ret = get_ok(response_messages.ENTIDADE_GRAVADA('Usuario'))
        if app.config['FLASK_ENV'] == 'testing':
            ret['password'] = password
        return ret, 201
    except SMTPAuthenticationError as se:
        db.rollback()
        return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL()), 500
    except Exception as ex:
        db.rollback()
        return get_erro(ex.__str__()), 400

def desativa_usuario(codUsuario, is_user):
    if is_user:
        return get_erro(response_messages.SEM_PERMICAO('desativar o próprio usuário')), 400
        
    db = get_db()
    usuarioDao = UsuarioDAO(db)

    usr = usuarioDao.get_usuario_ativo(codUsuario)
    if not usr:
        return get_erro(response_messages.NAO_ENCONTRADO('Usuário')), 404

    if usr['tipoUsuario'] == TiposUsuario.Coordenador.value:
        return get_erro(response_messages.SEM_PERMICAO('desativar um usuario do tipo Coordenador')), 400

    usuarioDao.desativa_usuario(codUsuario)
    return get_ok(response_messages.ENTIDADE_DESATIVADA('Usuario')), 200

def ativa_usuario(codUsuario, is_user):
    if is_user:
        return get_erro(response_messages.SEM_PERMICAO('ativar o próprio usuário')), 400

    db = get_db()
    usuarioDao = UsuarioDAO(db)

    usr = usuarioDao.get_usuario_inativo(codUsuario)
    if not usr:
        return get_erro(response_messages.NAO_ENCONTRADO('Usuário')), 404

    usuarioDao.ativa_usuario(codUsuario)
    return get_ok(response_messages.ENTIDADE_ATIVADA('Usuario')), 200

def deleta_usuario(codUsuario, is_user):
    if is_user:
        return get_falha(response_messages.SEM_PERMICAO('deletar o próprio usuário')), 400
    
    db = get_db()
    usuarioDao = UsuarioDAO(db)

    usr = usuarioDao.get_usuario(codUsuario)
    if not usr:
        return get_erro(response_messages.NAO_ENCONTRADO('Usuário')), 404

    if usr['tipoUsuario'] == TiposUsuario.Coordenador.value:
        return get_erro(response_messages.SEM_PERMICAO('apagar um usuario do tipo Coordenador')), 400

    usuarioDao.deleta_usuario(codUsuario)
    return get_ok(response_messages.ENTIDADE_DELETADA('Usuario')), 200

def busca_usuarios():
    db = get_db()
    usuarioDao = UsuarioDAO(db)

    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuarioDao.busca_usuarios_nome_like(nome)
    else:
        ret = usuarioDao.busca_usuarios()
    
    if ret:
        return get_data(ret), 200
    return None, 204

def buscar_usuarios_orientados(user_info):
    db = get_db()
    usuarioDao = UsuarioDAO(db)
    orientadoresDao = OrientadoresDAO(db)

    orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
    if not orientador:
        return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400

    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuarioDao.busca_usuarios_orientados_nome_like(nome, orientador['codOrientador'])
    else:
        ret = usuarioDao.busca_usuarios_orientados(orientador['codOrientador'])
    
    if ret:
        return get_data(ret), 200
    return None, 204

def busca_usuarios_inativos():
    db = get_db()
    usuarioDao = UsuarioDAO(db)

    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuarioDao.busca_usuarios_inativos_nome_like(nome)
    else:
        ret = usuarioDao.busca_usuarios_inativos()
    
    if ret:
        return get_data(ret), 200
    return None, 204

def busca_usuarios_secretaria_adm(user_info):
    db = get_db()
    usuarioDao = UsuarioDAO(db)

    nome = request.args.get('nomeUsuario')

    if user_info['tipoUsuario'] == TiposUsuario.Secretaria.value:
        usuarios = usuarioDao.buscar_usuarios_secretaria(nome)
        if usuarios:
            return get_data(usuarios), 200
        return None, 204
        
    elif user_info['tipoUsuario'] == TiposUsuario.Administrador.value:
        usuarios = usuarioDao.buscar_usuarios_admin(nome)
        if usuarios:
            return get_data(usuarios), 200
        return None, 204
    
    else:
        return get_erro(response_messages.TIPO_USUARIO_ERRADO('secretaria ou admin'))

def get_usuario_ativo(id):
    db = get_db()
    usuarioDao = UsuarioDAO(db)

    codUsuario = int(id)

    ret = usuarioDao.get_usuario_ativo(codUsuario)
    if ret:
        return get_data(ret), 200
    return get_falha(response_messages.NAO_ENCONTRADO('Usuário')), 404

def edita_usuario(codUsuario, is_admin, is_user):
    try:
        base = ['nome', 'email']
        if is_admin and not is_user:
            attr = get_request_form_data_attributes(base + ['nomeUsuario', 'tipoUsuario'])
        else:
            attr = get_request_form_data_attributes(base)
            attr['nomeUsuario'] = None
            attr['tipoUsuario'] = None
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    db = get_db()
    usuarioDao = UsuarioDAO(db)

    usr = usuarioDao.get_usuario_ativo(codUsuario)
    if not usr:
        return get_falha(response_messages.NAO_ENCONTRADO('Usuário')), 404

    if not is_admin:
        if usr['tipoUsuario'] == TiposUsuario.Administrador.value:
            return get_erro(response_messages.SEM_PERMICAO('alterar um administrador sem ser um administrador')), 400

    if attr['nomeUsuario']:
        if not is_valid_username(attr['nomeUsuario']):
            return get_erro(response_messages.VALIDACAO_DEVE('nomeUsuario', 'ser um nome de usuario válido')), 400
        usr['nomeUsuario'] = attr['nomeUsuario']
    if attr['nome']: 
        usr['nome'] = attr['nome']
    if attr['email']: 
        if not is_valid_email(attr['email']):
            return get_erro(response_messages.VALIDACAO_DEVE('email', 'ser um email valido')), 400
        usr['email'] = attr['email']
    if attr['tipoUsuario']: 
        usr['tipoUsuario'] = attr['tipoUsuario']

    usuarioDao.edita_usuario(usr)

    return get_ok(response_messages.ENTIDADE_EDITADA('Usuario')), 200

def altera_orientador_aluno(codProjeto, user_info):
        db = get_db()
        projetosDao = ProjetosDAO(db)
        orientadoresDao = OrientadoresDAO(db)
        usuarioOrientadoDao = UsuarioOrientadoDAO(db)
        cursosDao = CursosDAO(db)
            
        proj = projetosDao.get_projeto_novo(codProjeto, True)
        if not proj:
            return get_erro(response_messages.NAO_ENCONTRADO('Trabalho')), 404
        curso = cursosDao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
        if not curso:
            return get_erro(response_messages.SEM_PERMICAO('ter acesso a esta ação')), 400

        if not proj['curso']['abreviacao'] == curso['abreviacao']:
            return get_erro(response_messages.SEM_PERMICAO('ter acesso a esta ação')), 400
        
        try:
            attr = get_request_form_data_attributes(['codOrientador'])
        except Exception as ex:
            return get_erro(ex.__str__()), 400

        if not util.is_cod_valido(attr['codOrientador']):
            return get_erro(response_messages.VALIDACAO_DEVE('codOrientador', 'ser um numero inteiro')), 400

        orientador = orientadoresDao.get_orientador_codigo(attr['codOrientador'], False)
        if not orientador:
            return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 400
        if not orientador['codUsuario']:
            return get_erro(response_messages.NAO_ENCONTRADO('Orientador')), 400
        try:
            usuarioOrientadoDao.edita_orientador_projeto_novo(codProjeto, orientador['codOrientador'])
        except Exception as ex:
            db.rollback()
            return get_erro(ex.__str__())

        return None, 204

def mudar_senha(id):
    try:
        attr = get_request_form_data_attributes(['senha'])
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    db = get_db()
    usuarioDao = UsuarioDAO(db)

    usuarioDao.edita_senha(id, attr['senha'])
    return get_ok(response_messages.ENTIDADE_EDITADA('senha')), 200

def recuperar_senha():
    try:
        attr = get_request_form_data_attributes(['email'])
        attr['email'] = attr['email'].lower()
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    if not attr['email']:
        return get_erro(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400
    
    db = get_db()
    try:
        usuarioDao = UsuarioDAO(db)

        usuario = usuarioDao.get_usuario_email(attr['email'])
        if not usuario:
            return get_erro(response_messages.NAO_ENCONTRADO('Email')), 404

        novaSenha = generate_random_password()
        codUsuario = int(usuario['codUsuario'])
        
        mailer.send_email(
            usuario['email'],
            mailer.generate_message_html(
                'Recuperação de senha',
                usuario['email'], 
                '''
                    <h2>Sua senha foi redefinida.</h2>

                    <p>Olá, {0}.</p>

                    <p>A senha do usuário <b>{1}</b> foi redefinida para:</p>

                    <h3><b>{2}</b></h3>
                '''.format(usuario['nome'], usuario['nomeUsuario'], novaSenha)
            )
        )
        
        usuarioDao.edita_senha(codUsuario, novaSenha)

        return get_ok(response_messages.EMAIL_ENVIADO_SENHA_NOVA()), 200
    except SMTPAuthenticationError as se:
        db.rollback()
        return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL())
    except Exception as ex:
        db.rollback()
        return get_erro(ex.__str__())
