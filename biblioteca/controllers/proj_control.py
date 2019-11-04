from biblioteca.models.dao import projetos_dao
from flask import redirect, url_for, send_from_directory, send_file, flash, session, current_app as app
import os

ALLOWED_EXTENSIONS = set(['pdf'])

def busca_curso(req = None):
    curso, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_curso(curso, ordem, cres)

    return {
        'status':'OK',
        'data': ret
    }

def busca_descricao(req = None):
    desc, ordem, cres = get_filtro(req)
    
    ret = projetos_dao.busca_projeto_descricao(desc, ordem, cres)

    return {
        'status':'OK',
        'data': ret
    }
    

def busca_titulo(req = None):
    titulo, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_titulo(titulo, ordem, cres)

    return {
        'status':'OK',
        'data': ret
    }
    
def busca_orientador(req = None):
    orientador, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_orientador(orientador, ordem, cres)

    return {
        'status':'OK',
        'data': ret
    }
 
def busca_autor(req = None):
    autor, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_autor(autor, ordem, cres)

    return {
        'status':'OK',
        'data': ret
    }

def busca_palavras_chave(req = None):
    autor, ordem, cres = get_filtro(req)

    ret = projetos_dao.busca_projeto_palavras_chave(autor, ordem, cres)

    return {
        'status':'OK',
        'data': ret
    }

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
    flash(query)
    flash(tipo)
    flash(ordem)
        
    ret = projetos_dao.busca_projeto_ranking(query, tipo, ordem)


    if ret == None:
        return{
            'status':'vazio',
            'message': 'nenhum projeto listado',
            'data': ret
        }

    return {
        'status': 'OK',
        'message': 'ranking listado com sucesso',
        'data': ret
        }

def upload(req):
    if 'file' not in req.files:
        return {
            'status': 'falha',
            'message': 'Nenhum arquivo foi enviado'
        }

    if req.files['file'].filename == '':
        return {
            'status': 'falha',
            'message': 'Nenhum arquivo selecionado'
        }

    if req.files['file'] and allowed_file(req.files['file'].filename):
        return projetos_dao.upload_projeto(req, session['username'])
            
    elif not allowed_file(req.files['file'].filename):
        return {
                'status': 'falha',
                'message': 'Erro: extensão nao suportada'
            }
    
    else:
        return {
                'status': 'erro',
                'message': 'Um erro inesperado occoreu'
            }

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