from biblioteca import db
from .schemas import Orientadores

def get_orientador(raOrientador):
    query = 'select * from orientadores where raOrientador = (%s) and ativo = 1'
    ret = db.bd_busca_um(query, (raOrientador,))

    if ret:
        ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'])
        return ori
    return None

def busca_orientadores_codProjeto(codProjeto):
    val = db.bd_busca_um(
        'select codOrientador, nomeOrientador, raOrientador, email, currLattes from orientadores natural join projeto_orientador where codProjeto = (%s)',
        (codProjeto,)
    )

    return val

def busca_todos_orientadores():
    val = db.bd_busca(
        'select * from orientadores',
        None
    )

    return val

def busca_orientadores():    
    val = db.bd_busca(
        'select * from orientadores where ativo = 1',
        None
    )

    return val

def busca_todos_orientadores_nome(nome):
    nome = '%{}%'.format(nome)
    
    val = db.bd_busca(
        'select * from orientadores where nomeOrientador like (%s)',
        (nome,)
    )

    return val

def busca_orientadores_nome(nome):
    nome = '%{}%'.format(nome)
    
    val = db.bd_busca(
        'select * from orientadores where nomeOrientador like (%s) and ativo = 1',
        (nome,)
    )

    return val

def ativa_orientador(codOrientador):
    query = 'update orientadores set ativo = 1 where codOrientador = (%s)'

    db.bd_gravar(query, (codOrientador,))

def desativa_orientador(codOrientador):
    query = 'update orientadores set ativo = 0 where codOrientador = (%s)'

    db.bd_gravar(query, (codOrientador,))

def exists(codOrientador):
    query = 'select codOrientador from orientadores where codOrientador = (%s)'
    ret = db.bd_busca_um(query, (codOrientador,))

    if ret:
        return True
    return False

def get_count():
    query = 'select count(*) as orientadores from orientadores'
    ret = db.bd_busca_um(query, None)
    return ret['orientadores']