
class PalavrasChaveDAO:
    def __init__(self, db):
        self.db = db
        
    def busca_palavras_chave(self, codProj):
        palavras = self.db.busca(
            'select palavraChave from palavras_chave natural join projetos pj where codProjeto = %s',
            (codProj,)
        )

        return palavras
