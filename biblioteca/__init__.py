from flask import Flask, render_template, request, session, jsonify, make_response
from flask_cors import CORS
from werkzeug.exceptions import InternalServerError

from json import dumps
from datetime import datetime
from config import config

from .api import configure_api
from biblioteca.db import Db
from biblioteca.geral.logger_dao import LoggerDAO
from biblioteca.usuarios.usuario_dao import UsuarioDAO
from biblioteca.extensions import get_token_data
from biblioteca import response_messages

def create_app(config_name):
    app = Flask('biblioteca-api')
    
    app.config.from_object(config[config_name])
    
    app.jinja_options = Flask.jinja_options.copy()
    app.jinja_options.update(dict(
        variable_start_string='[[',  
        variable_end_string=']]',
    ))

    CORS(app)

    # executa a chamada da função de configuração
    configure_api(app)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template("index.html")

    @app.before_request
    def before():
        reqValues = {}
        if len(request.values) == 0:
            reqValues = None
        for key in request.values:
            if ('password' in key.lower()) or ('senha' in key.lower()) or ('email' in key.lower()):
                continue
            reqValues[key] = request.values[key]
        if not reqValues:
            reqValues = None

        with Db() as db:
            usuarioDao = UsuarioDAO(db)
            
            try:
                token_data = get_token_data()
                
                if request.method == 'GET':
                    raise Exception()
                
                current_user = usuarioDao.busca_usuarios_nome(token_data['username'])
                if not current_user:
                    raise Exception()
                

                session['log'] = True
                session['user'] = current_user
                session['url'] = request.base_url
                session['method'] = request.method
                session['enderecoIp'] = request.remote_addr
                session['reqDateTime'] = datetime.now()
                session['requestValues'] = dumps(reqValues, separators=(',',':')) if reqValues else None
            except:
                pass

    @app.after_request
    def after(response):
        with Db() as db:
            loggerDao = LoggerDAO(db)

            try:
                if session['log']:
                    status = response.status_code
                    resp = response.data.decode('utf-8')
                    loggerDao.logger_gravar(
                        session['url'],
                        session['reqDateTime'],
                        session['method'],
                        status,
                        session['user']['codUsuario'],
                        session['enderecoIp'],
                        session['requestValues'],
                        resp
                    )
                    session.clear()
            except:
                pass

            return response

    @app.errorhandler(InternalServerError)
    def internal_error(exception):
        with Db() as db:
            loggerDao = LoggerDAO(db)
                
            if hasattr(exception, 'original_exception'):
                ex = str(exception.original_exception)
            else:
                ex = str(exception)
            
            try:
                if session['log']:
                    status = 500
                    loggerDao.logger_gravar(
                        session['url'],
                        session['reqDateTime'],
                        session['method'],
                        status,
                        codUsuario= session['user']['codUsuario'],
                        ip_address= session['enderecoIp'],
                        request_data= session['requestValues'],
                        info= ex
                    )
                    session.clear()
            except:
                pass

            return make_response(response_messages.ERRO_INESPERADO(), 500)
    
    return app