from biblioteca import bd_conn
from mysql.connector.errors import IntegrityError

def busca_autores_proj(codProjeto):
    
    return bd_conn.bd_busca(
        '''
        SELECT autores.nomeAutor, autores.raAutor FROM autores 
        NATURAL JOIN projeto_autor pa 
        WHERE pa.codProjeto = %s
        ''',
        (codProjeto,)
    )

def deleta_autores(codProjeto):
    query = 'delete from projeto_autor where codProjeto = (%s)'
    bd_conn.bd_gravar(query, (codProjeto,))