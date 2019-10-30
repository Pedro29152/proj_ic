from biblioteca import app
from biblioteca.models.dao import projetos_dao
from flask import redirect, url_for, send_from_directory, send_file, flash, session
import os

ALLOWED_EXTENSIONS = set(['pdf'])

def busca_curso(req = None):
    curso, ordem, cres = get_filtro(req)

    return projetos_dao.busca_projeto_curso(curso, ordem, cres)

def busca_descricao(req = None):
    desc, ordem, cres = get_filtro(req)
    
    return projetos_dao.busca_projeto_descricao(desc, ordem, cres)
    

def busca_titulo(req = None):
    titulo, ordem, cres = get_filtro(req)

    return projetos_dao.busca_projeto_titulo(titulo, ordem, cres)
    
def busca_orientador(req = None):
    orientador, ordem, cres = get_filtro(req)

    return projetos_dao.busca_projeto_orientador(orientador, ordem, cres)
 
def busca_autor(req = None):
    autor, ordem, cres = get_filtro(req)

    return projetos_dao.busca_projeto_autor(autor, ordem, cres)

def busca_palavras_chave(req = None):
    autor, ordem, cres = get_filtro(req)

    return projetos_dao.busca_projeto_palavras_chave(autor, ordem, cres)

def upload(req):
    if 'file' not in req.files:
        flash("Nenhum arquivo enviado")
        return redirect(req.url)

    if req.files['file'].filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(req.url)

    if req.files['file'] and allowed_file(req.files['file'].filename):
        if(projetos_dao.upload_projeto(req, session['username'])):
            flash("Arquvio enviado com sucesso")
            return redirect(url_for('upload_file', filename=req.files['file'].filename))
        else:
            flash('Preencha todos os campos corretamente')
            return redirect(req.url)
            
            
    elif not allowed_file(req.files['file'].filename):
        flash('Erro: extensão nao suportada')
        return redirect(req.url)
    
    else:
        flash('Um erro inesperado occoreu')
        return redirect(req.url)

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