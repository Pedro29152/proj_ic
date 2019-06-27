from biblioteca import app
from biblioteca.cls.curso.curso_bd import get_codCurso, get_abbr_curso
from biblioteca.cls.gerenciador.gerenciador_bd import get_codGer_usr
from biblioteca.cls.proj.proj_bd import (busca_projeto_curso, busca_projeto_descricao, \
    busca_projeto_orientador, busca_projeto_titulo, grava_projeto, upload_projeto)
from flask import redirect, url_for, send_from_directory, send_file, flash, session
from random import randint
import datetime, os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf'])

def busca_curso(req = None):
    try:
        curso = req.form['query']
    except:
        curso = ''

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

    return busca_projeto_curso(curso, ordem, cres)

def busca_descricao(req = None):
    
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

    return busca_projeto_descricao(desc, ordem, cres)
    

def busca_titulo(req = None):

    try:
        titulo = req.form['query']
    except:
        titulo = ''

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

    return busca_projeto_titulo(titulo, ordem, cres)
    
def busca_orientador(req = None):

    try:
        orientador = req.form['query']
    except:
        orientador = ''

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

    return busca_projeto_orientador(orientador, ordem, cres)
 
def upload(req):
    if 'file' not in req.files:
        flash("Nenhum arquivo enviado")
        return redirect(req.url)

    if req.files['file'].filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(req.url)

    if req.files['file'] and allowed_file(req.files['file'].filename):
        if(upload_projeto(req, session['username'])):
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
