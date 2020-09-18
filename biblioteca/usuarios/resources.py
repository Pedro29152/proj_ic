import jwt
from flask import jsonify
from flask_restful import Resource, request, current_app
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError, IntegrityError
from datetime import datetime, timedelta

from biblioteca import mailer, response_messages
from biblioteca.orientador.schemas import Orientadores
from biblioteca.orientador import orientadores_dao
from biblioteca.autor import autores_dao
from biblioteca.curso import cursos_dao
from biblioteca.projeto import projetos_dao
from biblioteca.extensions import (
    secretaria_token_required,
    admin_token_required,
    user_admin_token_required,
    professor_token_required,
    is_valid_email,
    is_valid_username,
    admin_is_user_token_required,
    secretaria_token_required_user_info,
    secretaria_token_required_is_user,
    coordenador_secretaria_token_required,
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
from . import usuario_dao, usuario_orientado_dao
from . import util

class LoginResource(Resource):
    def post(self):
        res, cod = login()
        return get_response_code(res, cod)

class UsuarioIdResource(Resource):
    @user_admin_token_required
    def get(self, id, is_user, is_admin):
        res, cod = get_usuario(id)
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
    @coordenador_secretaria_token_required
    def put(self, id, user_info):
        res, cod = altera_orientador_aluno(id, user_info)
        return get_response_code(res, cod)

class CountUsuariosResource(Resource):
    @secretaria_token_required
    def get(self):
        count = usuario_dao.get_count()
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
    user  = ''
    senha = ''
    try:
        user = request.form['username']
        senha = request.form['password']
    except BadRequestKeyError:
        return get_erro(
            response_messages.CAMPOS_OBRIGATORIOS.format('"username" e "password"')
        ), 400

    usr = usuario_dao.verifica_usr(user, senha)
    if usr:
        extDt = datetime.now() + timedelta(hours=1)
        extDt = extDt.__str__()
        token_data = {
            'username': usr['nomeUsuario'], 
            'tipoUsuario': str(usr['tipoUsuario']),
            'nome': usr['nome'],
            'ext': extDt
        }

        token = jwt.encode(token_data,
            current_app.config['SECRET_KEY'])

        ret = get_ok("Usuario logado com sucesso")
        ret['token'] = token.decode('utf-8')
        ret['data'] = token_data
        return ret, 200
    return get_erro(response_messages.USUARIO_SENHA_INCORRETOS), 401

def cadastro_usuario():
    try:
        user = request.form['username']
        senha = request.form['password']
        tipoUsuario = int(request.form['tipoUsuario'])
        nome = request.form['nome']
        email = request.form['email']
    except BadRequestKeyError:
        return get_erro(
            response_messages.CAMPOS_OBRIGATORIOS.format('"username", "tipoUsuario", "email", "nome" e "password"')
        ), 400
    except ValueError:
        return get_erro(
            response_messages.VALIDACAO_DEVE.format('tipoUsuario', 'ser do tipo inteiro')
        ), 400

    if not (user and tipoUsuario and senha and email and nome):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO), 400
    if not is_valid_email(email):
        return get_erro(response_messages.VALIDACAO_DEVE.format('email',  'ser um email valido')), 400
    if not is_valid_username(user):
        return get_erro(response_messages.VALIDACAO_DEVE.format('username', 'ser um nome de usuario valido')), 400
    if not (tipoUsuario - 1) in range(TiposUsuario.Coordenador.value):
        return get_falha(response_messages.ATRIBUTO_INVALIDO.format('tipoUsuario')), 400
    if tipoUsuario == TiposUsuario.Aluno.value:
        return get_falha(response_messages.NOVA_ROTA_CADASTRO.format('aluno', '"/api/usuarios/cadastro/aluno"')), 400
    if tipoUsuario == TiposUsuario.Professor.value:
        return get_falha(response_messages.NOVA_ROTA_CADASTRO.format('orientador' '"/api/usuarios/cadastro/orientador/novo"')), 400
    if tipoUsuario == TiposUsuario.Coordenador.value:
        return get_falha(response_messages.NOVA_ROTA_CADASTRO.format('coordenador', '"/api/usuarios/cadastro/coordenador"')), 400

    if usuario_dao.add_usr(user, senha, tipoUsuario, nome, email):
        return get_ok(
            response_messages.ENTIDADE_GRAVADA.format('Usuario')
        ), 201
    return get_erro(response_messages.ERRO_INTEGRIDADE.format('Nome de usuario ou email')), 400

