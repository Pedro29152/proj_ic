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

from biblioteca import bd_conn
from biblioteca.models.dao import autores_dao, gerenciadores_dao, cursos_dao, projeto_autor_dao, palavras_chave_dao, orientadores_dao
from biblioteca.models.classes import Projetos, Avalicoes, Autores, Cursos, PalavrasChave, Gerenciadores, Orientadores
from datetime import date, datetime
from werkzeug.exceptions import BadRequestKeyError
from random import randint
from werkzeug.utils import secure_filename
import os

from flask import flash, current_app as app

QUERY_CURSO = 'SELECT * FROM projetos NATURAL JOIN cursos WHERE descricaoCurso LIKE (%s) OR abreviacao LIKE (%s) AND ativo = 1 '
QUERY_TITULO = 'SELECT * FROM projetos WHERE tituloProjeto LIKE (%s) AND ativo = 1 '
QUERY_DESCRICAO = 'SELECT * FROM projetos WHERE descricao LIKE (%s) AND ativo = 1 '
QUERY_ORIENTADOR = 'SELECT * FROM projetos WHERE nomeOrientador LIKE (%s) AND ativo = 1 '
QUERY_AUTOR = '''
    select distinct 
    codProjeto, tituloProjeto, nomeOrientador, descricao, nomeArquivo, likes, deslikes, 
    numVisitas, numDownloads, dataAvaliacao, dataEnvio, codGerenciador, codCurso, ativo
    from autores natural join projeto_autor natural join projetos pj where nomeAutor like (%s)
    '''
QUERY_PALAVRAS_CHAVE = '''
    select distinct 
    codProjeto, tituloProjeto, nomeOrientador, descricao, nomeArquivo, likes, deslikes, 
    numVisitas, numDownloads, dataAvaliacao, dataEnvio, codGerenciador, codCurso, ativo
    from palavras_chave natural join projetos pj where palavraChave like (%s)
    '''
    

def busca_projeto_curso(nomeCurso = '', ordem = 0, crescente = True):
    nomeCurso = '%' + nomeCurso + '%'

    ret = __busca_projeto_autor_palavra(
        QUERY_CURSO + 
        __ordena(ordem,crescente),
        (nomeCurso, nomeCurso)
    )
    
    #proj = get_proj_obj(ret)

    return ret
    
