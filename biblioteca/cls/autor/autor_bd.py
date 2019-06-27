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
        'INSERT INTO projeto_autor(codProjeto, raAutor) VALUES(%s,%s)', 
        (codProj, ra)
    )