def cadastro_professor(existente=True):
    try:
        nome = request.form['nome']
        email = request.form['email']
        if existente:
            codOrientador = request.form['codOrientador']
            if not (email and nome and codOrientador):
                return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO), 400
        else:
            currLattes = request.form['currLattes']
            ra = request.form['ra']
            if not (email and nome and currLattes and ra):
                return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO), 400
    except BadRequestKeyError:
        return get_erro(
            response_messages.CAMPOS_OBRIGATORIOS.format('{}, "nome" e "email" em seu corpo'.format('"codOrientador", ' if existente else '"currLattes", "ra", '))
        ), 400
    
    
    if not is_valid_email(email):
        return get_erro(response_messages.VALIDACAO_DEVE.format('email', 'ser um email valido')), 400

    if not existente:
        try:
            orientador = Orientadores(
                nomeOrientador=nome,
                raOrientador=ra,
                email=email,
                currLattes=currLattes
            )
            orientador.grava_orientador()

            codOrientador = orientador.codOrientador
        except AttributeError as ex:
            return get_erro(ex.__str__()), 400
        except DataError:
            return get_erro(response_messages.VALIDACAO_DEVE.format('ra', 'conter no máximo 13 caracteres')), 400
        except IntegrityError:
            return get_erro(response_messages.ERRO_INTEGRIDADE.format('Email ou ra')), 400
    else:
        if not orientadores_dao.exists(codOrientador):
            return get_erro(response_messages.NAO_ENCONTRADO.format('Orientador')), 400
            
    orientador = orientadores_dao.get_orientador_codigo(codOrientador, False)
    user = orientador['raOrientador']
    password = generate_random_password()
    if usuario_dao.add_orientador(user, password, nome, email, codOrientador):
        
        msg = mailer.generate_message_html(
            'BTA - Nova conta de Orientador',
            email,
            '''
                <h2>Você foi cadastrado no sistema BTA</h2>

                <p>Você foi cadastrado como um novo orientador do sistema BTA - Biblioteca de Trabalhos Acadêmicos.</p>
                <p>Veja abaixo os dados de login do seu usuário:</p>

                <p>Nome de usuário: <b>{0}</b></p>
                <p>Senha: <b>{1}</b></p>
            '''.format(user, password)
        )
        mailer.send_email(email, msg)

        return get_ok(
            response_messages.ENTIDADE_GRAVADA.format('Usuario')
        ), 201
    if not existente:
        orientadores_dao.deleta_orientador(codOrientador)
    return get_erro(response_messages.ERRO_INTEGRIDADE.format('Nome de usuario ou email')), 400

def cadastro_aluno(professor_user_info):
    try:
        nome = request.form['nome']
        email = request.form['email']
        ra = request.form['ra_aluno']
        codCurso = request.form['codCurso']
    except BadRequestKeyError:
        return get_erro(
            response_messages.CAMPOS_OBRIGATORIOS.format('"email", "nome", "ra_aluno" e "codCurso"')
        ), 400

    if not (email and nome and ra and codCurso):
        return get_falha(response_messages.PREENCHIMENTO_OBRIGATORIO), 400
    if not is_valid_email(email):
        return get_erro(response_messages.VALIDACAO_DEVE.format('email', 'ser um email valido')), 400
    
    curso = cursos_dao.get_curso_codCurso(codCurso, False)
    if not curso:
        return get_falha(response_messages.NAO_ENCONTRADO.format('Curso')), 400

    autor = autores_dao.get_autor_ra(ra)
    if not autor:
        try:
            autor = autores_dao.cadastra_autor(nome, email, ra)
            if not autor:
                return get_erro(response_messages.ERRO_INTEGRIDADE.format('Autor')), 400
        except DataError:
            return get_erro(response_messages.VALIDACAO_DEVE.format('ra', 'ter no maximo 13 caracteres')), 400
    orientador = orientadores_dao.get_orientador_codUsuario(professor_user_info['codUsuario'])
    if not orientador:
        return get_erro(response_messages.USUARIO_NAO_RELACIONADO), 400
    
    password = generate_random_password()
    if usuario_dao.add_aluno(ra, password, nome, email, autor['codAutor'], orientador['codOrientador'], codCurso):

        msg = mailer.generate_message_html(
            'BTA - Nova conta de Autor',
            email,
            '''
                <h2>Você foi cadastrado no sistema BTA</h2>

                <p>Você foi cadastrado como um novo autor do sistema BTA - Biblioteca de Trabalhos Acadêmicos.</p>
                <p>Veja abaixo os dados de login do seu usuário:</p>

                <p>Nome de usuário: <b>{0}</b></p>
                <p>Senha: <b>{1}</b></p>
            '''.format(ra, password)
        )
        mailer.send_email(email, msg)

        return get_ok(
            response_messages.ENTIDADE_GRAVADA.format('Usuario')
        ), 201
    return get_erro(response_messages.ERRO_INTEGRIDADE.format('Nome de usuario ou email')), 400

