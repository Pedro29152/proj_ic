from biblioteca.util.acessos import not_logged_in, login_reqired, admin_reqired
from biblioteca.util import util
from biblioteca.controllers import proj_control
from flask import request, jsonify, make_response, send_from_directory, Blueprint, current_app as app

PROJETOS_ROUTER = Blueprint('projetos_router', __name__)

#define rota para upload de arquivos 
@PROJETOS_ROUTER.route("/projetos/cadastrar", methods=['POST'])
@login_reqired
def upload_file():
    status = proj_control.upload(request)

    return util.response_ext(jsonify(status))

@PROJETOS_ROUTER.route("/projetos/buscar", methods=["GET"], defaults={'tipo':''})
@PROJETOS_ROUTER.route("/projetos/buscar/<path:tipo>", methods=["GET"])
def busca_titulo(tipo):
    projs = None
    if request.args.get('page'):
        page = request.args.get('page')
        projs = proj_control.busca_pag(request, tipo, page)
    else:
        projs = proj_control.busca(request, tipo)

    return util.response_ext(jsonify(projs))

@PROJETOS_ROUTER.route("/projetos/buscar/ranking", methods=["GET"])
def busca_ranking():
    projs = None
    if request.args.get('page'):
        page = request.args.get('page')
        projs = proj_control.busca_ranking_pag(request, page)
    else:
        projs = proj_control.busca_ranking(request)

    return util.response_ext(jsonify(projs))

#rota para download de arquivos
@PROJETOS_ROUTER.route("/projetos/download_file/<path:filename>", methods=["POST","GET"])
def download(filename):
    if proj_control.download_arquivo(filename):
        f = send_from_directory(    
                app.config['UPLOAD_FOLDER'],
                filename, 
                as_attachment=True
            )

        return util.response_ext(jsonify(f))
    
    return None

@PROJETOS_ROUTER.route('/projetos/count', methods=['GET'])
def projetos_count():
    ret = proj_control.get_count()
    
    
    return util.response_ext(jsonify(ret))