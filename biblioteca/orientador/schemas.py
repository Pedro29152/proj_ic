from biblioteca import db

class Orientadores:
    def __init__(self, codOrientador=None, nomeOrientador=None, raOrientador=None):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
    
    def grava_orientador(self):
        if self.nomeOrientador and self.raOrientador:
            db.bd_gravar(
                'insert into orientadores(nomeOrientador, raOrientador) values(%s, %s)',
                (self.nomeOrientador, self.raOrientador)
            )
            self.codOrientador = db.bd_busca_um(
                'select codOrientador from orientadores where raOrientador = (%s)', 
                (self.raOrientador,)
            )['codOrientador']
        else:
            raise AttributeError('A classe deve possuir os campos "nomeOrientador" e "raOrientador" preenchidos')