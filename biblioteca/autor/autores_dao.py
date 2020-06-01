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