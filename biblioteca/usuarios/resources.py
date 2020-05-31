import jwt
from flask import jsonify
from flask_restful import Resource, request, current_app
from werkzeug.exceptions import BadRequestKeyError
from datetime import datetime, timedelta

from biblioteca.extensions import (
    secretaria_token_required,
    admin_token_required,
    user_admin_token_required,
    professor_token_required,
    TiposUsuario
)
from biblioteca.responses import (
    get_falha,
    get_erro,
    get_ok,
    get_data,
    get_count
)
from . import usuario_dao
from . import util

class LoginResource(Resource):
    def post(self):
        res, cod = login()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class UsuarioIdResource(Resource):
    @user_admin_token_required
    def get(self, id, is_user, is_admin):
        res, cod = get_usuario(id)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

    @user_admin_token_required
    def delete(self, id, is_user, is_admin):
        res, cod = deleta_usuario(id, is_user)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

    @user_admin_token_required
    def put(self, id, is_user, is_admin):
        res, cod = edita_usuario(id, is_admin)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp

class CadastroUsuarioResource(Resource):
    @admin_token_required
    def post(self):
        res, cod = cadastro_usuario()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 
        
class CadastroAlunoResource(Resource):
    @professor_token_required
    def post(self):
        res, cod = cadastro_aluno()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class CountUsuariosResource(Resource):
    @secretaria_token_required
    def get(self):
        count = usuario_dao.get_count()
        return get_count(count)

class BuscaUsuariosResource(Resource):
    @admin_token_required
    def get(self):
        res, cod = busca_usuarios()
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 

class MudarSenhaUsuarioResource(Resource):
    @user_admin_token_required
    def put(self, id):
        res, cod = mudar_senha(id)
        
        resp = jsonify(res)
        resp.status_code = cod
        return resp 


def login():
    user  = ''
    senha = ''
    try:
        user = request.form['username']
        senha = request.form['password']
    except BadRequestKeyError:
        return get_erro(
            'A requisicao deve conter os campos "username" e "password" em seu corpo para poder ser reconhecida'
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
    return get_erro('Ususario ou senha incorretos, tente novamente'), 401

def cadastro_usuario():
    try:
        user = request.form['username']
        senha = request.form['password']
        tipoUsuario = int(request.form['tipoUsuario'])
        nome = request.form['nome']
        email = request.form['email']
    except BadRequestKeyError:
        return get_erro(
            'A requisicao deve possuir os campos "username", "tipoUsuario", "email", "nome" e "password" em seu corpo'
        ), 400
    except ValueError:
        return get_erro(
            'O campo "tipoUsuario" deve ser do tipo inteiro'
        ), 400

    if not (user and tipoUsuario and senha and email and nome):
        return get_falha('Os campos enviados nao podem estar vazios'), 400
    if not (tipoUsuario - 1) in range(TiposUsuario.Administrador.value):
        return get_falha('O tipo de usuario enviado é invalido'), 400

    if usuario_dao.add_usr(user, senha, tipoUsuario, nome, email):
        return get_ok(
            'Usuario cadastrado com sucesso'
        ), 201
    return get_erro('O nome de usuario "{}" ou o email "{}" ja estao sendo utilizados'.format(user, email)), 400

def cadastro_aluno():
    try:
        user = request.form['username']
        senha = request.form['password']
        nome = request.form['nome']
        email = request.form['email']
    except BadRequestKeyError:
        return get_erro(
            'A requisicao deve possuir os campos "username", "email", "nome" e "password" em seu corpo'
        ), 400

    if not (user and senha and email and nome):
        return get_falha('Os campos enviados nao podem estar vazios'), 400
    
    if usuario_dao.add_usr(user, senha, 1, nome, email):
        return get_ok(
            'Usuario cadastrado com sucesso'
        ), 201
    return get_erro('O nome de usuario "{}" ja esta sendo utilizado'.format(user)), 400

def deleta_usuario(id, is_user):
    if is_user:
        return get_falha('Voce nao pode deletar o proprio usuario'), 400
    if not util.is_cod_valido(id):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400
    id = int(id)
    usuario_dao.deleta_usuario(id)
    return get_ok('Usuario deletado com sucesso'), 200

def busca_usuarios():
    nome = request.args.get('nomeUsuario')

    if nome:
        ret = usuario_dao.busca_usuarios_nome_like(nome)
    else:
        ret = usuario_dao.busca_usuarios()
    
    if ret:
        return get_data(ret), 200
    return get_falha("Nenhum usuario retornado"), 204

def get_usuario(id):
    if not util.is_cod_valido(id):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400
    codUsuario = int(id)

    ret = usuario_dao.get_usuario(codUsuario)
    if ret:
        return get_data(ret), 200
    return get_falha('Usuario requisitado nao existe'), 404

def edita_usuario(codUsuario, is_admin):
    if not util.is_cod_valido(codUsuario):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400

    try:
        nomeUsuario = request.form['nomeUsuario']
        nome = request.form['nome']
        email = request.form['email']
        tipoUsuario = None
        if is_admin:
            tipoUsuario = request.form['tipoUsuario']
    except BadRequestKeyError:
        return get_erro('A requsicao deve conter o campo "nome", "email", "tipoUsuario" e "nomeUsuario" em seu corpo'), 400

    usr = usuario_dao.get_usuario(codUsuario)

    if usr:
        if nomeUsuario:
            usr['nomeUsuario'] = nomeUsuario
        if nome: 
            usr['nome'] = nome
        if email: 
            usr['email'] = email
        if tipoUsuario: 
            usr['tipoUsuario'] = tipoUsuario

        usuario_dao.edita_usuario(usr)

        return get_ok('Usuario editado com sucesso'), 200
    return get_falha('O codigo enviado nao esta relacionado a nenhum usuario'), 404

def mudar_senha(id):
    if not util.is_cod_valido(id):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400
    codUsuario = int(id)

    try:
        senha = request.form['senha']
    except BadRequestKeyError:
        return get_erro('A requisicao deve possuir o campo "senha" em seu corpo'), 400

    usuario_dao.edita_senha(codUsuario, senha)
    return get_ok('A senha foi alterada com sucesso'), 200
