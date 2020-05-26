from biblioteca import db

def busca_palavras_chave(codProj):
    palavras = db.bd_busca(
        'select palavraChave from palavras_chave natural join projetos pj where codProjeto = %s',
        (codProj,)
    )

    return palavras
