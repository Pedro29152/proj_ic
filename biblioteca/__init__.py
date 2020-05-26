from flask import Flask, render_template
from config import config

# Realize a importação da função que configura a api
from .api import configure_api

def create_app(config_name):
    app = Flask('biblioteca-api')
    
    app.config.from_object(config[config_name])
    
    app.jinja_options = Flask.jinja_options.copy()
    app.jinja_options.update(dict(
        variable_start_string='[[',  
        variable_end_string=']]',
    ))
    
    # executa a chamada da função de configuração
    configure_api(app)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template("index.html")

    return app