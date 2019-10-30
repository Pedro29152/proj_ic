from biblioteca import bd_conn
from werkzeug.security import check_password_hash, generate_password_hash

def verifica_usr(usuario, senha):
    
    query = busca_usuarios_nome(usuario)
    
    if(query):
        if(query[0] != None):
            if(check_password_hash(query[0]['senha'], senha)):
                return True

    return False
    
def busca_nivel_acesso(username):
    val = bd_conn.bd_busca_um(
        'SELECT tipoUsuario FROM usuarios WHERE nomeUsuario = %s',
        (username,)
    )

    return val['tipoUsuario']

def busca_usuarios_nome(nomeUsuario):
    val = bd_conn.bd_busca(
        'select * from usuarios where nomeUsuario = %s',
        (nomeUsuario,)
    )
    if(not val):
        val = ''

    return val

def add_usr(usuario, senha,tipoUsuario,codGerenciador):
    bd_conn.bd_gravar(
        'insert into usuarios(nomeUsuario, senha, tipoUsuario, ativo, codGerenciador) '+ 
        'values(%s, %s, %s, 1, %s)',
        (usuario, generate_password_hash(senha),tipoUsuario,codGerenciador)
    )
    
    return 0