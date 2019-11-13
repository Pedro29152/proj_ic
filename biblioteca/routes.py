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