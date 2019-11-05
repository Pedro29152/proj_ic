from biblioteca                 import app
from flask                      import render_template
from functools                  import wraps
from biblioteca.models.dao      import projetos_dao
from biblioteca.controllers     import usuario_control
#import simplejson

#define a rota principal
@app.route("/")
@app.route("/index")
def  index():
    #retorna a pagina
    return render_template("vue/index.html")

#define rota para consulta de projetos cadastrados
@app.route("/projetos/buscar", methods=["GET"])
def buscar():
    dados = projetos_dao.busca_projeto()
    
    return render_template("vue/busca.html",tgs = dados)

#rota padrao de caminhos nao definidos
@app.errorhandler(404)
def page_not_found(e):
    return render_template("err404.html")

#rota padrao para caminhos nao autorizados
@app.errorhandler(405)
def page_not_allowed(e):
    return render_template("err405.html")