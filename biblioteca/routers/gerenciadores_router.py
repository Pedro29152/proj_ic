from biblioteca import app
from biblioteca.controllers import gerenciadores_control
from flask import request, make_response, jsonify

@app.route('/gerenciadores/cadastrar', methods=['POST'])
def cadastro_gerenciadores():
    status = gerenciadores_control.grava_gerenciador(request)
    
    res = make_response(jsonify(status))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res