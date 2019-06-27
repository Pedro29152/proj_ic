from biblioteca import bd_conn
from biblioteca.cls.autor import autor_bd
from biblioteca.cls.curso.curso_bd import get_codCurso, get_abbr_curso
from biblioteca.cls.gerenciador.gerenciador_bd import get_codGer_usr
from random import randint
import datetime, os
from werkzeug.utils import secure_filename
from biblioteca import app
from werkzeug.exceptions import BadRequestKeyError

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
    Por padrao ordem recebe o valor 0

    Caso crescente for True ele ordena de ordem crescente
    Caso crescente for False ele ordena de ordem decrescente
    Por padrao crescente recebe o valor True
    '''
    query = 'SELECT * FROM projetos WHERE tituloProjeto LIKE (%s) AND ativo = 1 '

    titulo = "%" + titulo + "%"

    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente),
        (titulo,)
    )

def busca_projeto_curso(nomeCurso = '', ordem = 0, crescente = True):
    query = 'SELECT * FROM projetos NATURAL JOIN cursos WHERE descricaoCurso LIKE (%s) AND ativo = 1 '

    nomeCurso = '%' + nomeCurso + '%'

    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        (nomeCurso,)
    )
        
def busca_projeto_descricao(descricao, ordem = 0, crescente = True):
    query = 'SELECT * FROM projetos WHERE descricao LIKE (%s) AND ativo = 1 '

    descricao = '%' + descricao + '%'

    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        (descricao,)
    )

def busca_projeto_orientador(nomeOrientador, ordem = 0, crescente = True):
    query = 'SELECT * FROM projetos WHERE nomeOrientador LIKE (%s) AND ativo = 1 '
    
    nomeOrientador = '%' + nomeOrientador + '%'
    
    return bd_conn.bd_busca(
        query +
        ordena(ordem, crescente), 
        (nomeOrientador,)
    )    

def busca_cod_projeto(titulo):
    query = 'SELECT codProjeto FROM projetos WHERE tituloProjeto = (%s) ORDER BY codProjeto DESC'

    val = bd_conn.bd_busca_um(
        query, 
        (titulo,)
    )

    return val

def grava_projeto(
    titulo, 
    nomeOrientador, 
    descricao, 
    nomeArquivo,
    dataAvaliacao,
    codGer,
    codCurso,
    autor,
    palavrasChave
):
    bd_conn.bd_gravar(
        'insert into projetos'+
        '(tituloProjeto, nomeOrientador, descricao, nomeArquivo, dataAvaliacao, codGerenciador, codCurso, ativo)'+
        'values(%s,%s,%s,%s,%s,%s,%s,1)',
        (titulo, nomeOrientador, descricao, nomeArquivo, dataAvaliacao, codGer, codCurso)
    )

    codProjeto = busca_cod_projeto(titulo)['codProjeto']
    
    for aut in autor:
        autor_bd.grava_autor(str(aut['nome']), str(aut['ra']), codProjeto)

    for palavra in palavrasChave:
        grava_palavra_chave(palavra, codProjeto)

def grava_palavra_chave(palavra, codProjeto):
    val = bd_conn.bd_busca_um(
        'SELECT codPalavra FROM palavras_chave WHERE palavraChave = %s AND codProjeto = %s',
        (palavra, codProjeto)
    )
    if(val == None):
        bd_conn.bd_gravar(
            'INSERT INTO palavras_chave(palavraChave, codProjeto) values(%s, %s)',
            (palavra, codProjeto)
        )

def upload_projeto(req, nomeGer):
    titulo = req.form['titulo']
    nomeOrientador = req.form['nomeOrientador']
    descricao = req.form['descricao']
    dataAvaliacao = req.form['dataAvaliacao']
    curso = req.form['curso']
    file = req.files['file']
    
    autor = []
    autor.append({
        'nome': req.form['autor'], 
        'ra':   req.form['ra_autor']
    })


    i = 1
    try:
        while req.form['autor_' + str(i)] != None:
            nome = req.form['autor_' + str(i)]
            ra = req.form['ra_autor_' + str(i)]
            if(autor != '' and ra != ''):
                autor.append({
                    'nome': nome,
                    'ra':   ra
                })
                i += 1
    except BadRequestKeyError:
        None

    palavrasChave = []
    palavrasChave.append(req.form['palavra_chave'])
    j = 1
    try:
        while (req.form['palavra_chave_' + str(j)] != None):
            palavra = req.form['palavra_chave_' + str(j)]
            if(palavra != ''):
                palavrasChave.append(palavra)
                j += 1
    except BadRequestKeyError:
        None

    codCurso = get_codCurso(curso)

    rand = hex(randint(0x100000,0xffffff))
    data = datetime.datetime.now()
    data = data.date()

    filename = secure_filename(file.filename)
    nfilename = filename.rsplit('.',2)[0]

    if len(curso) >= 10:
        curso = get_abbr_curso(curso)

    tituloarq = titulo
    if len(titulo) > 41:
        aux = titulo.split()
        tituloarq = ""
        for div in aux:
            tituloarq += div[0]

    filename = filename.replace(
        nfilename, 
        curso.upper().replace(' ', '-') + '-' +
        tituloarq.upper().replace(' ', '-') + '-' + 
        str(data) + "-" + str(rand).upper()
    )
    
    codGer = get_codGer_usr(nomeGer)
    
    grava_projeto(
        titulo, nomeOrientador, descricao,
        filename, dataAvaliacao, 
        codGer, codCurso, autor, palavrasChave
    )

    file.save(
        os.path.join(
            app.config['UPLOAD_FOLDER'], 
            filename
        )
    )
    return True


def ordena(ordem, crescente):
    cres = ''
    if(not crescente):
        cres = 'DESC'

    if(ordem == 0):
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
    else:
        return ''
    
