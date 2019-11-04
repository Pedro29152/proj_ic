from flask import session, flash, redirect,url_for
from biblioteca.models.dao import usuario_dao, gerenciadores_dao, usuario_dao
from werkzeug.exceptions import BadRequestKeyError

def tentar_login(request, next_page=''):
    user  = ''
    senha = ''
    try:
        user = request.form['username']
        senha = request.form['password']
    except BadRequestKeyError:
        return {
            'status':'erro',
            'message':'A requisicao deve conter os campos "username" e "password" em seu corpo para poder ser reconhecida'
        }
        
    if usuario_dao.verifica_usr(user, senha):
            session['username'] = user
            session['logged_in'] = True
            session['nivel_acesso'] = usuario_dao.busca_nivel_acesso(user)
            return {
                'status': 'OK',
                'message': 'Ususario logado com sucesso',
                'next_page' : next_page
            }
    else:
        return {
            'status':'erro',
            'message': 'Ususario ou senha incorretos, tente novamente'
        }

def logout_url():
    session.clear()
    return {
        'status': 'OK',
        'message': 'Usuario deslogado com sucesso'
    }

def cadastro_usr(request):
        user = request.form['username']
        senha = request.form['password']
        tipoUsuario = request.form['tipoUsuario']
        gerenciador = request.form['gerenciador']
        rsenha = request.form['r_password']

        codGer = gerenciadores_dao.get_codGer_nomeGer(gerenciador)

        if(tipoUsuario == "Usuario"):
            tipoUsuario = 1
        if(tipoUsuario == "Diretor"):
            tipoUsuario = 2
        if(tipoUsuario == "Admin"):
            tipoUsuario = 3
            
        if senha == rsenha:
            usuario_dao.add_usr(user, senha,tipoUsuario,codGer)
            return {
                'status': 'OK',
                'message': 'Usuario cadastrado com sucesso'
            }

        return {
            'status': 'falha',
            'message': 'Senhas não coincidem'
        }

def logado(s):
    if 'logged_in' in s:
        return True
    else:
        return False