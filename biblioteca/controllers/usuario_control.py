from flask import session
from biblioteca.models.dao import usuario_dao, usuario_dao
from werkzeug.exceptions import BadRequestKeyError
from biblioteca.util import json_res

def tentar_login(request, next_page=''):
    user  = ''
    senha = ''
    try:
        user = request.form['username']
        senha = request.form['password']
    except BadRequestKeyError:
        return json_res.get_erro(
            'A requisicao deve conter os campos "username" e "password" em seu corpo para poder ser reconhecida'
        )
        
    usr = usuario_dao.verifica_usr(user, senha)
    if usr:
        session['username'] = user
        session['logged_in'] = True
        session['nivel_acesso'] = usr['tipoUsuario']
        session['nome'] = usr['nome']
        session['email'] = usr['email']

        ret = json_res.get_ok('Ususario logado com sucesso')
        ret['next_page'] = next_page
        return ret
    return json_res.get_erro('Ususario ou senha incorretos, tente novamente')

def logout_url():
    session.clear()
    return json_res.get_ok(
        'Usuario deslogado com sucesso'
    )

def cadastro_usr(request):
    try:
        user = request.form['username']
        senha = request.form['password']
        tipoUsuario = request.form['tipoUsuario']
        nome = request.form['nome']
        email = request.form['email']
    except BadRequestKeyError:
        return json_res.get_erro(
            'A requisicao deve possuir os campos "username", "tipoUsuario", "email", "nome" e "password" em seu corpo'
        )

    if not (user and tipoUsuario and senha):
        return json_res.get_falha('Os campos enviados nao podem estar vazios')
        
    if usuario_dao.add_usr(user, senha, tipoUsuario, nome, email):
        return json_res.get_ok(
            'Usuario cadastrado com sucesso'
        )

    return json_res.get_erro('O nome de usuario "{}" ja esta sendo utilizado'.format(user))
    
def buscar_usuario(req):
    nome = req.args.get('nomeUsuario')

    if nome:
        ret = usuario_dao.busca_usuarios_nome_like(nome)
    else:
        ret = usuario_dao.busca_usuarios()

    return json_res.get_data(ret)

def usuario_logado():
    if logado():
        return json_res.get_logado(session['nivel_acesso'], session['username'], session['nome'], session['email'])
    return json_res.get_deslogado()

def logado():
    if 'logged_in' in session:
        return True
    else:
        return False

def get_count(): 
    count = usuario_dao.get_count()
    return  json_res.get_count(count)

def get_usuario(codUsuario):
    if not __cod_valido(codUsuario):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    codUsuario = int(codUsuario)

    ret = usuario_dao.get_usuario(codUsuario)
    if ret:
        return json_res.get_data(ret)
    return json_res.get_falha('Usuario requisitado nao existe')

def edita_usuario(codUsuario, req):
    if not __cod_valido(codUsuario):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')

    try:
        nomeUsuario = req.form['nomeUsuario']
        nome = req.form['nome']
    except BadRequestKeyError:
        return json_res.get_erro('A requsicao deve conter o campo "nome" e "nomeUsuario" em seu corpo')

    codUsuario = int(codUsuario)
    usr = usuario_dao.get_usuario(codUsuario)

    if usr:
        if nomeUsuario and nome:
            usuario_dao.edita_usuario(codUsuario, nomeUsuario, nome)
            if usr['nomeUsuario'] == session['username']:
                session['username'] = nomeUsuario
                session['nome'] = nome
            return json_res.get_ok('Usuario editado com sucesso')
        return json_res.get_falha('Os campos enviados nao podem ser vazios')
    return json_res.get_falha('O codigo enviado nao esta relacionado a nenhum usuario')

def edita_senha(codUsuario, req):
    if not __cod_valido(codUsuario):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    codUsuario = int(codUsuario)

    try:
        senha = req.form['senha']
    except BadRequestKeyError:
        return json_res.get_erro('A requisicao deve possuir o campo "senha" em seu corpo')

    usuario_dao.edita_senha(codUsuario, senha)
    return json_res.get_ok('A senha foi alterada com sucesso')

def deleta_usuario(codUsuario):
    if not __cod_valido(codUsuario):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    codUsuario = int(codUsuario)
    if usuario_dao.is_usuario_logado(codUsuario, session['username']):
        return json_res.get_falha('Voce nao pode deletar o proprio usuario')

    usuario_dao.deleta_usuario(codUsuario)
    return json_res.get_ok('Usuario deletado com sucesso')


def is_user(codUsuario):
    if usuario_dao.is_user(codUsuario, session['username']):
        return True
    return False

def __cod_valido(codUsuario):
    try:
        int(codUsuario)
        return True
    except ValueError:
        return False