from biblioteca                 import (app)
from flask                      import (Flask, render_template, redirect, request,\
    flash, url_for, jsonify,send_from_directory, session, make_response)
from functools                  import wraps
from biblioteca.models.dao      import cursos_dao, projetos_dao, gerenciadores_dao
from biblioteca.controllers     import curso_control, proj_control, usuario_control, gerenciadores_control
import simplejson, json
from werkzeug.exceptions import BadRequestKeyError

def login_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado(session):
            return f(*args, **kwargs)
        else:
            return jsonify( {
                'status': 'deslogado',
                'message': 'Voce precisa estar logado antes de acessar esta página'
            })

    return wrap

def admin_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado(session):
            if session['nivel_acesso'] > 1:
                return f(*args, **kwargs)
            else:
                return jsonify( {
                    'status': 'inacessivel',
                    'message': 'Seu nivel de acesso nao permite acesso a esta pagina'
                })
        else:
            return jsonify( {
                'status': 'deslogado',
                'message': 'Voce precisa estar logado antes de acessar esta página'
            })

    return wrap

def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash('Voce ja esta logado em uma conta, deslogue-se para poder acessar esta pagina')
            return redirect(url_for('index'))
    
    return wrap

@app.route('/static/secret/<path:path>')
@app.route('/static/secret', defaults={'path':''})
@admin_reqired
def not_allowed(path):
    return redirect(path)

#define a rota principal
@app.route("/")
@app.route("/index/")
def  index():
    #retorna a pagina
    return render_template("vue/index.html")

#define rota para consulta de projetos cadastrados
@app.route("/projetos/buscar", methods=["GET"])
def buscar():
    dados = projetos_dao.busca_projeto()
    
    return render_template("vue/busca.html",tgs = dados)

#define rota para upload de arquivos 
@app.route("/projetos/upload", methods=['POST'])
@login_reqired
def upload_file():
    status = proj_control.upload(request)

    res = make_response(jsonify(status))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/projetos/buscar/<path:tipo>", methods=["GET"])
def busca_titulo(tipo):
    projs = None
    if tipo == 'titulo':
        projs = proj_control.busca_titulo(request)

    if tipo == 'curso':
        projs = proj_control.busca_curso(request)

    if tipo == 'descricao':
        projs = proj_control.busca_descricao(request)

    if tipo == 'orientador':
        projs = proj_control.busca_orientador(request)

    if tipo == 'autor':
        projs = proj_control.busca_autor(request)

    if tipo == 'palavrasChave':
        projs = proj_control.busca_palavras_chave(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/projetos/buscar/ranking", methods=["GET"])
def busca_ranking():
    projs = proj_control.busca_ranking(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

#rota para download de arquivos
@app.route("/projetos/download_file/<path:filename>", methods=["POST","GET"])
def download(filename): 
    ret = make_response(
        send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename, 
            as_attachment=True
        )
    )

    ret.headers['Access-Control-Allow-Origin'] = '*'
    return ret

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

@app.route('/gerenciadores/cadastrar', methods=['POST'])
def cadastro_gerenciadores():
    status = gerenciadores_control.grava_gerenciador(request)
    
    res = make_response(jsonify(status))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


#rota padrao de caminhos nao definidos
@app.errorhandler(404)
def page_not_found(e):
    return render_template("err404.html")

#rota padrao para caminhos nao autorizados
@app.errorhandler(405)
def page_not_allowed(e):
    return render_template("err405.html")