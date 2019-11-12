from biblioteca.controllers import usuario_control
from biblioteca.util import util
from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from flask import request, make_response, jsonify, Blueprint, session
from werkzeug.exceptions import BadRequestKeyError

USUARIOS_ROUTER = Blueprint('usuarios_router', __name__)

@USUARIOS_ROUTER.route("/usuarios/login", methods=['POST'])
@not_logged_in
def login_usuario():
    next_page = ''
    try:
        if request.form['next_page']:
            next_page = request.form['next_page']
    except BadRequestKeyError:
        next_page = '/index'

    ret = usuario_control.tentar_login(request, next_page)
    
    return util.response_ext(jsonify(ret))
        
@USUARIOS_ROUTER.route("/usuarios/logout", methods=['GET', 'POST'])
@login_reqired
def logout_usuario():
    ret = usuario_control.logout_url()

    return util.response_ext(jsonify(ret))

@USUARIOS_ROUTER.route("/usuarios/logged", methods=['GET', 'POST'])
def usuario_logado():
    ret = usuario_control.usuario_logado(session)

    return util.response_ext(jsonify(ret))

@USUARIOS_ROUTER.route("/usuarios/cadastrar", methods=["POST"])
@admin_reqired
def cadastrar_usuario():
    ret = usuario_control.cadastro_usr(request)
    
    return util.response_ext(jsonify(ret))

@USUARIOS_ROUTER.route("/usuarios/buscar", methods=["GET"])
@admin_reqired
def buscar_usuario():
    ret = usuario_control.buscar_usuario(request)
    
    return util.response_ext(jsonify(ret))

@USUARIOS_ROUTER.route('/usuarios/count', methods=['GET'])
@login_reqired
def usuarios_count():
    ret = usuario_control.get_count()
    
    return util.response_ext(jsonify(ret))