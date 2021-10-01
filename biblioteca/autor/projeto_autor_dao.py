
class ProjetoAutorDAO:
    def __init__(self, db):
        self.db = db

    def grava_autor_proj(self, codProjeto, codAutor):
        query = 'INSERT INTO projeto_autor VALUES(%s,%s)'
        self.db.gravar_autocommit(query, (codProjeto, codAutor))

    def is_valid_autor(self, codProjeto, codAutor):
        query = 'select * from projeto_autor where codProjeto = (%s) and codAutor = (%s)'
        ret = self.db.busca_um(query, (codProjeto, codAutor))
        if ret:
            return True
        return False
