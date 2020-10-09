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
        count = slide_dao.get_count()
        if count >= 5:
            return get_bad_request(response_messages.SEM_PERMICAO('cadastrar mais que 3 slides'))

        r, code = check_file()
        if r:
            return get_response_code(r, code)
        
        try:
            titulo = request.form['titulo']
            subTitulo = request.form['subTitulo']

            title = request.form['title']
            subTitle = request.form['subTitle']
        except:
            return get_bad_request(response_messages.CAMPOS_OBRIGATORIOS('"titulo", "subTitulo", "title" e "subTitle"'))
        
        if titulo and not title:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"title"'))
        if title and not titulo:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"titulo"'))
        if subTitulo and not subTitle:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"subTitle"'))
        if subTitle and not subTitulo:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"subTitulo"'))

        file = request.files['file']
        filename = file.filename
        if len(filename) > 255:
            return get_erro(response_messages.NOME_ARQUIVO_MUITO_GRANDE())
        try:
            slide_dao.adiciona_slide(titulo, subTitulo, title, subTitle, '/static/slides/{0}'.format(filename))
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

            title = request.form['title']
            subTitle = request.form['subTitle']
        except:
            return get_bad_request(response_messages.CAMPOS_OBRIGATORIOS('"titulo", "subTitulo", "title" e "subTitle"'))
        
        if (titulo and not title) and not slide['titulo']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"title"'))
        if (title and not titulo) and not slide['title']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"titulo"'))
        if (subTitulo and not subTitle) and not slide['subtitle']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"subTitle"'))
        if (subTitle and not subTitulo) and not slide['subtitulo']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"subTitulo"'))

        if titulo:
            slide['titulo'] = titulo
        if subTitulo:
            slide['subtitulo'] = subTitulo

        if title:
            slide['title'] = title
        if subTitle:
            slide['subtitle'] = subTitle

        slide_dao.edita_slide(slide)

        if has_file:
            file = request.files['file']
            filename = file.filename
            try:
                slide_dao.edita_imagem(id, '/static/slides/{0}'.format(filename))
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
        count = slide_dao.get_count()
        if count <= 1:
            return get_bad_request(response_messages.SEM_PERMICAO('apagar o último slide'))

        slide = slide_dao.get_slide(id)
        if not slide:
            return get_not_found(response_messages.NAO_ENCONTRADO('Slide'))
        
        slide_dao.delete_slide(id)

        nomeImagem = slide['imagem'].split('/')[-1]
        filepath = os.path.join(
            app.config['SLIDES_FOLDER'],
            nomeImagem
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
