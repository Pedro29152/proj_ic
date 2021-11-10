from flask import Flask, render_template, request, session, g
from flask_cors import CORS
from werkzeug.exceptions import MethodNotAllowed, NotFound

import traceback
from json import dumps
from datetime import datetime
from config import config

from .api import configure_api
from biblioteca.db import get_db
from biblioteca.geral.logger_dao import LoggerDAO
from biblioteca.usuarios.usuario_dao import UsuarioDAO
from biblioteca.extensions import get_token_data
from biblioteca import response_messages, responses

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
    @app.route('/')
    def catch_all():
        import setup
        return render_template("index.html", versao=setup.__version__, descricao=setup.__description__, descricao_longa=setup.__long_description__)

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
        db = get_db()
        usuarioDao = UsuarioDAO(db)
        
        try:
            if request.path == '/api/auth/login':
                current_user = {'codUsuario': None}
            else:
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
        db = get_db()
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

    @app.errorhandler(Exception)
    def internal_error(exception):
        if isinstance(exception, MethodNotAllowed):
            return responses.get_method_not_allowed()

        if isinstance(exception, NotFound):
            return responses.get_not_found()
    
        db = get_db()
        loggerDao = LoggerDAO(db)
            
        ex = traceback.format_exc()
        
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
        except Exception as ex:
            traceback.print_exc()

        traceback.print_exc()
        return responses.get_response_code(response_messages.ERRO_INESPERADO(), 500)
    
    @app.teardown_appcontext
    def teardown_db(exception):
        db_rm = g.pop('db', None)

        if db_rm is not None:
            db_rm.close()

    return app
