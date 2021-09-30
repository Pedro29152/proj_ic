from biblioteca.db import Db
from .schemas import Cursos

from mysql.connector.errors import ProgrammingError

def busca_curso_nome(descricaoCurso):
    with Db() as db:
        nomeCurso = '%' + descricaoCurso + '%'

        val = db.busca(
            'select * from cursos where descricaoCurso like (%s) and ativo = 1',
            (nomeCurso,)
        )

        return val

def desativa_curso(codCurso):
    with Db() as db:
        query = 'update cursos set ativo = 0 where codCurso = (%s)'

        db.gravar_autocommit(query, (codCurso,))

def ativa_curso(codCurso):
    with Db() as db:
        query = 'update cursos set ativo = 1 where codCurso = (%s)'

        db.gravar_autocommit(query, (codCurso,))

def is_ativo(curso):
    with Db() as db:
        query = 'select * from cursos where (descricaoCurso = (%s) or abreviacao = (%s)) and ativo = 1'
        ret = db.busca_um(query, (curso.descricaoCurso, curso.abreviacao))

        if ret:
            return True
        return False

def reativa_curso(curso):
    with Db() as db:
        query = 'update cursos set descricaoCurso = (%s), abreviacao = (%s), ativo = 1, codUsuario = (%s) where abreviacao = (%s) or descricaoCurso = (%s)'

        db.gravar_autocommit(query, (curso.descricaoCurso, curso.abreviacao, curso.codUsuario, curso.abreviacao, curso.descricaoCurso))

def busca_cursos():
    with Db() as db:
        val = db.busca(
            'select * from cursos where ativo = 1',
            None
        )

        return val

def busca_cursos_inativo():
    with Db() as db:
        val = db.busca(
            'select * from cursos',
            None
        )

        return val

def busca_curso_cod(codCurso):
    with Db() as db:
        val = db.busca_um(
            'select descricaoCurso, abreviacao from cursos where codCurso = (%s) and ativo = 1',
            (codCurso,)
        )

        return val

def get_all_curso_cod(codCurso):
    with Db() as db:
        query = '''
            select descricaoCurso, abreviacao from cursos 
            where codCurso = (%s)
        '''
        val = db.busca_um(query,(codCurso,))
        return val

def get_codCurso(descricaoCurso):
    with Db() as db:
        val = db.busca_um(
            'select * from cursos where descricaoCurso = (%s) and ativo = 1', 
            (descricaoCurso, )
        )

        return val['codCurso']

def get_abreviacao(descricaoCurso):
    with Db() as db:
        curso = db.busca_um(
            'select abreviacao from cursos where descricaoCurso = (%s) and ativo = 1',
            (descricaoCurso, )
        )

        return curso['abreviacao']

def get_curso_desc(descricaoCurso):
    with Db() as db:
        res = db.busca_um("select * from cursos where descricaoCurso = (%s) and ativo = 1",
        (descricaoCurso,))

        curso = Cursos(res['descricaoCurso'], res['abreviacao'], res['codCurso'])

        return curso

def get_curso_codCurso(codCurso, is_instance=True):
    with Db() as db:
        query = '''
            select * from cursos 
            where codCurso = (%s) and ativo = 1
        '''
        res = db.busca_um(query, (codCurso,))

        if(not res):
            return None
        
        if is_instance:
            curso = Cursos(res['descricaoCurso'], res['abreviacao'], res['codUsuario'], res['codCurso'])
            return curso
        return res

def get_curso_codUsuario(codUsuario):
    with Db() as db:
        query = '''
            select c.* from cursos as c 
            join usuario_orientado as uo 
            on uo.codCurso = c.codCurso
            where uo.codUsuario = (%s)
        '''
        ret = db.busca_um(query, (codUsuario,))
        return ret

def get_count():
    with Db() as db:
        query = 'select count(*) as cursos from cursos where ativo = 1'
        ret = db.busca_um(query, None)
        return ret['cursos']

def get_curso_codUsuario_coordenador(codUsuario):
    with Db() as db:
        query = '''
            select * from cursos where codUsuario = (%s)
        '''
        ret = db.busca_um(query, (codUsuario,))
        return ret

def get_relatorio_cursos(data_i= None, data_f= None):
    with Db() as db:
        base_query = '''
            select 
                c.descricaoCurso as curso,
                count(*) as quantidadeDeProjetos, 
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
                ret = db.busca(query, (data_i, data_f))
            except ProgrammingError:
                return None
        else:
            query = base_query.format('')
            try:
                ret = db.busca(query)
            except ProgrammingError:
                return None
        
        __remove_decimais(ret)

        return ret

def __remove_decimais(obj):
    for item in obj:
        item['semestre 1'] = int(item['semestre 1'])
        item['semestre 2'] = int(item['semestre 2'])
