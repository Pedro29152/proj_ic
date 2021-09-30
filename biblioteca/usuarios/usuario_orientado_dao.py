from biblioteca.db import Db

def edita_orientador_projeto_novo(codProjeto, codOrientador):
    with Db() as db:
        query = 'update usuario_orientado set codOrientador = (%s) where codProjeto = (%s)'
        query2 = 'update projeto_orientador set codOrientador = (%s) where codProjeto = (%s)'

        db.gravar(query, (codOrientador, codProjeto))
        db.gravar(query2, (codOrientador, codProjeto))
        db.commit()

def get_usuario_orientado(codOrientador, codUsuario):
    with Db() as db:
        query = '''
            select * from usuario_orientado 
            where codOrientador = (%s) and codUsuario = (%s)
        '''
        ret = db.busca_um(query, (codOrientador, codUsuario))
        return ret

def get_usuario_orientado_aluno(codUsuario):
    with Db() as db:
        query = '''
            select * from usuario_orientado where codUsuario = (%s)
        '''
        return db.busca_um(query, (codUsuario,))

def get_usuario_orientado_codProjeto_codOrientador(codProjeto, codOrientador):
    with Db() as db:
        query = '''
            select * from usuario_orientado where codProjeto = (%s) and codOrientador = (%s)
        '''
        ret = db.busca_um(query, (codProjeto, codOrientador))
        return ret

def get_usuario_codProjeto(codProjeto):
    with Db() as db:
        query = '''
            select u.* from usuarios as u 
            natural join usuario_orientado as uo 
            where uo.codProjeto = (%s)
        '''
        ret = db.busca_um(query, (codProjeto,))
        return ret

def add_projeto(codUsuario, codProjeto):
    with Db() as db:
        query = '''
            update usuario_orientado set codProjeto = (%s) where codUsuario = (%s)
        '''
        db.gravar_autocommit(query, (codProjeto, codUsuario))
