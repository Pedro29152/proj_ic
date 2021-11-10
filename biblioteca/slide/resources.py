import os

from flask_restful import Resource, request
from flask import current_app as app
from mysql.connector.errors import IntegrityError

from .slide_dao import SlideDAO
from biblioteca.db import get_db
from biblioteca import response_messages
from biblioteca.extensions import admin_token_required, get_request_form_data_attributes
from biblioteca.responses import (
    get_bad_request,
    get_response_code,
    get_not_found,
    get_success,
    get_erro,
    get_falha
)

ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpg', 'jpeg'])

class BuscarSlidesResource(Resource):
    def get(self):
        db = get_db()
        slideDao = SlideDAO(db)

        ret = slideDao.busca_slides()
        return ret

    @admin_token_required
    def post(self):
        db = get_db()
        slideDao = SlideDAO(db)

        count = slideDao.get_count()
        if count >= 5:
            return get_bad_request(response_messages.SEM_PERMICAO('cadastrar mais que 3 slides'))

        r, code = check_file()
        if r:
            return get_response_code(r, code)
        
        try:
            attr = get_request_form_data_attributes(['titulo', 'subTitulo', 'title', 'subTitle'])
        except Exception as ex:
            return get_erro(ex.__str__()), 400

        if attr['titulo'] and not attr['title']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"title"'))
        if attr['title'] and not attr['titulo']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"titulo"'))
        if attr['subTitulo'] and not attr['subTitle']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"subTitle"'))
        if attr['subTitle'] and not attr['subTitulo']:
            return get_bad_request(response_messages.ATRIBUTO_OBRIGATORIO('"subTitulo"'))

        file = request.files['file']
        filename = file.filename
        if len(filename) > 255:
            return get_erro(response_messages.NOME_ARQUIVO_MUITO_GRANDE())
        try:
            slideDao.adiciona_slide(attr['titulo'], attr['subTitulo'], attr['title'], attr['subTitle'], '/static/slides/{0}'.format(filename))
        except IntegrityError:
            return get_bad_request(response_messages.ERRO_INTEGRIDADE('Imagem'))

        try:
            filepath = os.path.join(
                app.config['SLIDES_FOLDER'],
                filename
            )
            file.save(filepath)
        except Exception as ex:
            db.rollback()
            raise ex

        return get_success(response_messages.ENTIDADE_GRAVADA('Slide'))

class SlideIdResource(Resource):
    def get(self, id):
        db = get_db()
        slideDao = SlideDAO(db)

        slide = slideDao.get_slide(id)
        return get_success(slide)
    
    @admin_token_required
    def put(self, id):
        has_file = True
        r, code = check_file()
        if r:
            has_file = False
        
        db = get_db()
        slideDao = SlideDAO(db)
            
        slide = slideDao.get_slide(id)
        if not slide:
            return get_not_found(response_messages.NAO_ENCONTRADO('Slide'))
        
        try:
            attr = get_request_form_data_attributes(['titulo', 'subTitulo', 'title', 'subTitle'])
        except Exception as ex:
            return get_erro(ex.__str__()), 400

        if attr['titulo']:
            slide['titulo'] = attr['titulo']
        if attr['subTitulo']:
            slide['subtitulo'] = attr['subTitulo']

        if attr['title']:
            slide['title'] = attr['title']
        if attr['subTitle']:
            slide['subtitle'] = attr['subTitle']

        slideDao.edita_slide(slide)

        if has_file:
            file = request.files['file']
            filename = file.filename
            try:
                slideDao.edita_imagem(id, '/static/slides/{0}'.format(filename))
            except IntegrityError:
                return get_bad_request(response_messages.ERRO_INTEGRIDADE('Imagem'))

            nomeImagem = slide['imagem'].split('/')[-1]
            oldFilepath = os.path.join(
                app.config['SLIDES_FOLDER'],
                nomeImagem
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
        db = get_db()
        slideDao = SlideDAO(db)

        count = slideDao.get_count()
        if count <= 1:
            return get_bad_request(response_messages.SEM_PERMICAO('apagar o último slide'))

        slide = slideDao.get_slide(id)
        if not slide:
            return get_not_found(response_messages.NAO_ENCONTRADO('Slide'))
        
        slideDao.delete_slide(id)

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
