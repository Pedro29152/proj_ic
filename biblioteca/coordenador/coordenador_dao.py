from biblioteca import db

def get_coordenador_codCurso(codCurso):
    query = '''
        select * from coordenadores where codCurso = (%s)
    '''
    coord = db.bd_busca_um(query, (codCurso,))
    return coord

def get_coordenador_codUsuario(codUsuario):
    query = '''
        SELECT * FROM coordenadores 
        where codUsuario = (%s)
    '''
    coord = db.bd_busca_um(query, (codUsuario,))
    return coord
