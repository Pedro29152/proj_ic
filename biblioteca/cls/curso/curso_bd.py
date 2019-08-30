from  biblioteca import bd_conn

def busca_curso(nomeCurso):
    nomeCurso = '%' + nomeCurso + '%'
    val = bd_conn.bd_busca(
        'select * from cursos where descricaoCurso like (%s)',
        (nomeCurso,)
    )

    return val

def busca_curso_cod(codCurso):
    
    val = bd_conn.bd_busca_um(
        'select descricaoCurso, abreviacao from cursos where codCurso = (%s)',
        (codCurso,)
    )

    return val

def grava_curso(desc, abbr):
    bd_conn.bd_gravar(
        'insert into cursos(descricaoCurso, abreviacao, ativo) values(%s,%s,1)',
        (desc, abbr)
    )

def get_codCurso(curso):
    val = bd_conn.bd_busca(
        'select * from cursos where descricaoCurso = (%s)', 
        (curso, )
    )
    if(val != None):
        val = val[0]['codCurso']

    return val

def get_abbr_curso(descricaoCurso):
    curso = bd_conn.bd_busca_um(
        'select abreviacao from cursos where descricaoCurso = (%s)',
        (descricaoCurso, )
    )
    return curso['abreviacao']
