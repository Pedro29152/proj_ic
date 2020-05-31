from biblioteca import db

class Orientadores:
    def __init__(self, codOrientador=None, nomeOrientador=None, raOrientador=None, email=None, currLattes=None):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
        self.email = email
        self.currLattes = currLattes
    
    def grava_orientador(self):
        if self.nomeOrientador and self.raOrientador and self.email and self.currLattes:
            db.bd_gravar(
                'insert into orientadores(nomeOrientador, raOrientador, email, currLattes) values(%s, %s, %s, %s)',
                (self.nomeOrientador, self.raOrientador, self.email, self.currLattes)
            )
            self.codOrientador = db.bd_busca_um(
                'select codOrientador from orientadores where raOrientador = (%s)', 
                (self.raOrientador,)
            )['codOrientador']
        else:
            raise AttributeError('Os campos "nomeOrientador", "raOrientador", "email" e "linkCurrLattes" devem ser preenchidos')
    
    def edita_orientador(self):
        if not (self.nomeOrientador or self.raOrientador or self.email or self.currLattes):
            raise AttributeError('Os campos "nomeOrientador", "raOrientador", "email" e "linkCurrLattes" devem ser preenchidos')

        db.bd_gravar(
            'update orientadores set nomeOrientador = (%s), raOrientador = (%s), email = (%s), currLattes = (%s) where codOrientador = (%s)',
            (self.nomeOrientador, self.raOrientador, self.email, self.currLattes, self.codOrientador)
        )