from biblioteca import db
from .schemas import Cursos

from mysql.connector.errors import ProgrammingError

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

def get_relatorio_cursos(data_i= None, data_f= None):
    base_query = '''
        select 
            c.descricaoCurso as curso,
            count(*) as numProjetos, 
            year(dataAvaliacao) as ano, 
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end) AS 'semestre 1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre 2'
        from projetos as p
        natural join cursos as c
        where (p.ativo = 1 and p.status = 1) {0}
        group by c.codCurso, 3
        order by 1, 3
    '''
    
    if data_i and data_f:
        query = base_query.format('and dataAvaliacao between %s and %s')
        try:
            ret = db.bd_busca(query, (data_i, data_f))
        except ProgrammingError:
            return None
    else:
        query = base_query.format('')
        try:
            ret = db.bd_busca(query)
        except ProgrammingError:
            return None
    
    __remove_decimais(ret)

    return ret

def __remove_decimais(obj):
    for item in obj:
        item['semestre 1'] = int(item['semestre 1'])
        item['semestre 2'] = int(item['semestre 2'])
