from mysql.connector.errors import DatabaseError
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector.errors import IntegrityError
from datetime import datetime, timedelta

from biblioteca import db

def verifica_usr(usuario, senha):
    
    senhaR = busca_senha_nome(usuario)
    
    if(senhaR):
        if(check_password_hash(senhaR, senha)):
            return busca_usuarios_nome(usuario)

    return None
    
def busca_nivel_acesso(username):
    val = db.bd_busca_um(
        'SELECT tipoUsuario FROM usuarios WHERE nomeUsuario = %s',
        (username,)
    )

    return val['tipoUsuario']

def busca_usuarios():
    val = db.bd_busca(
        'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where ativo = 1',
        None
    )
    if(not val):
        val = []

    return val

def busca_usuarios_nome(nomeUsuario):
    val = db.bd_busca_um(
        'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario = (%s) and ativo = 1',
        (nomeUsuario,)
    )

    return val

def busca_senha_nome(nomeUsuario):
    val = db.bd_busca_um(
        'select senha from usuarios where nomeUsuario = (%s) and ativo = 1',
        (nomeUsuario,)
    )
    if val:
        return val['senha']
    return None

def busca_usuarios_nome_like(nomeUsuario):
    nomeUsuario = '%{}%'.format(nomeUsuario)
    val = db.bd_busca(
        'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario like (%s) and ativo = 1',
        (nomeUsuario,)
    )
    if(not val):
        val = []

    return val

def add_usr(usuario, senha, tipoUsuario, nome, email):
    try:
        db.bd_gravar(
            'insert into usuarios(nomeUsuario, senha, tipoUsuario, ativo, nome, email) '+ 
            'values(%s, %s, %s, 1, %s, %s)',
            (usuario, generate_password_hash(senha),tipoUsuario, nome, email)
        )
        return get_usuario_username(usuario)
    except IntegrityError:
        return None

def add_aluno(user, senha, nome, email, codAutor, codOrientador):
    user = add_usr(user, senha, 1, nome, email)
    if not user:
        return False

    dataValidade = datetime.now() + timedelta(days=30)
    codUsuario = user['codUsuario']
    query = 'insert into usuario_orientado(codOrientador, codAutor, codUsuario, dataValidade) values (%s, %s, %s, %s)'
    db.bd_gravar(query, (codOrientador, codAutor, codUsuario, dataValidade.__str__()))
    return True

def add_orientador(user, senha, nome, email, codOrientador):
    usr = add_usr(user, senha, 2, nome, email)
    if not usr:
        return False

    codUser = usr['codUsuario']
    query = 'update orientadores set codUsuario = (%s) where codOrientador = (%s)'
    db.bd_gravar(query, (codUser, codOrientador))
    return True

def get_count():
    query = 'select count(*) as usuarios from usuarios'
    ret = db.bd_busca_um(query, None)
    return ret['usuarios']

def get_usuario(codUsuario):
    query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where codUsuario = (%s)'
    ret = db.bd_busca_um(query,(codUsuario,))
    return ret

def get_usuario_username(username):
    query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario = (%s)'
    ret = db.bd_busca_um(query,(username,))
    return ret

def edita_usuario(usuario):
    query = 'update usuarios set nomeUsuario = (%s), nome = (%s), email = (%s), tipoUsuario = (%s) where codUsuario = (%s)'
    db.bd_gravar(query,(usuario['nomeUsuario'], usuario['nome'], usuario['email'], usuario['tipoUsuario'], usuario['codUsuario']))

def deleta_usuario(codUsuario):
    query = 'delete from usuarios where codUsuario = (%s)'
    db.bd_gravar(query,(codUsuario,))

def edita_senha(codUsuario, novaSenha):
    query = 'update usuarios set senha = (%s) where codUsuario = (%s)'
    db.bd_gravar(query, (generate_password_hash(novaSenha), codUsuario))

def is_user(codUsuario, username):
    query = 'select codUsuario from usuarios where codUsuario = (%s) and nomeUsuario = (%s)'
    if db.bd_busca_um(query, (codUsuario, username)):
        return True
    return False

def is_usuario_logado(codUsuario, nomeUsuarioLogado):
    query = 'select codUsuario from usuarios where nomeUsuario = (%s)'
    ret = db.bd_busca_um(query, (nomeUsuarioLogado,))
    if ret:
        if (ret['codUsuario'] == codUsuario):
            return True
    return False