from flask import session, flash, redirect,url_for
from biblioteca.models.dao import usuario_dao, gerenciadores_dao, usuario_dao

def login_url(request):
    user = request.form['username']
    senha = request.form['password']
    if usuario_dao.verifica_usr(user, senha):
        session['username'] = user
        session['logged_in'] = True
        session['nivel_acesso'] = usuario_dao.busca_nivel_acesso(user)
    else:
        flash("Ususario ou senha incorretos, tente novamente")
        return redirect(url_for('login_url'))
 
    return redirect(url_for('index'))

def logout_url():
    session.clear()

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
            flash("Usuario cadastrado com sucesso")
            return redirect(url_for('cadastro'))

        flash("Senhas não coincidem")
        return redirect(url_for('cadastro'))