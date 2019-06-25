from random import randint
from flask import redirect, url_for, send_from_directory, send_file, flash, session
import datetime, os
from werkzeug.utils import secure_filename
from biblioteca import app
from biblioteca.cls.proj import proj_control
from biblioteca.cls.gerenciador import gerenciador_bd
from biblioteca.cls.curso import curso_bd
from io import BytesIO

ALLOWED_EXTENSIONS = set(['pdf'])

def upload(request):
    if 'file' not in request.files:
        flash("Nenhum arquivo enviado")
        return redirect(request.url)
    req = request

    if req.files['file'].filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(request.url)

    if req.files['file'] and allowed_file(req.files['file'].filename):
        proj_control.upload_arquivo(req, session['username'])
        flash("Arquvio enviado com sucesso")
        return redirect(url_for('upload_file', filename=req.files['file'].filename))
            
    elif not allowed_file(req.files['file'].filename):
        flash('Erro: extensão nao suportada')
        return redirect(request.url)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_arquivo(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file = open(uploads + '/' + filename, 'r')
    return file
