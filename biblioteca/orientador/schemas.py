from biblioteca import response_messages
from biblioteca import extensions
from mysql.connector.errors import DataError, IntegrityError

class Orientadores:
    def __init__(self, codOrientador=None, nomeOrientador='', raOrientador='', email='', currLattes=None, db=None):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
        self.email = email.lower()
        self.currLattes = currLattes

        self.db = db

        if not extensions.is_valid_email(self.email):
            raise AttributeError(response_messages.VALIDACAO_DEVE('email', 'ser um email valido'))
        if not extensions.is_valid_http_link(self.currLattes):
            raise AttributeError(response_messages.VALIDACAO_DEVE('currLattes', 'ser um link http/https valido valido'))
    
    def grava_orientador(self):
        try:
            if self.nomeOrientador and self.raOrientador and self.email and self.currLattes:
                query1 = 'insert into orientadores(nomeOrientador, raOrientador, email, currLattes) values(%s, %s, %s, %s)'
                self.db.gravar(query1, (self.nomeOrientador, self.raOrientador, self.email, self.currLattes))
                
                query2 = 'select codOrientador from orientadores where raOrientador = (%s)'
                self.codOrientador = self.db.busca_um(query2, (self.raOrientador,))['codOrientador']
            else:
                raise AttributeError(response_messages.ATRIBUTO_OBRIGATORIO('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"'))
        except DataError:
            raise DataError(response_messages.VALIDACAO_DEVE('"raOrientador"', 'conter no máximo 5 caracteres'))
        except IntegrityError:
            raise IntegrityError(response_messages.ERRO_INTEGRIDADE('Email ou raOrientador'))
        
    def edita_orientador(self):
        if not (self.nomeOrientador or self.raOrientador or self.email or self.currLattes):
            raise AttributeError(response_messages.ATRIBUTO_OBRIGATORIO('"nomeOrientador", "raOrientador", "email" e "linkCurrLattes"'))
            
        query = 'update orientadores set nomeOrientador = (%s), raOrientador = (%s), email = (%s), currLattes = (%s) where codOrientador = (%s)'
        self.db.gravar(query, (self.nomeOrientador, self.raOrientador, self.email, self.currLattes, self.codOrientador))
