from biblioteca import db
from .schemas import Cursos

def busca_curso_nome(descricaoCurso):
    nomeCurso = '%' + descricaoCurso + '%'

    val = db.bd_busca(
        'select * from cursos where descricaoCurso like (%s) and ativo = 1',
        (nomeCurso,)
    )

    return val

def desativa_curso(codCurso):
    query = 'update cursos set ativo = 0 where codCurso = (%s)'

    db.bd_gravar(query, (codCurso,))

def ativa_curso(codCurso):
    query = 'update cursos set ativo = 1 where codCurso = (%s)'

    db.bd_gravar(query, (codCurso,))

def is_ativo(curso):
    query = 'select * from cursos where (descricaoCurso = (%s) or abreviacao = (%s)) and ativo = 1'
    ret = db.bd_busca_um(query, (curso.descricaoCurso, curso.abreviacao))

    if ret:
        return True
    return False

def reativa_curso(curso):
    query = 'update cursos set descricaoCurso = (%s), abreviacao = (%s), ativo = 1, codUsuario = (%s) where abreviacao = (%s) or descricaoCurso = (%s)'

    db.bd_gravar(query, (curso.descricaoCurso, curso.abreviacao, curso.codUsuario, curso.abreviacao, curso.descricaoCurso))

def busca_cursos():
    val = db.bd_busca(
        'select * from cursos where ativo = 1',
        None
    )

    return val

def busca_cursos_inativo():
    val = db.bd_busca(
        'select * from cursos',
        None
    )

    return val

def busca_curso_cod(codCurso):

    val = db.bd_busca_um(
        'select descricaoCurso, abreviacao from cursos where codCurso = (%s) and ativo = 1',
        (codCurso,)
    )

    return val

def get_all_curso_cod(codCurso):
    query = '''
        select descricaoCurso, abreviacao from cursos 
        where codCurso = (%s)
    '''
    val = db.bd_busca_um(query,(codCurso,))
    return val

def get_codCurso(descricaoCurso):

    val = db.bd_busca_um(
        'select * from cursos where descricaoCurso = (%s) and ativo = 1', 
        (descricaoCurso, )
    )

    return val['codCurso']

def get_abreviacao(descricaoCurso):

    curso = db.bd_busca_um(
        'select abreviacao from cursos where descricaoCurso = (%s) and ativo = 1',
        (descricaoCurso, )
    )

    return curso['abreviacao']

def get_curso_desc(descricaoCurso):
    res = db.bd_busca_um("select * from cursos where descricaoCurso = (%s) and ativo = 1",
    (descricaoCurso,))

    curso = Cursos(res['descricaoCurso'], res['abreviacao'], res['codCurso'])

    return curso

def get_curso_codCurso(codCurso, is_instance=True):
    query = '''
        select * from cursos 
        where codCurso = (%s) and ativo = 1
    '''
    res = db.bd_busca_um(query, (codCurso,))

    if(not res):
        return None
    
    if is_instance:
        curso = Cursos(res['descricaoCurso'], res['abreviacao'], res['codUsuario'], res['codCurso'])
        return curso
    return res

def get_curso_codUsuario(codUsuario):
    query = '''
        select c.* from cursos as c 
        join usuario_orientado as uo 
        on uo.codCurso = c.codCurso
        where uo.codUsuario = (%s)
    '''
    ret = db.bd_busca_um(query, (codUsuario,))
    return ret

def get_count():
    query = 'select count(*) as cursos from cursos where ativo = 1'
    ret = db.bd_busca_um(query, None)
    return ret['cursos']

def get_curso_codUsuario_coordenador(codUsuario):
    query = '''
        select * from cursos where codUsuario = (%s)
    '''
    ret = db.bd_busca_um(query, (codUsuario,))
    return ret
