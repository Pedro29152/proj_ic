from biblioteca.controllers import curso_control
from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from flask import make_response, jsonify, request, Blueprint

CURSOS_ROUTER = Blueprint('cursos_router', __name__)

@CURSOS_ROUTER.route("/cursos/cadastrar", methods=['POST'])
@admin_reqired
def cadastra_curso():
    status = curso_control.grava_curso(request)

    res = make_response(jsonify(status))    
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
    
@CURSOS_ROUTER.route("/cursos/buscar", methods=['GET'])
def buscar_curso():
    status = curso_control.buscar_curso()

    res = make_response(jsonify(status))    
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@CURSOS_ROUTER.route('/cursos/count', methods=['GET'])
def cursos_count():
    ret = curso_control.get_count()
    
    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res