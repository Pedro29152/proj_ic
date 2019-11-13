from flask import session
from biblioteca.models.dao import usuario_dao, gerenciadores_dao, usuario_dao
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
        
    if usuario_dao.verifica_usr(user, senha):
            session['username'] = user
            session['logged_in'] = True
            session['nivel_acesso'] = usuario_dao.busca_nivel_acesso(user)

            ret = json_res.get_ok('Ususario logado com sucesso')
            ret['next_page'] = next_page
            return ret
    else:
        return json_res.get_erro('Ususario ou senha incorretos, tente novamente')

def logout_url():
    session.clear()
    return json_res.get_ok(
        'Usuario deslogado com sucesso'
    )

def cadastro_usr(request):
    try:
        user = request.form['username']
        tipoUsuario = request.form['tipoUsuario']
        codGer = request.form['gerenciador']
        senha = request.form['password']
    except BadRequestKeyError:
        return json_res.get_erro(
            'A requisicao deve possuir os campos "username", "tipoUsuario", "gerenciador" e "password" em seu corpo'
        )

    if not (user and tipoUsuario and codGer and senha):
        return json_res.get_falha('Os campos enviados nao podem estar vazios')

    if(tipoUsuario == "Usuario"):
        tipoUsuario = 1
    if(tipoUsuario == "Diretor"):
        tipoUsuario = 2
    if(tipoUsuario == "Admin"):
        tipoUsuario = 3
    
    if usuario_dao.add_usr(user, senha,tipoUsuario,codGer):
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
        return json_res.get_logado(session['nivel_acesso'], session['username'])
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

    ret = usuario_dao.get_usuario(codUsuario)
    if ret:
        return json_res.get_data(ret)
    return json_res.get_falha('Usuario requisitado nao existe')

def edita_usuario(codUsuario, req):
    if not __cod_valido(codUsuario):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    if usuario_dao.get_usuario(codUsuario):
        try:
            nomeUsuario = req.form['nomeUsuario']
            tipoUsuario = req.form['tipoUsuario']
        except BadRequestKeyError:
            return json_res.get_erro('A requsicao deve ter os campos "nomeUsuario" e "tipoUsuario" em seu corpo')
        if nomeUsuario and tipoUsuario:
            usuario_dao.edita_usuario(codUsuario, nomeUsuario, tipoUsuario)
            return json_res.get_ok('Projeto editado com sucesso')
        return json_res.get_falha('Os campos enviados nao devem ser vazios')
    return json_res.get_falha('O codigo enviado nao esta relacionado a nenhum usuario')

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