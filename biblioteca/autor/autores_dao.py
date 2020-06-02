from mysql.connector.errors import IntegrityError
from biblioteca import db

def busca_autores_proj(codProjeto):
    
    return db.bd_busca(
        '''
        SELECT autores.nomeAutor, autores.raAutor FROM autores 
        NATURAL JOIN projeto_autor pa 
        WHERE pa.codProjeto = %s
        ''',
        (codProjeto,)
    )

def get_autor_ra(ra):
    query = 'select * from autores where raAutor = (%s)'
    ret = db.bd_busca_um(query, (ra,))
    return ret

def cadastra_autor(nome, email, ra):
    query = 'insert into autores(nomeAutor, email, raAutor) values (%s, %s, %s)'
    try:
        db.bd_gravar(query, (nome, email, ra))
        return get_autor_ra(ra)
    except IntegrityError:
        return None