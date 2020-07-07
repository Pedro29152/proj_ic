from mysql.connector.errors import IntegrityError
from biblioteca import db

def busca_autores(nomeAutor=''):
    if not nomeAutor:
        nomeAutor = ''
    nomeAutor = '%{}%'.format(nomeAutor)
    query = '''
        SELECT *
        FROM autores
        WHERE nomeAutor like (%s)
        '''
    ret = db.bd_busca(
        query,
        (nomeAutor,)
    )
    return ret


def busca_autores_proj(codProjeto):
    
    return db.bd_busca(
        '''
        SELECT autores.nomeAutor, autores.raAutor, autores.email
        FROM autores 
        NATURAL JOIN projeto_autor pa 
        WHERE pa.codProjeto = %s
        ''',
        (codProjeto,)
    )

def get_autor_ra(ra):
    query = 'select * from autores where raAutor = (%s)'
    ret = db.bd_busca_um(query, (ra,))
    return ret

def get_autor_codUsuario(codUsuario):
    query = '''
        select distinct a.codAutor, a.nomeAutor, a.raAutor, a.email 
        from autores as a 
        join usuario_orientado as uo 
        on uo.codAutor = a.codAutor 
        join usuarios as u 
        on u.codUsuario = uo.codUsuario 
        where u.codUsuario = (%s) and u.ativo = 1
    '''
    return db.bd_busca_um(query, (codUsuario,))

def cadastra_autor(nome, email, ra):
    query = 'insert into autores(nomeAutor, email, raAutor) values (%s, %s, %s)'
    try:
        db.bd_gravar(query, (nome, email, ra))
        return get_autor_ra(ra)
    except IntegrityError:
        return None


GET_ALUNO_QUERY = '''
    select distinct u.codUsuario
    from usuarios as u 
    join usuario_orientado as uo 
    on u.codUsuario = uo.codUsuario 
    join autores as a 
    on a.codAutor = uo.codAutor 
    where uo.dataValidade > now() and u.codUsuario = (%s) 
'''

def is_aluno_valido(codUsuario):
    query = GET_ALUNO_QUERY
    return db.bd_busca_um(query, (codUsuario,))
