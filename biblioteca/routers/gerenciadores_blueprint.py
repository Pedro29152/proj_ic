from biblioteca.controllers import gerenciadores_control
from flask import request, make_response, jsonify, Blueprint
from biblioteca.acesso.acessos import not_logged_in, login_reqired, admin_reqired

GERENCIADORES_ROUTER = Blueprint('gerenciadores_router', __name__)

@GERENCIADORES_ROUTER.route('/gerenciadores/cadastrar', methods=['POST'])
@admin_reqired
def cadastro_gerenciadores():
    status = gerenciadores_control.grava_gerenciador(request)
    
    res = make_response(jsonify(status))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@GERENCIADORES_ROUTER.route('/gerenciadores/buscar', methods=['GET'])
def buscar_gerenciadores():
    status = gerenciadores_control.busca_gerenciador(request)
    
    res = make_response(jsonify(status))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res