def desativa_usuario(codUsuario, is_user):
    if is_user:
        return get_erro(response_messages.SEM_PERMICAO.format('desativar o próprio usuário')), 400
        
    usr = usuario_dao.get_usuario(codUsuario)
    if usr:
        if usr['tipoUsuario'] == TiposUsuario.Coordenador.value:
            return get_erro(response_messages.SEM_PERMICAO.format('apagar um usuario do tipo Coordenador')), 400
        usuario_dao.desativa_usuario(codUsuario)
        return get_ok(response_messages.ENTIDADE_DESATIVADA.format('Usuario')), 200
    return get_erro(response_messages.NAO_ENCONTRADO.format('Usuário')), 404

def ativa_usuario(codUsuario, is_user):
    if is_user:
        return get_erro(response_messages.SEM_PERMICAO.format('ativar o próprio usuário')), 400

    usr = usuario_dao.get_usuario_inativo(codUsuario)
    if usr:
        usuario_dao.ativa_usuario(codUsuario)
        return get_ok(response_messages.ENTIDADE_ATIVADA.format('Usuario')), 200
    return get_erro(response_messages.NAO_ENCONTRADO.format('Usuário')), 404

def deleta_usuario(codUsuario, is_user):
    if is_user:
        return get_falha(response_messages.SEM_PERMICAO.format('deletar o próprio usuário')), 400
    
    usr = usuario_dao.get_usuario(codUsuario)
    if usr:
        if usr['tipoUsuario'] == TiposUsuario.Coordenador.value:
            return get_erro(response_messages.SEM_PERMICAO.format('apagar um usuario do tipo Coordenador')), 400
        usuario_dao.deleta_usuario(codUsuario)
        return get_ok(response_messages.ENTIDADE_DELETADA.format('Usuario')), 200
    return get_erro(response_messages.NAO_ENCONTRADO.format('Usuário')), 404

def busca_usuarios():
    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuario_dao.busca_usuarios_nome_like(nome)
    else:
        ret = usuario_dao.busca_usuarios()
    
    if ret:
        return get_data(ret), 200
    return None, 204

def buscar_usuarios_orientados(user_info):
    orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
    if not orientador:
        return get_erro(response_messages.USUARIO_NAO_RELACIONADO), 400

    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuario_dao.busca_usuarios_orientados_nome_like(nome, orientador['codOrientador'])
    else:
        ret = usuario_dao.busca_usuarios_orientados(orientador['codOrientador'])
    
    if ret:
        return get_data(ret), 200
    return None, 204

def busca_usuarios_inativos():
    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuario_dao.busca_usuarios_inativos_nome_like(nome)
    else:
        ret = usuario_dao.busca_usuarios_inativos()
    
    if ret:
        return get_data(ret), 200
    return None, 204

def busca_usuarios_secretaria_adm(user_info):
    nome = request.args.get('nomeUsuario')

    if user_info['tipoUsuario'] == TiposUsuario.Secretaria.value:
        usuarios = usuario_dao.buscar_usuarios_secretaria(nome)
        if usuarios:
            return get_data(usuarios), 200
        return None, 204
        
    if user_info['tipoUsuario'] == TiposUsuario.Administrador.value:
        usuarios = usuario_dao.buscar_usuarios_admin(nome)
        if usuarios:
            return get_data(usuarios), 200
        return None, 204

def get_usuario(id):
    codUsuario = int(id)

    ret = usuario_dao.get_usuario(codUsuario)
    if ret:
        return get_data(ret), 200
    return get_falha(response_messages.NAO_ENCONTRADO.format('Usuário')), 404

