from biblioteca import bd_conn
from werkzeug.security import check_password_hash, generate_password_hash

def verifica_usr(usuario, senha):
    
    query = busca_senha_nome(usuario)
    
    if(query):
        if(query != None):
            if(check_password_hash(query['senha'], senha)):
                return True

    return False
    
def busca_nivel_acesso(username):
    val = bd_conn.bd_busca_um(
        'SELECT tipoUsuario FROM usuarios WHERE nomeUsuario = %s',
        (username,)
    )

    return val['tipoUsuario']

def busca_usuarios():
    val = bd_conn.bd_busca(
        'select codUsuario, nomeUsuario, tipoUsuario, codGerenciador from usuarios where ativo = 1',
        None
    )
    if(not val):
        val = []

    return val

def busca_usuarios_nome(nomeUsuario):
    val = bd_conn.bd_busca_um(
        'select codUsuario, nomeUsuario, tipoUsuario, codGerenciador from usuarios where nomeUsuario = (%s) and ativo = 1',
        (nomeUsuario,)
    )
    if(not val):
        val = []

    return val

def busca_senha_nome(nomeUsuario):
    val = bd_conn.bd_busca_um(
        'select senha from usuarios where nomeUsuario = (%s) and ativo = 1',
        (nomeUsuario,)
    )

    return val

def busca_usuarios_nome_like(nomeUsuario):
    nomeUsuario = '%{}%'.format(nomeUsuario)
    val = bd_conn.bd_busca(
        'select codUsuario, nomeUsuario, tipoUsuario, codGerenciador from usuarios where nomeUsuario like (%s) and ativo = 1',
        (nomeUsuario,)
    )
    if(not val):
        val = []

    return val

def add_usr(usuario, senha,tipoUsuario,codGerenciador):
    bd_conn.bd_gravar(
        'insert into usuarios(nomeUsuario, senha, tipoUsuario, ativo, codGerenciador) '+ 
        'values(%s, %s, %s, 1, %s)',
        (usuario, generate_password_hash(senha),tipoUsuario,codGerenciador)
    )
    
    return 0

def get_count():
    query = 'select count(*) as usuarios from usuarios'
    ret = bd_conn.bd_busca_um(query, None)
    return ret['usuarios']