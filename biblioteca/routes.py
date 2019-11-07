from biblioteca                 import app
from flask                      import render_template
from functools                  import wraps
from biblioteca.models.dao      import projetos_dao
from biblioteca.controllers     import usuario_control
#import simplejson

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

#rota padrao de caminhos nao definidos
@app.errorhandler(404)
def page_not_found(e):
    return render_template("err404.html")

#rota padrao para caminhos nao autorizados
@app.errorhandler(405)
def page_not_allowed(e):
    return render_template("err405.html")