from biblioteca.db import Db

def busca_slides():
    with Db() as db:
        query = '''
            select * from slides
        '''

    ret = db.busca(query, None)
    return ret

def get_slide(codSlide):
    with Db() as db:
        query = '''
            select * from slides
            where codSlide = (%s)
        '''
        ret = db.busca_um(query, (codSlide,))
        return ret

def adiciona_slide(titulo, subTitulo, title, subTitle, nomeImagem):
    with Db() as db:
        query = '''
            insert into slides(titulo, subtitulo, title, subtitle, imagem) values (%s,%s,%s,%s,%s)
        '''

        db.gravar_autocommit(query, (titulo, subTitulo, title, subTitle, nomeImagem))

def edita_slide(slide):
    with Db() as db:
        query = '''
            update slides set titulo = (%s), subtitulo = (%s), title = (%s), subtitle = (%s)
            where codSlide = (%s)
        '''
        db.gravar_autocommit(query, (slide['titulo'], slide['subtitulo'], slide['title'], slide['subtitle'], slide['codSlide']))

def edita_imagem(codSlide, imagem):
    with Db() as db:
        query = '''
            update slides set imagem = (%s)
            where codSlide = (%s)
        '''
        db.gravar_autocommit(query, (imagem, codSlide))

def delete_slide(codSlide):
    with Db() as db:
        query = '''
            delete from slides 
            where codSlide = (%s)
        '''
        db.gravar_autocommit(query, (codSlide,))

def get_count():
    with Db() as db:
        query = '''
            select count(*) as count from slides
        '''
        ret = db.busca_um(query, None)
        return ret['count']
