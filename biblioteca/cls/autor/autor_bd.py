from  biblioteca import bd_conn

def grava_autor(nome, ra, codProj):
    bd_conn.bd_gravar(
        'insert into autores(raAutor, nomeAutor, codProjeto) values (%s,%s,%s)', 
        (nome, ra, codProj)
    )