from biblioteca.controllers import usuario_control
from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from flask import request, make_response, jsonify, Blueprint
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
    
    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
        
@USUARIOS_ROUTER.route("/usuarios/logout", methods=['GET', 'POST'])
@login_reqired
def logout_usuario():
    ret = usuario_control.logout_url()

    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@USUARIOS_ROUTER.route("/usuarios/cadastrar", methods=["POST"])
@admin_reqired
def cadastrar_usuario():
    ret = usuario_control.cadastro_usr(request)
    
    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@USUARIOS_ROUTER.route("/usuarios/buscar", methods=["GET"])
@admin_reqired
def buscar_usuario():
    ret = usuario_control.buscar_usuario(request)
    
    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@USUARIOS_ROUTER.route('/usuarios/count', methods=['GET'])
def usuarios_count():
    ret = usuario_control.get_count()
    
    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res