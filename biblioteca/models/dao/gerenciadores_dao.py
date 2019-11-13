from biblioteca import bd_conn
from biblioteca.models.classes import Gerenciadores

def busca_um_gerenciador_codGerenciador(codGerenciador):
    codGerenciador = '%' + codGerenciador + '%'

    val = bd_conn.bd_busca_um(
        'select * from gerenciadores where codGerenciador like (%s) and ativo = 1',
        (codGerenciador,)
    )

    return val

def busca_gerenciadores():
    val = bd_conn.bd_busca(
        'select * from gerenciadores where ativo = 1',
        None
    )

    return val

def busca_gerenciadores_nome(nomeGerenciador):
    nomeGerenciador = '%{}%'.format(nomeGerenciador)
    val = bd_conn.bd_busca(
        'select * from gerenciadores where nomeGerenciador like (%s) and ativo = 1',
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
    
def get_count():
    query = 'select count(*) as gerenciadores from gerenciadores where ativo = 1'
    ret = bd_conn.bd_busca_um(query, None)
    return ret['gerenciadores']

def deleta_gerenciador(codGerenciador):
    query = 'update gerenciadores set ativo = 0 where codGerenciador = (%s)'
    bd_conn.bd_gravar(query,(codGerenciador,))

def get_gerenciador(codGerenciador):
    query = 'select * from gerenciadores where codGerenciador = (%s)'
    ret = bd_conn.bd_busca_um(query,(codGerenciador,))
    return ret

def edita_gerenciador(codGerenciador, nomeGerenciador, instituicao, emailGerenciador):
    query = 'update gerenciadores set nomeGerenciador = (%s), instituicao = (%s), emailGerenciador = (%s) where codGerenciador = (%s)'
    bd_conn.bd_gravar(query,(nomeGerenciador, instituicao, emailGerenciador, codGerenciador))

def is_ativo(cpfGerenciador):
    query = 'select codGerenciador from gerenciadores where cpfGerenciador = (%s) and ativo = 1'
    if bd_conn.bd_busca_um(query, (cpfGerenciador,)):
        return True
    return False

def ativa_gerenciador(gerenciador):
    query = 'update gerenciadores set instituicao = (%s), nomeGerenciador = (%s), emailGerenciador = (%s), ativo = 1 where cpfGerenciador = (%s)'
    bd_conn.bd_gravar(query, (gerenciador.instituicao, gerenciador.nomeGerenciador, gerenciador.emailGerenciador, gerenciador.cpfGerenciador))