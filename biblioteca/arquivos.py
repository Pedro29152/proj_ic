from random import randint
from flask import redirect, url_for, send_from_directory, send_file, flash, session
import datetime, os
from werkzeug.utils import secure_filename
from biblioteca import app
from biblioteca.cls.proj import proj_bd
from biblioteca.cls.gerenciador import gerenciador_bd
from biblioteca.cls.curso import curso_bd
from io import BytesIO

ALLOWED_EXTENSIONS = set(['pdf'])

#upload de arquivos eae
def upload(request):
    if 'file' not in request.files:
        flash("Nenhum arquivo enviado")
        return redirect(request.url)
    req = request

    if req.files['file'].filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(request.url)

    if req.files['file'] and allowed_file(req.files['file'].filename):
        upload_arquivo(req, session['username'])
        flash("Arquvio enviado com sucesso")
        return redirect(url_for('upload_file', filename=req.files['file'].filename))
            
    elif not allowed_file(req.files['file'].filename):
        flash('Erro: extensão nao suportada')
        return redirect(request.url)

def upload_arquivo(req, nomeGer):
    titulo = req.form['titulo']
    nomeOrientador = req.form['nomeOrientador']
    descricao = req.form['descricao']
    notaProj = req.form['notaProj']
    dataAvaliacao = req.form['dataAvaliacao']
    curso = req.form['curso']
    file = req.files['file']

    codCurso =  curso_bd.get_codCurso(curso)

    rand = hex(randint(0x100000,0xffffff))
    data = datetime.datetime.now()
    data = data.date()

    filename = secure_filename(file.filename)
    nfilename = filename.rsplit('.',2)[0]

    if len(curso) >= 10:
        curso = curso_bd.get_abbr_curso(curso)

    tituloarq = titulo
    if len(titulo) > 41:
        aux = titulo.split()
        tituloarq = ""
        for div in aux:
            tituloarq += div[0]


    filename = filename.replace(
        nfilename, 
        curso.upper().replace(' ', '-') + '-' +
        tituloarq.upper().replace(' ', '-') + '-' + 
        str(data) + "-" + str(rand).upper()
    )
    
    codGer = gerenciador_bd.get_codGer_usr(nomeGer)
    
    proj_bd.grava_projeto(
        titulo, nomeOrientador, descricao,
        filename, notaProj, dataAvaliacao, 
        codGer, codCurso
    )

    file.save(
        os.path.join(
            app.config['UPLOAD_FOLDER'], 
            filename
        )
    )
    return redirect(url_for('upload_file', filename=filename))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_arquivo(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file = open(uploads + '/' + filename, 'r')
    return file
