from biblioteca import db
from biblioteca import extensions

class Orientadores:
    def __init__(self, codOrientador=None, nomeOrientador='', raOrientador='', email='', currLattes=None):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
        self.email = email.lower()
        self.currLattes = currLattes

        if not extensions.is_valid_email(self.email):
            raise AttributeError('O campo "email" deve ser um email valido')
        if not extensions.is_valid_http_link(self.currLattes):
            raise AttributeError('O campo "currLattes" deve ser um link http/https valido valido')
    
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