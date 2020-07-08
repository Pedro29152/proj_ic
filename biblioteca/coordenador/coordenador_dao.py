from biblioteca import db

def get_coordenador_codCurso(codCurso):
    query = '''
        select * from coordenadores where codCurso = (%s)
    '''
    coord = db.bd_busca_um(query, (codCurso,))
    return coord