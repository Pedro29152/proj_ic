from biblioteca.controllers import curso_control
from biblioteca.util import util
from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from flask import make_response, jsonify, request, Blueprint

CURSOS_ROUTER = Blueprint('cursos_router', __name__)

@CURSOS_ROUTER.route("/cursos/cadastrar", methods=['POST'])
@admin_reqired
def cadastra_curso():
    status = curso_control.grava_curso(request)

    return util.response_ext(jsonify(status))

@CURSOS_ROUTER.route('/cursos/ativar/<path:codCurso>', methods=['POST'])
@admin_reqired
def ativa_curso(codCurso):
    status = curso_control.ativa_curso(codCurso)
    
    return util.response_ext(jsonify(status))

@CURSOS_ROUTER.route('/cursos/desativar/<path:codCurso>', methods=['POST'])
@admin_reqired
def desativa_curso(codCurso):
    status = curso_control.desativa_curso(codCurso)
    
    return util.response_ext(jsonify(status))

@CURSOS_ROUTER.route("/cursos/buscar", methods=['GET'])
@login_reqired
def buscar_curso():
    status = curso_control.buscar_curso()

    return util.response_ext(jsonify(status))

@CURSOS_ROUTER.route("/cursos/buscar/inativos", methods=['GET'])
@admin_reqired
def buscar_curso_inativo():
    status = curso_control.buscar_curso_inativo()

    return util.response_ext(jsonify(status))

@CURSOS_ROUTER.route('/cursos/count', methods=['GET'])
@login_reqired
def cursos_count():
    ret = curso_control.get_count()
    
    return util.response_ext(jsonify(ret))