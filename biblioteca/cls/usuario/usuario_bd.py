from  biblioteca import bd_conn
from werkzeug.security import check_password_hash, generate_password_hash

def busca_usuario(nomeUsuario):
    nomeUsuario = '%' + nomeUsuario + '%'
    val = bd_conn.bd_busca(
        'select * from usuarios where nomeUsuario like (%s)',
        nomeUsuario
    )
    if(not val):
        val = ''

    return val

    
def busca_usuario_cmp(nomeUsuario):
    val = bd_conn.bd_busca(
        'select * from usuarios where nomeUsuario = %s',
        nomeUsuario
    )
    if(not val):
        val = ''

    return val

    
def grava_usuario(nomeUsuario, senha, tipoUsuario, codGerenciador):
    bd_conn.bd_gravar(
        'insert into usuarios(nomeUsuario,senha,tipoUsuario,codGerenciador)'+
        'values(%s, %s, %s,%s)',
        (nomeUsuario,generate_password_hash(senha),tipoUsuario,codGerenciador)
    )


def verifica_usr(usuario, senha):
    
    query = busca_usuario_cmp(usuario)
    
    if(query):
        if(query[0] != None):
            if(check_password_hash(query[0]['senha'], senha)):
                return True

    return False

def add_usr(usuario, senha,tipoUsuario,codGerenciador):
    bd_conn.bd_gravar(
        'insert into usuarios(nomeUsuario, senha, tipoUsuario, ativo, codGerenciador) '+ 
        'values(%s, %s, %s, 1, %s)',
        (usuario, generate_password_hash(senha),tipoUsuario,codGerenciador)
    )
    
    return 0