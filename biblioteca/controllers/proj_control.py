from biblioteca.models.dao import projetos_dao
from biblioteca.util import json_res 
from flask import session, current_app as app
import os

ALLOWED_EXTENSIONS = set(['pdf'])

def busca_curso(req = None):
    curso, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_curso(curso, ordem, cres)

    return json_res.get_data(ret)

def busca_descricao(req = None):
    desc, ordem, cres = get_filtro(req)
    
    ret = projetos_dao.busca_projeto_descricao(desc, ordem, cres)

    return json_res.get_data(ret)
    

def busca_titulo(req = None):
    titulo, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_titulo(titulo, ordem, cres)

    return json_res.get_data(ret)
    
def busca_orientador(req = None):
    orientador, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_orientador(orientador, ordem, cres)

    return json_res.get_data(ret)
 
def busca_autor(req = None):
    autor, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_autor(autor, ordem, cres)

    return json_res.get_data(ret)

def busca_palavras_chave(req = None):
    autor, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_palavras_chave(autor, ordem, cres)

    return json_res.get_data(ret)

def busca_ranking(req):
    try:
        query = req.form['query']#args.get('query')
    except:
        query = ''
        
    try:
        tipo = req.form['tipo']
    except:
        tipo = 'like'

    try:
        ordem = req.form['ordem']
        if(not (ordem == '' or ordem == 'desc')):
            ordem = ''
    except:
        ordem = ''
        
    ret = projetos_dao.busca_projeto_ranking(query, tipo, ordem)


    if ret == None:
        return json_res.get_falha('Nenhum projeto listado')

    return json_res.get_data(ret)

def upload(req):
    if 'file' not in req.files:
        return json_res.get_falha('Nenhum arquivo foi enviado')

    if req.files['file'].filename == '':
        return json_res.get_falha('Nenhum arquivo selecionado')

    if req.files['file'] and allowed_file(req.files['file'].filename):
        return projetos_dao.upload_projeto(req, session['username'])
            
    elif not allowed_file(req.files['file'].filename):
        return json_res.get_falha('Erro: extensão nao suportada')
    
    else:
        return json_res.get_erro('Um erro inesperado occoreu')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_arquivo(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file = open(uploads + '/' + filename, 'r')
    return file

def get_filtro(req = None):
    try:
        desc = req.form['query']
    except:
        desc = ''

    try:
        ordem = int(req.form['ordem'])
    except:
        ordem = 0

    cres = True
    try:
        if(req.form['crescente'] == '0'):
            cres = False
    except:
        cres = True

    return desc, ordem, cres

def get_count():
    count = projetos_dao.get_count()
    return json_res.get_count(count)