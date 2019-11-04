from biblioteca import app
from biblioteca.controllers import usuario_control
from biblioteca.routes import not_logged_in, login_reqired, admin_reqired
from flask import request, make_response, jsonify
from werkzeug.exceptions import BadRequestKeyError

@app.route("/usuarios/login", methods=['POST'])
@not_logged_in
def login_url():
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
        
@app.route("/usuarios/logout", methods=['GET', 'POST'])
@login_reqired
def logout():
    ret = usuario_control.logout_url()

    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/usuarios/cadastrar", methods=["POST"])
@login_reqired
@admin_reqired
def cadastro():
    ret = usuario_control.cadastro_usr(request)
    
    res = make_response(jsonify(ret))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
