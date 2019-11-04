from flask import Flask
from biblioteca.routers.cursos_blueprint import CURSOS_ROUTER
from biblioteca.routers.usuarios_blueprint import USUARIOS_ROUTER
from biblioteca.routers.gerenciadores_blueprint import GERENCIADORES_ROUTER
from biblioteca.routers.projetos_blueprint import PROJETOS_ROUTER
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/files')

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.jinja_options = Flask.jinja_options.copy()
app.jinja_options.update(dict(
    variable_start_string='[[',  
    variable_end_string=']]',
))

app.register_blueprint(CURSOS_ROUTER)
app.register_blueprint(USUARIOS_ROUTER)
app.register_blueprint(GERENCIADORES_ROUTER)
app.register_blueprint(PROJETOS_ROUTER)

from biblioteca import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0')
