from biblioteca import bd_conn
from biblioteca.models.classes import Gerenciadores

def busca_um_gerenciador_codGerenciador(codGerenciador):
    codGerenciador = '%' + codGerenciador + '%'

    val = bd_conn.bd_busca_um(
        'select * from gerenciadores where codGerenciador like (%s)',
        (codGerenciador,)
    )

    return val

def busca_gerenciadores():

    val = bd_conn.bd_busca(
        'select * from gerenciadores',
        None
    )

    return val

def busca_gerenciadores_nome(nomeGerenciador):
    nomeGerenciador = '%{}%'.format(nomeGerenciador)
    val = bd_conn.bd_busca(
        'select * from gerenciadores where nomeGerenciador like (%s)',
        (nomeGerenciador,)
    )

    return val

def get_codGer_nomeUsuario(nome): 
    val = ""

    query = bd_conn.bd_busca_um(
        'select gerenciadores.codGerenciador '+ 
        'from usuarios '+ 
        'natural join gerenciadores '+
        'where usuarios.nomeUsuario = (%s)',
        (nome, )
    )

    if(query != None):
        val = query['codGerenciador']

    return val

def get_gerenciador_cod_ger(codGerenciador):
    res = bd_conn.bd_busca_um(
        'select * from gerenciadores where codGerenciador = (%s)',
        (codGerenciador,))

    gerenciador = Gerenciadores(
        res['codGerenciador'],
        res['cpfGerenciador'],
        res['instituicao'],
        res['nomeGerenciador']
    )

    return gerenciador

def get_codGer_nomeGer(nomeGerenciador):
    ret = bd_conn.bd_busca_um(
        'select codGerenciador from gerenciadores where nomeGerenciador = (%s)',
        (nomeGerenciador,))
    
    return ret['codGerenciador']