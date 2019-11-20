from biblioteca import bd_conn
from biblioteca.models.classes import Orientadores

def get_orientador(raOrientador):
    query = 'select * from orientadores where raOrientador = (%s)'
    ret = bd_conn.bd_busca_um(query, (raOrientador,))

    if ret:
        ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'])
        return ori
    return None

def busca_orientadores_codProjeto(codProjeto):
    
    val = bd_conn.bd_busca_um(
        'select codOrientador, nomeOrientador, raOrientador from orientadores natural join projeto_orientador where codProjeto = (%s)',
        (codProjeto,)
    )

    return val

def busca_orientadores():    
    val = bd_conn.bd_busca(
        'select * from orientadores',
        None
    )

    return val

def busca_orientadores_nome(nome):
    nome = '%{}%'.format(nome)
    
    val = bd_conn.bd_busca(
        'select * from orientadores where nomeOrientador like (%s)',
        (nome,)
    )

    return val

def get_count():
    query = 'select count(*) as orientadores from orientadores'
    ret = bd_conn.bd_busca_um(query, None)
    return ret['orientadores']