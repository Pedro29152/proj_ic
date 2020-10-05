import os

from flask_restful import Resource, request
from flask import current_app as app
from mysql.connector.errors import IntegrityError

from . import slide_dao
from biblioteca import response_messages
from biblioteca.extensions import admin_token_required
from biblioteca.responses import (
    get_bad_request,
    get_response_code,
    get_not_found,
    get_success,
    get_erro,
    get_falha
)

ALLOWED_EXTENSIONS = set(['png', 'gif'])

class BuscarSlidesResource(Resource):
    def get(self):
        ret = slide_dao.busca_slides()
        return ret

    @admin_token_required
    def post(self):
        r, code = check_file()
        if r:
            return get_response_code(r, code)
        
        try:
            titulo = request.form['titulo']
            subTitulo = request.form['subTitulo']
        except:
            return get_bad_request(response_messages.CAMPOS_OBRIGATORIOS('"titulo" e "subTitulo"'))
        
        if not (titulo and subTitulo):
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"titulo" e "subTitulo"'))

        file = request.files['file']
        filename = file.filename
        if len(filename) > 255:
            return get_erro(response_messages.NOME_ARQUIVO_MUITO_GRANDE())
        try:
            slide_dao.adiciona_slide(titulo, subTitulo, filename)
        except IntegrityError:
            return get_bad_request(response_messages.ERRO_INTEGRIDADE('Imagem'))

        filepath = os.path.join(
            app.config['SLIDES_FOLDER'],
            filename
        )
        file.save(filepath)

        return get_success(response_messages.ENTIDADE_GRAVADA('Slide'))

class SlideIdResource(Resource):
    @admin_token_required
    def put(self, id):
        has_file = True
        r, code = check_file()
        if r:
            has_file = False
        
        slide = slide_dao.get_slide(id)
        if not slide:
            return get_not_found(response_messages.NAO_ENCONTRADO('Slide'))
        
        try:
            titulo = request.form['titulo']
            subTitulo = request.form['subTitulo']
        except:
            return get_bad_request(response_messages.CAMPOS_OBRIGATORIOS('"titulo" e "subTitulo"'))

        if titulo:
            slide['titulo'] = titulo
        if subTitulo:
            slide['subTitulo'] = subTitulo

        slide_dao.edita_slide(slide)

        if has_file:
            file = request.files['file']
            filename = file.filename

            try:
                slide_dao.edita_imagem(id, filename)
            except IntegrityError:
                return get_bad_request(response_messages.ERRO_INTEGRIDADE('Imagem'))

            oldFilepath = os.path.join(
                app.config['SLIDES_FOLDER'],
                slide['imagem']
            )
            filepath = os.path.join(
                app.config['SLIDES_FOLDER'],
                filename
            )

            os.remove(oldFilepath)
            file.save(filepath)

        return get_success(response_messages.ENTIDADE_EDITADA('Slide'))

    @admin_token_required
    def delete(self, id):
        slide = slide_dao.get_slide(id)
        if not slide:
            return get_not_found(response_messages.NAO_ENCONTRADO('Slide'))
        
        slide_dao.delete_slide(id)

        filepath = os.path.join(
            app.config['SLIDES_FOLDER'],
            slide['imagem']
        )
        os.remove(filepath)

        return get_success(response_messages.ENTIDADE_DELETADA('Slide'))

def check_file():
    if 'file' not in request.files:
        return get_falha(response_messages.ARQUIVO_NAO_ENVIADO()), 400

    if request.files['file'].filename == '':
        return get_falha(response_messages.ARQUIVO_NAO_ENVIADO()), 400

    if not __allowed_file(request.files['file'].filename):
        return get_falha(response_messages.EXTENSAO_NAO_SUPORTADA()), 415
    
    if request.files['file']:
        return None, None
            
    return get_erro(response_messages.ERRO_INESPERADO()), 500
def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
