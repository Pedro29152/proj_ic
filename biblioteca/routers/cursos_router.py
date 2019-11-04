from biblioteca import app
from biblioteca.controllers import curso_control
from biblioteca.routes import login_reqired, admin_reqired
from flask import make_response, jsonify, request

@app.route("/cursos/buscar", methods=['GET'])
def buscar_curso():
    status = curso_control.buscar_curso()

    res = make_response(jsonify(status))    
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/cursos/cadastrar", methods=['POST'])
@login_reqired
@admin_reqired
def cadastra_curso():
    status = curso_control.grava_curso(request)

    res = make_response(jsonify(status))    
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
