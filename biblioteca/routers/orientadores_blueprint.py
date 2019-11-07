from biblioteca.controllers import orientadores_control
from biblioteca.util import util
from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from flask import request, make_response, jsonify, Blueprint

ORIENTADORES_ROUTER = Blueprint('orientadores_router', __name__)


@ORIENTADORES_ROUTER.route('/orientadores/cadastrar', methods=['POST'])
@admin_reqired
def cadastra_orientador():
    status = orientadores_control.grava_orientador(request)
    
    return util.response_ext(jsonify(status))

@ORIENTADORES_ROUTER.route('/orientadores/buscar', methods=['GET'])
@login_reqired
def busca_orientador():
    status = orientadores_control.busca_orientador(request)
    
    return util.response_ext(jsonify(status))

@ORIENTADORES_ROUTER.route('/orientadores/count', methods=['GET'])
@login_reqired
def orientadores_count():
    ret = orientadores_control.get_count()
    
    return util.response_ext(jsonify(ret))
