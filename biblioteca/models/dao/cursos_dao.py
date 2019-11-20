from  biblioteca import bd_conn
from biblioteca.models.classes import Cursos

def busca_curso_nome(descricaoCurso):
    nomeCurso = '%' + descricaoCurso + '%'

    val = bd_conn.bd_busca(
        'select * from cursos where descricaoCurso like (%s) and ativo = 1',
        (nomeCurso,)
    )

    return val

def desativa_curso(codCurso):
    query = 'update cursos set ativo = 0 where codCurso = (%s)'

    bd_conn.bd_gravar(query, (codCurso,))

def ativa_curso(codCurso):
    query = 'update cursos set ativo = 1 where codCurso = (%s)'

    bd_conn.bd_gravar(query, (codCurso,))

def is_ativo(curso):
    query = 'select * from cursos where (descricaoCurso = (%s) or abreviacao = (%s)) and ativo = 1'
    ret = bd_conn.bd_busca_um(query, (curso.descricaoCurso, curso.abreviacao))

    if ret:
        return True
    return False

def reativa_curso(curso):
    query = 'update cursos set descricaoCurso = (%s), abreviacao = (%s), ativo = 1 where abreviacao = (%s) or descricaoCurso = (%s)'

    bd_conn.bd_gravar(query, (curso.descricaoCurso, curso.abreviacao, curso.abreviacao, curso.descricaoCurso))

def busca_cursos():
    val = bd_conn.bd_busca(
        'select * from cursos where ativo = 1',
        None
    )

    return val

def busca_cursos_inativo():
    val = bd_conn.bd_busca(
        'select * from cursos',
        None
    )

    return val

def busca_curso_cod(codCurso):

    val = bd_conn.bd_busca_um(
        'select descricaoCurso, abreviacao from cursos where codCurso = (%s) and ativo = 1',
        (codCurso,)
    )

    return val

def get_codCurso(descricaoCurso):

    val = bd_conn.bd_busca_um(
        'select * from cursos where descricaoCurso = (%s) and ativo = 1', 
        (descricaoCurso, )
    )

    return val['codCurso']

def get_abreviacao(descricaoCurso):

    curso = bd_conn.bd_busca_um(
        'select abreviacao from cursos where descricaoCurso = (%s) and ativo = 1',
        (descricaoCurso, )
    )

    return curso['abreviacao']

def get_curso_desc(descricaoCurso):
    res = bd_conn.bd_busca_um("select * from cursos where descricaoCurso = (%s) and ativo = 1",
    (descricaoCurso,))

    curso = Cursos(res['descricaoCurso'], res['abreviacao'], res['codCurso'])

    return curso

def get_curso_codCurso(codCurso):
    res = bd_conn.bd_busca_um("select * from cursos where codCurso = (%s) and ativo = 1",
    (codCurso,))

    curso = Cursos(res['descricaoCurso'], res['abreviacao'], res['codCurso'])

    return curso

def get_count():
    query = 'select count(*) as cursos from cursos where ativo = 1'
    ret = bd_conn.bd_busca_um(query, None)
    return ret['cursos']