def busca_projeto_titulo(titulo = '', ordem = 0, crescente = True):
    titulo = "%" + titulo + "%"

    ret = __busca_projeto_autor_palavra(
        QUERY_TITULO + 
        __ordena(ordem,crescente),
        (titulo,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_descricao(descricao, ordem = 0, crescente = True):
    descricao = '%' + descricao + '%'

    ret = __busca_projeto_autor_palavra(
        QUERY_DESCRICAO + 
        __ordena(ordem,crescente),
        (descricao,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_orientador(nomeOrientador, ordem = 0, crescente = True):
    
    nomeOrientador = '%' + nomeOrientador + '%'
    
    ret = __busca_projeto_autor_palavra(
        QUERY_ORIENTADOR + 
        __ordena(ordem,crescente),
        (nomeOrientador,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_autor(nomeAutor, ordem = 0, crescente = True):
    
    nomeAutor = '%' + nomeAutor + '%'
    
    ret = __busca_projeto_autor_palavra(
        QUERY_AUTOR + __ordena(ordem,crescente),
        (nomeAutor,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_palavras_chave(palavra_chave, ordem = 0, crescente = True):
    palavra_chave = '%' + palavra_chave + '%'
    
    ret = __busca_projeto_autor_palavra(
        QUERY_PALAVRAS_CHAVE +
        __ordena(ordem, crescente),
        (palavra_chave,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto():
    query = 'select * from projetos where ativo = 1'

    ret = bd_conn.bd_busca(
        query,None
    )



    return ret

def busca_projeto_ranking(titulo, tipo, ordem):
    titulo = '%{}%'.format(titulo)
    
    query = 'select * from projetos where tituloProjeto like (%s) order by likes' + ordem
    
    if tipo == 'deslikes':
        query = 'select * from projetos where tituloProjeto like (%s) order by deslikes' + ordem

    if tipo == 'numVisitas':
        query = 'select * from projetos where tituloProjeto like (%s) order by numVisitas' + ordem

    if tipo == 'numDownloads':
        query = 'select * from projetos where tituloProjeto like (%s) order by numDownloads' + ordem

    if tipo == 'notaProjeto':
        query = 'select * from projetos where tituloProjeto like (%s) order by notaProjeto' + ordem
    
    return __busca_projeto_autor_palavra(query, (titulo,))

def get_cod_projeto_titulo(titulo):
    query = 'SELECT codProjeto FROM projetos WHERE tituloProjeto = (%s) ORDER BY codProjeto DESC'

    val = bd_conn.bd_busca_um(
        query, 
        (titulo,)
    )

    return val['codProjeto']

def get_proj_obj(ret):
    return Projetos(
        ret['codProjeto'],
        ret['tituloProjeto'],
        ret['nomeOrientador'],
        ret['descricao'],
        ret['nomeArquivo'],
        ret['notaProjeto'],
        date.strftime(ret['dataAvaliacao'], '%d/%m/%y'),
        date.strftime(ret['dataEnvio'], '%d/%m/%y'),
        Avalicoes(
            ret['likes'],
            ret['deslikes'],
            ret['numVisitas'],
            ret['numDownloads']
        ),
        gerenciadores_dao.busca_um_gerenciador_codGerenciador(ret['codGerenciador']),
        cursos_dao.busca_curso_cod(ret['codCurso']),
        autores_dao.busca_autores_proj(ret['codProjeto'])
    )  

def get_count():
    query = 'select count(codProjeto) as projetos from projetos'
    ret = bd_conn.bd_busca_um(query, None)
    return ret['projetos']

def __ordena(ordem, crescente):
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

def upload_projeto(req, nomeUsr):
    file = req.files['file']

    codGer = gerenciadores_dao.get_codGer_nomeUsuario(nomeUsr)

    try:
        titulo = req.form['titulo']
        nomeOrientador = req.form['nomeOrientador']
        raOrientador = req.form['raOrientador']
        descricao = req.form['descricao']
        dataAvaliacao = req.form['dataAvaliacao']
        codCurso = req.form['curso']
    except BadRequestKeyError:
        return {
            'status': 'erro',
            'message': 'A requisicao deve conter os campos "titulo", "nomeOrientador", "raOrientador", "descricao", "dataAvaliacao" e "curso"'
        }

    

    projeto = Projetos(
        tituloProjeto = titulo,
        descricao = descricao,
        dataAvaliacao = dataAvaliacao,
        autores=[], 
        palavrasChave=[],
        orientador= orientadores_dao.get_add_orientador(raOrientador, nomeOrientador),
        curso = cursos_dao.get_curso_codCurso(codCurso),
        gerenciador = gerenciadores_dao.get_gerenciador_cod_ger(codGer)
    )

    try:
        ra_autor = req.form['ra_autor']
        autor = req.form['autor']
    except BadRequestKeyError:
        return {
            'status' : 'erro',
            'message': 'A requisicao deve conter ao menos um campo "ra_autor" e um "autor"'
        }

    projeto.autores.append(Autores(
        ra_autor,
        autor
    ))

    i = 1
    try:
        while req.form['autor_' + str(i)] != None:
            nome = req.form['autor_' + str(i)]
            ra = req.form['ra_autor_' + str(i)]
            if(nome != '' and ra != ''):
                projeto.autores.append(
                    Autores(ra,nome)
                )
                i += 1
    except BadRequestKeyError:
       pass
    
    try:
        palavra = req.form['palavra_chave']
    except BadRequestKeyError:
        return {
            'status' : 'erro',
            'message': 'A requisicao deve conter ao menos um campo "palavra_chave". Os demais campos devem estar no formato: palavra_chave_(numero da palavra)'
        }

    projeto.palavrasChave.append(
        PalavrasChave(palavra)
    )
    j = 1
    try:
        while (req.form['palavra_chave_' + str(j)] != None):
            palavra = req.form['palavra_chave_' + str(j)]
            if(palavra != ''):
                projeto.palavrasChave.append(
                    PalavrasChave(palavra)
                )
                j += 1
    except BadRequestKeyError:
        None


    rand = hex(randint(0x100000,0xffffff))
    data = datetime.now().date()

    #-------------------------------------------------------------

    filename = secure_filename(file.filename)
    nfilename = filename.rsplit('.',2)[0]

    descricaoCurso = projeto.curso.descricaoCurso
    if len(descricaoCurso) >= 10:
        descricaoCurso = projeto.curso.abreviacao

    titulo = projeto.tituloProjeto
    if len(titulo) > 41:
        aux = titulo.split()
        titulo = ""
        for div in aux:
            titulo += div[0]

    filename = filename.replace(
        nfilename,
        descricaoCurso.upper().replace(' ', '-') + '-' +
        titulo.upper().replace(' ', '-') + '-' + 
        str(data) + "-" + str(rand).upper()
    )
    
    projeto.nomeArquivo = filename

    grava_projeto(
        projeto
    )

    file.save(
        os.path.join(
            app.config['UPLOAD_FOLDER'], 
            filename
        )
    )
    return {
        'status':'OK',
        'message': 'Projeto cadastrado com sucesso'
    }

def grava_projeto(
    projeto
):
    bd_conn.bd_gravar(
        'insert into projetos'+
        '(tituloProjeto, descricao, nomeArquivo, notaProjeto, dataAvaliacao, codGerenciador, codCurso, ativo)'+
        'values(%s,%s,%s,%s,%s,%s,%s,1)',
        (projeto.tituloProjeto, 
        projeto.descricao, 
        projeto.nomeArquivo, 
        projeto.notaProjeto, 
        projeto.dataAvaliacao,
        projeto.gerenciador.codGerenciador,
        projeto.curso.codCurso)
    )

    projeto.codProjeto = get_cod_projeto_titulo(projeto.tituloProjeto)
    
    for aut in projeto.autores:
        codAutor = aut.grava_autor(projeto.codProjeto)
        projeto_autor_dao.grava_autor_proj(projeto.codProjeto, codAutor)

    for palavra in projeto.palavrasChave:
        palavra.grava_palavra_chave(projeto.codProjeto)

    __grava_proj_ori(projeto.codProjeto, projeto.orientador.codOrientador)

    

def __busca_projeto_autor_palavra(query, *args):
    ret = bd_conn.bd_busca(query, *args)

    __prenche_projeto(ret)
    
    return ret

def __prenche_projeto(ret):
    for item in ret:
        item['autores'] = autores_dao.busca_autores_proj(item['codProjeto'])
        item['palavrasChave'] = palavras_chave_dao.busca_palavras_chave(item['codProjeto'])
        item['curso'] = cursos_dao.busca_curso_cod(item['codCurso'])
        item['orientadores'] = orientadores_dao.busca_orientadores_codProjeto(item['codProjeto'])

def __grava_proj_ori(codProjeto, codOrientador):
    query = 'insert into projeto_orientador values(%s, %s)'

    bd_conn.bd_gravar(query, (codOrientador, codProjeto))