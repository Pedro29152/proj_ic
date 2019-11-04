from biblioteca import bd_conn
from biblioteca.models.classes import Orientadores

def get_add_orientador(raOrientador, nomeOrientador):
    query = 'select * from orientadores where raOrientador = (%s)'
    ret = bd_conn.bd_busca_um(query, (raOrientador,))

    if ret:
        ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'])
        return ori

    else:
        ori = Orientadores(nomeOrientador=nomeOrientador, raOrientador=raOrientador)
        ori.grava_orientador()

        return ori

def busca_orientadores_codProjeto(codProjeto):
    
    val = bd_conn.bd_busca_um(
        'select codOrientador, nomeOrientador, raOrientador from orientadores natural join projeto_orientador where codProjeto = (%s)',
        (codProjeto,)
    )

    return val