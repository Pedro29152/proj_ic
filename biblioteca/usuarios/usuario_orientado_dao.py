
class UsuarioOrientadoDAO():
    def __init__(self, db):
        self.db = db

    def edita_orientador_projeto_novo(self, codProjeto, codOrientador):
        query = 'update usuario_orientado set codOrientador = (%s) where codProjeto = (%s)'
        query2 = 'update projeto_orientador set codOrientador = (%s) where codProjeto = (%s)'

        self.db.gravar(query, (codOrientador, codProjeto))
        self.db.gravar(query2, (codOrientador, codProjeto))
        self.db.commit()

    def get_usuario_orientado(self, codOrientador, codUsuario):
        query = '''
            select * from usuario_orientado 
            where codOrientador = (%s) and codUsuario = (%s)
        '''
        ret = self.db.busca_um(query, (codOrientador, codUsuario))
        return ret

    def get_usuario_orientado_aluno(self, codUsuario):
        query = '''
            select * from usuario_orientado where codUsuario = (%s)
        '''
        return self.db.busca_um(query, (codUsuario,))

    def get_usuario_orientado_codProjeto_codOrientador(self, codProjeto, codOrientador):
        query = '''
            select * from usuario_orientado where codProjeto = (%s) and codOrientador = (%s)
        '''
        ret = self.db.busca_um(query, (codProjeto, codOrientador))
        return ret

    def get_usuario_codProjeto(self, codProjeto):
        query = '''
            select u.* from usuarios as u 
            natural join usuario_orientado as uo 
            where uo.codProjeto = (%s)
        '''
        ret = self.db.busca_um(query, (codProjeto,))
        return ret

    def add_projeto(self, codUsuario, codProjeto):
        query = '''
            update usuario_orientado set codProjeto = (%s) where codUsuario = (%s)
        '''
        self.db.gravar(query, (codProjeto, codUsuario))
