from biblioteca import app
from biblioteca.routes import login_reqired
from biblioteca.controllers import proj_control
from flask import request, jsonify, make_response, send_from_directory

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
