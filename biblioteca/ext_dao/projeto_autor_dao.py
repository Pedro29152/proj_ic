from mysql.connector.errors import IntegrityError
from biblioteca import db

def grava_autor_proj(codProjeto, codAutor):
    db.bd_gravar(
        'INSERT INTO projeto_autor VALUES(%s,%s)',
        (codProjeto, codAutor)
    )
            