def edita_usuario(codUsuario, is_admin, is_user):
    try:
        nome = request.form['nome']
        email = request.form['email']
        tipoUsuario = None
        nomeUsuario = None
        if is_admin and not is_user:
            nomeUsuario = request.form['nomeUsuario']
            tipoUsuario = request.form['tipoUsuario']
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS.format('"nome", "email", "tipoUsuario" e "nomeUsuario"')), 400

    usr = usuario_dao.get_usuario(codUsuario)

    if usr:
        if not is_admin:
            if usr['tipoUsuario'] == TiposUsuario.Administrador.value:
                return get_erro(response_messages.SEM_PERMICAO.format('alterar um administrador sem ser um administrador')), 400

        if nomeUsuario:
            if not is_valid_username(nomeUsuario):
                return get_erro(response_messages.VALIDACAO_DEVE.format('nomeUsuario', 'ser um nome de usuario válido')), 400
            usr['nomeUsuario'] = nomeUsuario
        if nome: 
            usr['nome'] = nome
        if email: 
            if not is_valid_email(email):
                return get_erro(response_messages.VALIDACAO_DEVE.format('email', 'ser um email valido')), 400
            usr['email'] = email
        if tipoUsuario: 
            usr['tipoUsuario'] = tipoUsuario

        usuario_dao.edita_usuario(usr)

        return get_ok(response_messages.ENTIDADE_EDITADA.format('Usuario')), 200
    return get_falha(response_messages.NAO_ENCONTRADO.format('Usuário')), 404

def altera_orientador_aluno(codProjeto, user_info):
    proj = projetos_dao.get_projeto_novo(codProjeto, True)
    if not proj:
        return get_erro(response_messages.NAO_ENCONTRADO.format('Trabalho')), 404
    curso = cursos_dao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
    if not curso:
        return get_erro(response_messages.SEM_PERMICAO.format('ter acesso a esta ação')), 400

    if not proj['curso']['abreviacao'] == curso['abreviacao']:
        return get_erro(response_messages.SEM_PERMICAO.format('ter acesso a esta ação')), 400

    try:
        codOrientador = request.form['codOrientador']
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS.format('"codOrientador"')), 400

    if not util.is_cod_valido(codOrientador):
        return get_erro(response_messages.VALIDACAO_DEVE.format('codOrientador', 'ser um numero inteiro')), 400

    orientador = orientadores_dao.get_orientador_codigo(codOrientador, False)
    if not orientador:
        return get_erro(response_messages.NAO_ENCONTRADO.format('Orientador')), 400
    if not orientador['codUsuario']:
        return get_erro(response_messages.NAO_ENCONTRADO.format('Orientador')), 400
    
    usuario_orientado_dao.edita_orientador_projeto_novo(codProjeto, orientador['codOrientador'])
    return None, 204

def mudar_senha(id):
    try:
        senha = request.form['senha']
    except BadRequestKeyError:
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS.format('"senha"')), 400

    usuario_dao.edita_senha(id, senha)
    return get_ok(response_messages.ENTIDADE_EDITADA.format('senha')), 200

def recuperar_senha():
    try:
        email = request.form['email']
        email = email.lower()
    except BadRequestKeyError: 
        return get_erro(response_messages.CAMPOS_OBRIGATORIOS.format('"email"')), 400

    if not email:
        return get_erro(response_messages.PREENCHIMENTO_OBRIGATORIO), 400
    
    usuario = usuario_dao.get_usuario_email(email)
    if not usuario:
        return get_erro(response_messages.NAO_ENCONTRADO.format('Email')), 404

    novaSenha = generate_random_password()
    codUsuario = int(usuario['codUsuario'])
    usuario_dao.edita_senha(codUsuario, novaSenha)

    mailer.send_email(
        usuario['email'],
        mailer.generate_message_html(
            'Recuperação de senha - BTA',
            usuario['email'], 
            '''
                <h2>Sua senha foi redefinida.</h2>

                <p>Olá, {0}.</p>

                <p>A senha do usuário <b>{1}</b> foi redefinida para:</p>

                <h3><b>{2}</b></h3>
            '''.format(usuario['nome'], usuario['nomeUsuario'], novaSenha)
        )
    )

    return get_ok(response_messages.EMAIL_ENVIADO_SENHA_NOVA), 200
