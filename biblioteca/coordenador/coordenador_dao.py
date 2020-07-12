from biblioteca import db
from biblioteca.curso import cursos_dao

def buscar_coordenadores(nomeCoordenador=''):
    nomeCoordenador = '%{}%'.format(nomeCoordenador)
    query = '''
        select * from coordenadores where nomeCoordenador like (%s)
    '''
    ret = db.bd_busca(query, (nomeCoordenador,)) 

    preenche_coordenadores(ret)

    return ret

def get_coordenador(codCoordenador):
    query = '''
        select * from coordenadores where codCoordenador = (%s)
    '''
    coord = db.bd_busca_um(query, (codCoordenador,))
    
    preenche_coordenador(coord)

    return coord

def get_count():
    query = '''
        select count(*) as coord from coordenadores
    '''
    coord = db.bd_busca_um(query, None)
    return coord['coord']

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

def cadastro_coordenador(nome, email, codCurso, codUsuario):
    query = '''
        insert into coordenadores(nomeCoordenador, email, codCurso, codUsuario) 
        values(%s, %s, %s, %s)
    '''
    db.bd_gravar(query, (nome, email, codCurso, codUsuario))

def preenche_coordenadores(coordenadores):
    for item in coordenadores:
        preenche_coordenador(item)

def preenche_coordenador(coordenador):
    curso = cursos_dao.get_all_curso_cod(coordenador['codCurso'])
    if curso:
        coordenador['curso'] = curso
