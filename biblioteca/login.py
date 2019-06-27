from flask import session, flash, redirect,url_for
from biblioteca.cls.usuario import usuario_bd
from biblioteca.cls.gerenciador import gerenciador_bd

def login_url(request):
    user = request.form['username']
    senha = request.form['password']
    if usuario_bd.verifica_usr(user, senha):
        session['username'] = user
        session['logged_in'] = True
    else:
        flash("Ususario ou senha incorretos, tente novamente")
        return redirect(url_for('login_url'))
 
    return redirect(request.url)

def logout_url():
    session.clear()

def cadastro_usr(request):
        user = request.form['username']
        senha = request.form['password']
        tipoUsuario = request.form['tipoUsuario']
        gerenciador = request.form['gerenciador']
        rsenha = request.form['r_password']

        codGer = gerenciador_bd.get_codGer(gerenciador)

        if(tipoUsuario == "Usuario"):
            tipoUsuario = 1
        if(tipoUsuario == "Diretor"):
            tipoUsuario = 2
        if(tipoUsuario == "Admin"):
            tipoUsuario = 3
            
        if senha == rsenha:
            usuario_bd.add_usr(user, senha,tipoUsuario,codGer)
            flash("Usuario cadastrado com sucesso")
            return redirect(url_for('cadastro'))

        flash("Senhas não coincidem")
        return redirect(url_for('cadastro'))