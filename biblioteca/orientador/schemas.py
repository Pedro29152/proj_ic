from biblioteca.db import Db
from biblioteca import response_messages
from biblioteca import extensions

class Orientadores:
    def __init__(self, codOrientador=None, nomeOrientador='', raOrientador='', email='', currLattes=None):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
        self.email = email.lower()
        self.currLattes = currLattes

        if not extensions.is_valid_email(self.email):
            raise AttributeError(response_messages.VALIDACAO_DEVE('email', 'ser um email valido'))
        if not extensions.is_valid_http_link(self.currLattes):
            raise AttributeError(response_messages.VALIDACAO_DEVE('currLattes', 'ser um link http/https valido valido'))
    
    def grava_orientador(self):
        with Db() as db:
            if self.nomeOrientador and self.raOrientador and self.email and self.currLattes:
                query1 = 'insert into orientadores(nomeOrientador, raOrientador, email, currLattes) values(%s, %s, %s, %s)'
                db.gravar_autocommit(query1, (self.nomeOrientador, self.raOrientador, self.email, self.currLattes))
                
                query2 = 'select codOrientador from orientadores where raOrientador = (%s)'
                self.codOrientador = db.busca_um(query2, (self.raOrientador,))['codOrientador']
            else:
                raise AttributeError(response_messages.ATRIBUTO_OBRIGATORIO('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"'))
        
    def edita_orientador(self):
        with Db() as db:
            if not (self.nomeOrientador or self.raOrientador or self.email or self.currLattes):
                raise AttributeError(response_messages.ATRIBUTO_OBRIGATORIO('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"'))
                
            query = 'update orientadores set nomeOrientador = (%s), raOrientador = (%s), email = (%s), currLattes = (%s) where codOrientador = (%s)'
            db.gravar_autocommit(query, (self.nomeOrientador, self.raOrientador, self.email, self.currLattes, self.codOrientador))