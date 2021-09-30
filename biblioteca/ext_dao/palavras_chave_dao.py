from biblioteca.db import Db

def busca_palavras_chave(codProj):
    with Db() as db:
        palavras = db.busca(
            'select palavraChave from palavras_chave natural join projetos pj where codProjeto = %s',
            (codProj,)
        )

        return palavras
