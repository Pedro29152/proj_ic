from mysql.connector.errors import IntegrityError
from biblioteca.db import Db


def grava_autor_proj(codProjeto, codAutor):
    with Db() as db:
        query = 'INSERT INTO projeto_autor VALUES(%s,%s)'
        db.gravar_autocommit(query, (codProjeto, codAutor))

def is_valid_autor(codProjeto, codAutor):
    with Db() as db:
        query = 'select * from projeto_autor where codProjeto = (%s) and codAutor = (%s)'
        ret = db.busca_um(query, (codProjeto, codAutor))
        if ret:
            return True
        return False
