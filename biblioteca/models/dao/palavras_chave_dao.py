from biblioteca import bd_conn
from biblioteca.models.classes import PalavrasChave
from biblioteca.models.dao import projetos_dao

def busca_palavras_chave(codProj):
    palavras = bd_conn.bd_busca(
        'select palavraChave from palavras_chave natural join projetos pj where codProjeto = %s',
        (codProj,)
    )

    return palavras
