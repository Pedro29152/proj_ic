from biblioteca                 import app
from flask                      import render_template, redirect, flash, jsonify, session
from functools                  import wraps
from biblioteca.models.dao      import projetos_dao
from biblioteca.controllers     import usuario_control
#import simplejson

def login_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado(session):
            return f(*args, **kwargs)
        else:
            return jsonify( {
                'status': 'erro',
                'message': 'Voce precisa estar logado antes de acessar esta página'
            })

    return wrap

def admin_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado(session):
            if session['nivel_acesso'] > 1:
                return f(*args, **kwargs)
            else:
                return jsonify( {
                    'status': 'inacessivel',
                    'message': 'Seu nivel de acesso nao permite acesso a esta pagina'
                })
        else:
            return jsonify( {
                'status': 'erro',
                'message': 'Voce precisa estar logado antes de acessar esta página'
            })

    return wrap

def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            return jsonify({
                'status':'logado',
                'message':'Voce ja esta logado em uma conta, deslogue-se para poder acessar esta pagina'
            })
    
    return wrap

#define a rota principal
@app.route("/")
@app.route("/index/")
def  index():
    #retorna a pagina
    return render_template("vue/index.html")

#define rota para consulta de projetos cadastrados
@app.route("/projetos/buscar", methods=["GET"])
def buscar():
    dados = projetos_dao.busca_projeto()
    
    return render_template("vue/busca.html",tgs = dados)

import biblioteca.routers.projetos_router

import biblioteca.routers.usuarios_router

import biblioteca.routers.cursos_router

import biblioteca.routers.gerenciadores_router

#rota padrao de caminhos nao definidos
@app.errorhandler(404)
def page_not_found(e):
    return render_template("err404.html")

#rota padrao para caminhos nao autorizados
@app.errorhandler(405)
def page_not_allowed(e):
    return render_template("err405.html")