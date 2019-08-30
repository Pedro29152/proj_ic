from biblioteca import bd_conn
from mysql.connector.errors import IntegrityError

def grava_autor(nome, ra, codProj):
    try:
        bd_conn.bd_gravar(
            'INSERT INTO autores(raAutor, nomeAutor) VALUES(%s,%s)', 
            (ra, nome)
        )
    except IntegrityError:
        None

    bd_conn.bd_gravar(
        'INSERT INTO projeto_autor VALUES(%s,%s)', 
        (codProj, ra)
    )

def busca_autor(codProj):
    try:
        return bd_conn.bd_busca(
            'SELECT autores.nomeAutor, autores.codAutor FROM autores NATURAL JOIN projeto_autor WHERE projeto_autor.codProjeto = %s',
            (codProj,)
        )
    except:
        return None