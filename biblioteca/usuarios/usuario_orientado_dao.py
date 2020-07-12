from biblioteca import db

def edita_orientador_aluno(codUsuario, codOrientador):
    query = 'update usuario_orientado set codOrientador = (%s) where codUsuario = (%s)'
    db.bd_gravar(query, (codOrientador, codUsuario))

def get_usuario_orientado(codOrientador, codUsuario):
    query = '''
        select * from usuario_orientado 
        where codOrientador = (%s) and codUsuario = (%s)
    '''
    ret = db.bd_busca_um(query, (codOrientador, codUsuario))
    return ret

def get_usuario_orientado_aluno(codUsuario):
    query = '''
        select * from usuario_orientado where codUsuario = (%s)
    '''
    return db.bd_busca_um(query, (codUsuario,))

def add_projeto(codUsuario, codProjeto):
    query = '''
        update usuario_orientado set codProjeto = (%s) where codUsuario = (%s)
    '''
    db.bd_gravar(query, (codProjeto, codUsuario))

def is_valid_coordenador(codCoordenador):
    pass
