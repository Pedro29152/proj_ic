import jwt
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
        user  = ''
        senha = ''
        try:
            user = request.form['username']
            senha = request.form['password']
        except BadRequestKeyError:
            return get_erro(
                'A requisicao deve conter os campos "username" e "password" em seu corpo para poder ser reconhecida'
            )

        usr = usuario_dao.verifica_usr(user, senha)
        if usr:
            extDt = datetime.now() + timedelta(hours=1)
            extDt = extDt.__str__()
            token = jwt.encode({
                "username": usr['nomeUsuario'], 
                'tipoUsuario': str(usr['tipoUsuario']), 
                'ext': extDt
            },
                current_app.config['SECRET_KEY'])

            ret = get_ok("Usuario logado com sucesso")
            ret['token'] = token.decode('utf-8')
            return ret
        return get_erro('Ususario ou senha incorretos, tente novamente')

class CadastroUsuarioResource(Resource):
    @admin_token_required
    def post(self):
        try:
            user = request.form['username']
            senha = request.form['password']
            tipoUsuario = int(request.form['tipoUsuario'])
            nome = request.form['nome']
            email = request.form['email']
        except BadRequestKeyError:
            return get_erro(
                'A requisicao deve possuir os campos "username", "tipoUsuario", "email", "nome" e "password" em seu corpo'
            )
        except ValueError:
            return get_erro(
                'O campo "tipoUsuario" deve ser do tipo inteiro'
            )

        if not (user and tipoUsuario and senha and email and nome):
            return get_falha('Os campos enviados nao podem estar vazios')
        if not (tipoUsuario - 1) in range(TiposUsuario.Administrador.value):
            return get_falha('O tipo de usuario enviado é invalido')

        if usuario_dao.add_usr(user, senha, tipoUsuario, nome, email):
            return get_ok(
                'Usuario cadastrado com sucesso'
            )
        return get_erro('O nome de usuario "{}" ja esta sendo utilizado'.format(user))

class CadastroAlunoResource(Resource):
    @professor_token_required
    def post(self):
        try:
            user = request.form['username']
            senha = request.form['password']
            nome = request.form['nome']
            email = request.form['email']
        except BadRequestKeyError:
            return get_erro(
                'A requisicao deve possuir os campos "username", "email", "nome" e "password" em seu corpo'
            )

        if not (user and senha and email and nome):
            return get_falha('Os campos enviados nao podem estar vazios')
        
        if usuario_dao.add_usr(user, senha, 1, nome, email):
            return get_ok(
                'Usuario cadastrado com sucesso'
            )
        return get_erro('O nome de usuario "{}" ja esta sendo utilizado'.format(user))

class CountUsuariosResource(Resource):
    @secretaria_token_required
    def get(self):
        count = usuario_dao.get_count()
        return get_count(count)

class DeletaUsuarioResource(Resource):
    @user_admin_token_required
    def delete(self, id, is_user):
        if is_user:
            return get_falha('Voce nao pode deletar o proprio usuario')
        if not util.is_cod_valido(id):
            return get_erro('O valor enviado deve ser do tipo inteiro')
        id = int(id)
        usuario_dao.deleta_usuario(id)
        return get_ok('Usuario deletado com sucesso')

class BuscaUsuariosResource(Resource):
    @admin_token_required
    def get(self):
        nome = request.args.get('nomeUsuario')

        if nome:
            ret = usuario_dao.busca_usuarios_nome_like(nome)
        else:
            ret = usuario_dao.busca_usuarios()

        return get_data(ret)

class GetUsuarioResource(Resource):
    @user_admin_token_required
    def get(self, id, is_user):
        if not util.is_cod_valido(id):
            return get_erro('O valor enviado deve ser do tipo inteiro')
        codUsuario = int(id)

        ret = usuario_dao.get_usuario(codUsuario)
        if ret:
            return get_data(ret)
        return get_falha('Usuario requisitado nao existe')

class EditarUsuarioResource(Resource):
    @user_admin_token_required
    def put(self, id, is_user):
        if not util.is_cod_valido(id):
            return get_erro('O valor enviado deve ser do tipo inteiro')

        try:
            nomeUsuario = request.form['nomeUsuario']
            nome = request.form['nome']
        except BadRequestKeyError:
            return get_erro('A requsicao deve conter o campo "nome" e "nomeUsuario" em seu corpo')

        codUsuario = int(id)
        usr = usuario_dao.get_usuario(codUsuario)

        if usr:
            if nomeUsuario and nome:
                usuario_dao.edita_usuario(codUsuario, nomeUsuario, nome)
                return get_ok('Usuario editado com sucesso')
            return get_falha('Os campos enviados nao podem ser vazios')
        return get_falha('O codigo enviado nao esta relacionado a nenhum usuario')

class MudarSenhaUsuarioResource(Resource):
    @user_admin_token_required
    def put(self, id):
        if not util.is_cod_valido(id):
            return get_erro('O valor enviado deve ser do tipo inteiro')
        codUsuario = int(id)

        try:
            senha = request.form['senha']
        except BadRequestKeyError:
            return get_erro('A requisicao deve possuir o campo "senha" em seu corpo')

        usuario_dao.edita_senha(codUsuario, senha)
        return get_ok('A senha foi alterada com sucesso')

