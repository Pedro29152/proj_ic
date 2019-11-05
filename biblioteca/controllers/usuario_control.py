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
        rsenha = request.form['r_password']
    except BadRequestKeyError:
        return json_res.get_erro(
            'A requisicao deve possuir os campos "username", "tipoUsuario", "gerenciador", "password" e "r_password" em seu corpo'
        )

    #codGer = gerenciadores_dao.get_codGer_nomeGer(gerenciador)

    if(tipoUsuario == "Usuario"):
        tipoUsuario = 1
    if(tipoUsuario == "Diretor"):
        tipoUsuario = 2
    if(tipoUsuario == "Admin"):
        tipoUsuario = 3
        
    if senha == rsenha:
        usuario_dao.add_usr(user, senha,tipoUsuario,codGer)
        return json_res.get_ok(
            'Usuario cadastrado com sucesso'
        )

    return json_res.get_falha(
        'Senhas não coincidem'
    )

def buscar_usuario(req):
    nome = req.args.get('nomeUsuario')

    if nome:
        ret = usuario_dao.busca_usuarios_nome_like(nome)
    else:
        ret = usuario_dao.busca_usuarios()

    return json_res.get_data(ret)

def logado(s):
    if 'logged_in' in s:
        return True
    else:
        return False

def get_count(): 
    count = usuario_dao.get_count()
    return  json_res.get_count(count)