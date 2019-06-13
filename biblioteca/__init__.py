from flask import Flask
from flask_admin import Admin 
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/files')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#mysql://127.0.0.1:3306/java?useTimezone=true&serverTimezone=UTC
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://127.0.0.1:3306/proj_ic?useTimezone=true&serverTimezone=UTC'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.jinja_options = Flask.jinja_options.copy()
app.jinja_options.update(dict(
    variable_start_string='[[',  
    variable_end_string=']]',
))

from biblioteca import routes
