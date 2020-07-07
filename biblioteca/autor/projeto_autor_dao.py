from mysql.connector.errors import IntegrityError
from biblioteca import db

def grava_autor_proj(codProjeto, codAutor):
    db.bd_gravar(
        'INSERT INTO projeto_autor VALUES(%s,%s)',
        (codProjeto, codAutor)
    )

def is_valid_autor(codProjeto, codAutor):
    query = 'select * from projeto_autor where codProjeto = (%s) and codAutor = (%s)'
    ret = db.bd_busca_um(query,(codProjeto, codAutor))
    if ret:
        return True
    return False

