from biblioteca.controllers import gerenciadores_control
from biblioteca.util import util
from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from flask import request, make_response, jsonify, Blueprint

GERENCIADORES_ROUTER = Blueprint('gerenciadores_router', __name__)

@GERENCIADORES_ROUTER.route('/gerenciadores/cadastrar', methods=['POST'])
@admin_reqired
def cadastro_gerenciadores():
    status = gerenciadores_control.grava_gerenciador(request)
    
    return util.response_ext(jsonify(status))

@GERENCIADORES_ROUTER.route('/gerenciadores/buscar', methods=['GET'])
@login_reqired
def buscar_gerenciadores():
    status = gerenciadores_control.busca_gerenciador(request)
    
    return util.response_ext(jsonify(status))

@GERENCIADORES_ROUTER.route('/gerenciadores/count', methods=['GET'])
@login_reqired
def gerenciadores_count():
    ret = gerenciadores_control.get_count()
    
    return util.response_ext(jsonify(ret))