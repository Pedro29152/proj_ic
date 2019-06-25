from biblioteca                 import (app, arquivos, login, cls)
from flask                      import (Flask, render_template, redirect, request,\
    flash, url_for, jsonify,send_from_directory, session, make_response)
from functools                  import wraps
from biblioteca.cls.proj        import proj_bd
from biblioteca.cls.curso       import curso_bd
from biblioteca.cls.gerenciador import gerenciador_bd
from biblioteca.cls.usuario     import usuario_bd
import simplejson, json

def login_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Voce precisa estar logado antes de acessar esta página')
            return redirect(url_for('login_url'))

    return wrap
    
@app.route('/static/secret/<path:path>')
@app.route('/static/secret/')
@app.route('/<path:path>', defaults={'path':''})
@login_reqired
def not_allowed(path):
    return redirect(path)

#define a rota principal
@app.route("/")
@app.route("/index/")
def  index():
    #retorna a pagina
    return render_template("index.html")

#define rota para upload de arquivos 
@app.route("/upload/", methods=["GET", "POST"])
@login_reqired
def upload_file():
    if request.method == "POST":
        return arquivos.upload(request)
            
    cursos = curso_bd.busca_curso("")
    return render_template("upload.html", cursos= cursos )

#define rota para consulta de projetos cadastrados
@app.route("/consulta_proj", methods=["GET", "POST"])
@app.route("/consulta_proj/titulo", methods=["GET", "POST"])
def busca_titulo():
    if request.method == "GET":
        dados = proj_bd.busca_projeto_titulo("")
        return render_template("consulta.html",tgs = dados)

    if request.method == "POST":
        projs = busca_titulo(request)
        
        res = make_response(jsonify(projs))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/consulta_proj/titulo/likes', methods=['POST'])
def busca_likes():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/titulo/deslikes', methods=['POST'])
def busca_deslikes():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/titulo/n_visitas', methods=['POST'])
def busca_n_visitas():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/titulo/n_downloads', methods=['POST'])
def busca_n_downloads():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/titulo/dt_avaliacao', methods=['POST'])
def busca_dt_avaliacao():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/titulo/dataEnvio', methods=['POST'])
def busca_dt_envio():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/titulo/nota_rojeto', methods=['POST'])
def busca_nota_projeto():
    projs = busca_titulo(request)

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/curso', methods=['POST'])
def busca_curso():
    projs = None
    if(request.form['query']):
        projs = proj_bd.busca_projeto_curso(request.form['query'])
    else:
        projs = proj_bd.busca_projeto_curso('')
    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/descricao', methods=['POST'])
def busca_descricao():
    projs = None
    if(request.form['query']):
        projs = proj_bd.busca_projeto_descricao(request.form['query'])
    else:
        projs = proj_bd.busca_projeto_descricao('')
    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/consulta_proj/orientador', methods=['POST'])
def busca_orientador():
    projs = None
    if(request.form['query']):
        projs = proj_bd.busca_projeto_orientador(request.form['query'])
    else:
        projs = proj_bd.busca_projeto_orientador('')

    res = make_response(jsonify(projs))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def busca_titulo(req):
    projs = None
    cres = True

    try:
        titulo = req.form['query']
    except:
        titulo = ''

    try:
        ordem = int(req.form['ordem'])
    except:
        ordem = 0

    try:
        if(req.form['crescente'] == '0'):
            cres = False
    except:
        cres = True
    return proj_bd.busca_projeto_titulo(titulo, ordem, cres)
    
#rota para download de arquivos
@app.route("/download_file/<path:filename>", methods=["POST","GET"])
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

@app.route("/login/", methods=['POST','GET'])
def login_url():
    if request.method == "POST":
        return login.login_url(request)
        
    return render_template('login.html')

@app.route("/logout/", methods=['GET','POST'])
@login_reqired
def logout():
    login.logout_url()

    return redirect(url_for('index'))

@app.route("/cadastrar/", methods=["GET", "POST"])
@login_reqired
def cadastro():
    if request.method == "POST":
        return login.cadastro_usr(request)
    
    tipo = ['Usuario','Diretor','Admin']
    gerenciadores = gerenciador_bd.busca_gerenciador("")
    return render_template("cadastro.html",gerenciadores=gerenciadores,tipos=tipo)

@app.route('/testes/', methods=['POST', 'GET'])
def teste():
    if request.method == 'POST':
        projs = proj_bd.busca_projeto_titulo(request.form['query'])
        res = make_response(jsonify(projs))
        #res.headers['Access-Control-Allow-Origin'] = '*'
        return res

    return render_template('busca.html')

@app.route('/testei/')
def testei():
    return render_template('index_teste.html')

#rota padrao de caminhos nao definidos
@app.errorhandler(404)
def page_not_found(e):
    return render_template("err404.html")

#rota padrao para caminhos nao autorizados
@app.errorhandler(405)
def page_not_allowed(e):
    return render_template("err405.html")