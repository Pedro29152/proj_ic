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
    query = 'SELECT * FROM projetos WHERE tituloProjeto LIKE (%s) '

    titulo = "%" + titulo + "%"

    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        titulo
    )

def busca_projeto_curso(nomeCurso = '', ordem = 0, crescente = True):
    query = 'SELECT * FROM projetos NATURAL JOIN cursos WHERE descricaoCurso LIKE (%s) '

    nomeCurso = '%' + nomeCurso + '%'

    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        nomeCurso
    )
        
def busca_projeto_descricao(descricao, ordem = 0, crescente = True):
    query = 'SELECT * FROM projetos WHERE descricao LIKE (%s) '

    descricao = '%' + descricao + '%'

    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        descricao
    )


def busca_projeto_orientador(nomeOrientador, ordem = 0, crescente = True):
    query = 'SELECT * FROM projetos WHERE nomeOrientador LIKE (%s) '
    
    nomeOrientador = '%' + nomeOrientador + '%'
    
    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        nomeOrientador
    )    


def grava_projeto(
    titulo, 
    nomeOrientador, 
    descricao, 
    nomeArquivo, 
    notaProj, 
    dataAvaliacao,
    codGer,
    codCurso):
    bd_conn.bd_gravar(
        'insert into projetos'+
        '(tituloProjeto,nomeOrientador,descricao,nomeArquivo,notaProjeto,dataAvaliacao,codGerenciador,codCurso,ativo)'+
        'values(%s,%s,%s,%s,%s,%s,%s,%s,1)',
        (titulo,nomeOrientador,descricao,nomeArquivo,notaProj,dataAvaliacao,codGer,codCurso)
    )

def ordena(ordem, crescente):
    cres = ""
    if(not crescente):
        cres = "DESC"

    elif(ordem == 0):
        return ''
    
    elif(ordem == 1):
        return 'ORDER BY likes  ' + cres
    
    elif(ordem == 2):
        return 'ORDER BY deslikes  ' + cres
    
    elif(ordem == 3):
        return 'ORDER BY numVisitas  ' + cres
    
    elif(ordem == 4):
        return 'ORDER BY numDownloads  ' + cres
    
    elif(ordem == 5):
        return 'ORDER BY dataAvaliacao ' + cres
    
    elif(ordem == 6):
        return 'ORDER BY dataEnvio  ' + cres
    
    elif(ordem == 7):
        return 'ORDER BY notaProjeto  ' + cres
    else:
        return ''
    
