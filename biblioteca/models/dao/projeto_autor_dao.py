from biblioteca import bd_conn
from mysql.connector.errors import IntegrityError

def grava_autor_proj(codProjeto, codAutor):
    bd_conn.bd_gravar(
        'INSERT INTO projeto_autor VALUES(%s,%s)',
        (codProjeto, codAutor)
    )
            
