from biblioteca.db import Db

class SlideDAO:
    def __init__(self, db):
        self.db = db

    def busca_slides(self):
        query = '''
            select * from slides
        '''

        ret = self.db.busca(query, None)
        return ret

    def get_slide(self, codSlide):
        query = '''
            select * from slides
            where codSlide = (%s)
        '''
        ret = self.db.busca_um(query, (codSlide,))
        return ret

    def adiciona_slide(self, titulo, subTitulo, title, subTitle, nomeImagem):
        query = '''
            insert into slides(titulo, subtitulo, title, subtitle, imagem) values (%s,%s,%s,%s,%s)
        '''

        self.db.gravar_autocommit(query, (titulo, subTitulo, title, subTitle, nomeImagem))

    def edita_slide(self, slide):
        query = '''
            update slides set titulo = (%s), subtitulo = (%s), title = (%s), subtitle = (%s)
            where codSlide = (%s)
        '''
        self.db.gravar_autocommit(query, (slide['titulo'], slide['subtitulo'], slide['title'], slide['subtitle'], slide['codSlide']))

    def edita_imagem(self, codSlide, imagem):
        query = '''
            update slides set imagem = (%s)
            where codSlide = (%s)
        '''
        self.db.gravar_autocommit(query, (imagem, codSlide))

    def delete_slide(self, codSlide):
        query = '''
            delete from slides 
            where codSlide = (%s)
        '''
        self.db.gravar_autocommit(query, (codSlide,))

    def get_count(self):
        query = '''
            select count(*) as count from slides
        '''
        ret = self.db.busca_um(query, None)
        return ret['count']
