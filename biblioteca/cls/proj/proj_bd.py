from biblioteca import bd_conn

def busca_projeto_titulo(titulo = '', ordem = 0, crescente = True):
    '''
    Busca um projeto pelo titulo com base em uma ordenacao 

    O parametro ordem serve para indicar qual sera o campo do qual a lista ira ser ordenada
    O parametro crescente serve para indicar qual sera o campo do qual a lista ira ser ordenada

    Caso ordem seja igual a 0 ordena pelo padrao do sql
    Caso ordem seja 1 ordena com base nos likes
    Caso ordem seja 2 ordena com base nos deslikes
    Caso ordem seja 3 ordena com base no numero de visitas
    Caso ordem seja 4 ordena com base no numero de downloads
    Caso ordem seja 5 ordena com base na data de avalicao
    Caso ordem seja 6 ordena com base na data de envio
    Caso ordem seja 7 ordena com base na nota projeto
    Por padrao ordem recebe o valor 0

    Caso crescente for True ele ordena de ordem crescente
    Caso crescente for False ele ordena de ordem decrescente
    Por padrao crescente recebe o valor True
    '''
    cres = ""
    if(crescente):
        cres = ""
    else:
        cres = "desc"

    titulo = "%" + titulo + "%"

    if(ordem == 0):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s)'+
            'ORDER BY tituloProjeto ' + cres, 
            titulo
        )
    elif (ordem == 1):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY likes ' + cres, 
            titulo
        )
    elif (ordem == 2):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY deslikes ' + cres, 
            titulo
        )
    elif (ordem == 3):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY numVisitas ' + cres, 
            titulo
        )
    elif (ordem == 4):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY numDownloads ' + cres, 
            titulo
        )
    elif (ordem == 5):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY dataAvaliacao ' + cres, 
            titulo
        )
    elif (ordem == 6):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY dataEnvio ' + cres, 
            titulo
        )
    elif (ordem == 7):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE tituloProjeto LIKE (%s) '+
            'ORDER BY notaProjeto ' + cres, 
            titulo
        )
    else:
        return None

def busca_projeto_curso(nomeCurso = '', ordem = 0, crescente = True):
    cres = ""
    if(crescente):
        cres = ""
    else:
        cres = "DESC"

    nomeCurso = '%' + nomeCurso + '%'
    if(ordem == 0):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s)',
            nomeCurso
        )
    elif (ordem == 1):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY likes ' + cres, 
            nomeCurso
        )
    elif (ordem == 2):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY deslikes ' + cres, 
            nomeCurso
        )
    elif (ordem == 3):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY numVisitas ' + cres, 
            nomeCurso
        )
    elif (ordem == 4):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY numDownloads ' + cres, 
            nomeCurso
        )
    elif (ordem == 5):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY dataAvaliacao ' + cres, 
            nomeCurso
        )
    elif (ordem == 6):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY dataEnvio ' + cres, 
            nomeCurso
        )
    elif (ordem == 7):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos ' + 
            'NATURAL JOIN cursos ' +
            'WHERE descricaoCurso LIKE (%s) '+
            'ORDER BY notaProjeto ' + cres, 
            nomeCurso
        )
        
def busca_projeto_descricao(descricao, ordem = 0, crescente = True):

    cres = ""
    if(crescente):
        cres = ""
    else:
        cres = "DESC"

    descricao = '%' + descricao + '%'
    if(ordem == 0):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s)', 
            descricao
        )
    elif (ordem == 1):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY likes  ' + cres, 
            descricao
        )
    elif (ordem == 2):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY deslikes  ' + cres, 
            descricao
        )
    elif (ordem == 3):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY numVisitas  ' + cres, 
            descricao
        )
    elif (ordem == 4):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY numDownloads  ' + cres, 
            descricao
        )
    elif (ordem == 5):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY dataAvaliacao  ' + cres, 
            descricao
        )
    elif (ordem == 6):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY dataEnvio  ' + cres, 
            descricao
        )
    elif (ordem == 7):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE descricao LIKE (%s) '+
            'ORDER BY notaProjeto  ' + cres, 
            descricao
        )


def busca_projeto_orientador(nomeOrientador, ordem = 0, crescente = True):

    cres = ""
    if(crescente):
        cres = ""
    else:
        cres = "DESC"

    nomeOrientador = '%' + nomeOrientador + '%'
    if(ordem == 0):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s)', 
            nomeOrientador
        )
    elif (ordem == 1):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY likes  ' + cres, 
            nomeOrientador
        )
    elif (ordem == 2):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY deslikes  ' + cres, 
            nomeOrientador
        )
    elif (ordem == 3):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY numVisitas  ' + cres, 
            nomeOrientador
        )
    elif (ordem == 4):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY numDownloads  ' + cres, 
            nomeOrientador
        )
    elif (ordem == 5):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY dataAvaliacao ' + cres, 
            nomeOrientador
        )
    elif (ordem == 6):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY dataEnvio  ' + cres, 
            nomeOrientador
        )
    elif (ordem == 7):
        return bd_conn.bd_busca(
            'SELECT * FROM projetos '+
            'WHERE nomeOrientador LIKE (%s) '+
            'ORDER BY notaProjeto  ' + cres, 
            nomeOrientador
        )


def grava_projeto(titulo, nomeOrientador, descricao, nomeArquivo, notaProj, dataAvaliacao,codGer,codCurso):
    bd_conn.bd_gravar(
        'insert into projetos'+
        '(tituloProjeto,nomeOrientador,descricao,nomeArquivo,notaProjeto,dataAvaliacao,codGerenciador,codCurso,ativo)'+
        'values(%s,%s,%s,%s,%s,%s,%s,%s,1)',
        (titulo,nomeOrientador,descricao,nomeArquivo,notaProj,dataAvaliacao,codGer,codCurso)
    )

