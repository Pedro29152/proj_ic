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

@app.route('/', defaults={'path': ''})
@app.route('/static/<path:path>')
def catch_all(path):
    return redirect(url_for('index'))

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

#define rota para consulta de tgs cadastrados
@app.route("/consulta/", methods=["GET", "POST"])
def consulta():
    if request.method == "GET":
        dados = proj_bd.busca_projeto("")
        return render_template("consulta.html",tgs = dados)
    if request.method == "POST":
        projs = None
        if(request.form):
            projs = proj_bd.busca_projeto(request.form['query'])
        else:
            projs = proj_bd.busca_projeto('')
        res = make_response(jsonify(projs))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#rota para download de arquivos
@app.route("/download_file/<path:filename>", methods=["POST","GET"])
def download(filename):

    ret = make_response(
        send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename, 
            sas_attachment=True
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
        projs = proj_bd.busca_projeto(request.form['query'])
        res = make_response(jsonify(projs))
        #res.headers['Access-Control-Allow-Origin'] = '*'
        return res

    return render_template('busca.html')

#rota padrao de caminhos nao definidos
@app.errorhandler(404)
def page_not_found(e):
    return render_template("err404.html")

#rota padrao para caminhos nao autorizados
@app.errorhandler(405)
def page_not_allowed(e):
    return render_template("err404.html")

if __name__ == '__main__':
    app.run()