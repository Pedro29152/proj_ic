from biblioteca import db

def busca_slides():
    query = '''
        select * from slides
    '''

    ret = db.bd_busca(query, None)
    return ret

def get_slide(codSlide):
    query = '''
        select * from slides
        where codSlide = (%s)
    '''
    ret = db.bd_busca_um(query, (codSlide,))
    return ret

def adiciona_slide(titulo, subTitulo, title, subTitle, nomeImagem):
    query = '''
        insert into slides(titulo, subtitulo, title, subtitle, imagem) values (%s,%s,%s,%s,%s)
    '''

    db.bd_gravar(query, (titulo, subTitulo, title, subTitle, nomeImagem))

def edita_slide(slide):
    query = '''
        update slides set titulo = (%s), subtitulo = (%s), title = (%s), subtitle = (%s)
        where codSlide = (%s)
    '''
    db.bd_gravar(query, (slide['titulo'], slide['subtitulo'], slide['title'], slide['subtitle'], slide['codSlide']))

def edita_imagem(codSlide, imagem):
    query = '''
        update slides set imagem = (%s)
        where codSlide = (%s)
    '''
    db.bd_gravar(query, (imagem, codSlide))

def delete_slide(codSlide):
    query = '''
        delete from slides 
        where codSlide = (%s)
    '''
    db.bd_gravar(query, (codSlide,))

def get_count():
    query = '''
        select count(*) as count from slides
    '''
    ret = db.bd_busca_um(query, None)
    return ret['count']
