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
from biblioteca.util import json_res
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

    ret = __busca_projeto_full(
        QUERY_CURSO + 
        __ordena(ordem,crescente),
        (nomeCurso, nomeCurso)
    )
    
    #proj = get_proj_obj(ret)

    return ret
    
def busca_projeto_titulo(titulo = '', ordem = 0, crescente = True):
    titulo = "%" + titulo + "%"

    ret = __busca_projeto_full(
        QUERY_TITULO + 
        __ordena(ordem,crescente),
        (titulo,)
    )

    return ret

def busca_projeto_descricao(descricao, ordem = 0, crescente = True):
    descricao = '%' + descricao + '%'

    ret = __busca_projeto_full(
        QUERY_DESCRICAO + 
        __ordena(ordem,crescente),
        (descricao,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_orientador(nomeOrientador, ordem = 0, crescente = True):
    
    nomeOrientador = '%' + nomeOrientador + '%'
    
    ret = __busca_projeto_full(
        QUERY_ORIENTADOR + __ordena(ordem,crescente)
        (nomeOrientador,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_autor(nomeAutor, ordem = 0, crescente = True):
    
    nomeAutor = '%' + nomeAutor + '%'
    
    ret = __busca_projeto_full(
        QUERY_AUTOR + __ordena(ordem,crescente),
        (nomeAutor,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_palavras_chave(palavra_chave, ordem = 0, crescente = True):
    palavra_chave = '%' + palavra_chave + '%'
    
    ret = __busca_projeto_full(
        QUERY_PALAVRAS_CHAVE +
        __ordena(ordem, crescente),
        (palavra_chave,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_curso_pag(nomeCurso = '', ordem = 0, crescente = True, pag = 1):
    nomeCurso = '%' + nomeCurso + '%'
    
    ret = __busca_projeto_full(
        QUERY_CURSO + __ordena(ordem,crescente) + __get_limit(pag),
        (nomeCurso, nomeCurso)
    )

    return ret
    
def busca_projeto_titulo_pag(titulo = '', ordem = 0, crescente = True, pag = 1):
    titulo = "%" + titulo + "%"


    ret = __busca_projeto_full(
        QUERY_TITULO + __ordena(ordem,crescente) + __get_limit(pag),
        (titulo,)
    )

    return ret

def busca_projeto_descricao_pag(descricao, ordem = 0, crescente = True, pag = 1):
    descricao = '%' + descricao + '%'


    ret = __busca_projeto_full(
        QUERY_DESCRICAO + __ordena(ordem,crescente) + __get_limit(pag),
        (descricao,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_orientador_pag(nomeOrientador, ordem = 0, crescente = True, pag = 1):
    
    nomeOrientador = '%' + nomeOrientador + '%'
    
    ret = __busca_projeto_full(
        QUERY_ORIENTADOR + __ordena(ordem,crescente) + __get_limit(pag),
        (nomeOrientador,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_autor_pag(nomeAutor, ordem = 0, crescente = True, pag = 1):
    
    nomeAutor = '%' + nomeAutor + '%'
    
    ret = __busca_projeto_full(
        QUERY_AUTOR + __ordena(ordem,crescente) + __get_limit(pag),
        (nomeAutor,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto_palavras_chave_pag(palavra_chave, ordem = 0, crescente = True, pag = 1):
    palavra_chave = '%' + palavra_chave + '%'
    
    ret = __busca_projeto_full(
        QUERY_PALAVRAS_CHAVE + __ordena(ordem, crescente) + __get_limit(pag),
        (palavra_chave,)
    )

    #proj = get_proj_obj(ret)
    
    return ret

def busca_projeto():
    query = 'select * from projetos where ativo = 1'

    ret = bd_conn.bd_busca(
        query,None
    )

    prenche_projetos(ret)

    return ret

def busca_projeto_ranking(titulo, tipo, ordem):
    titulo = '%{}%'.format(titulo)
    
    query = 'select * from projetos where tituloProjeto like (%s) and ativo = 1'
    
    if tipo == 'likes':
        query += ' order by likes' + ordem
    if tipo == 'deslikes':
        query += ' order by deslikes' + ordem
    elif tipo == 'numVisitas':
        query += 'order by numVisitas' + ordem
    elif tipo == 'numDownloads':
        query += 'order by numDownloads' + ordem
    elif tipo == 'notaProjeto':
        query += 'order by notaProjeto' + ordem
    else:
        query += ' order by likes' + ordem

    return __busca_projeto_full(query, (titulo,))

def busca_projeto_ranking_pag(titulo, tipo, ordem, pag):
    titulo = '%{}%'.format(titulo)

    query = 'select * from projetos where tituloProjeto like (%s) and ativo = 1'
    
    if tipo == 'likes':
        query += ' order by likes' + ordem
    if tipo == 'deslikes':
        query += ' order by deslikes' + ordem
    elif tipo == 'numVisitas':
        query += 'order by numVisitas' + ordem
    elif tipo == 'numDownloads':
        query += 'order by numDownloads' + ordem
    elif tipo == 'notaProjeto':
        query += 'order by notaProjeto' + ordem
    else:
        query += ' order by likes' + ordem

    query += __get_limit(pag, 5)

    return __busca_projeto_full(query, (titulo,))

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
    query = 'select count(*) as projetos from projetos'
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
        subTitulo = req.form['subTitulo']
    except BadRequestKeyError:
        return json_res.get_erro('A requisicao deve conter os campos "titulo", "nomeOrientador", "raOrientador", "descricao", "dataAvaliacao", "subTitulo" e "curso"')

    if not(titulo and nomeOrientador and raOrientador and descricao and dataAvaliacao and codCurso and subTitulo):
        return json_res.get_erro('Os valores de "titulo", "nomeOrientador", "raOrientador", "descricao", "dataAvaliacao", "subTitulo" e "curso" nao podem ser nulos')

    projeto = Projetos(
        tituloProjeto = titulo,
        subTitulo = subTitulo,
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
        return json_res.get_erro('A requisicao deve conter ao menos um campo "ra_autor" e um "autor"')

    if not (ra_autor and autor):
        return json_res.get_erro('Os valores de "ra_autor" e "autor" nao podem ser nulos')

    projeto.autores.append(Autores(
        ra_autor,
        autor
    ))

    i = 1
    try:
        while req.form['autor_' + str(i)] != None or i < 4:
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
        return json_res.get_erro('A requisicao deve conter ao menos um campo "palavra_chave". Os demais campos devem estar no formato: palavra_chave_(numero da palavra)')

    if not palavra:
        return json_res.get_erro('O valor de "palavra_chave" nao pode ser nulo')

    projeto.palavrasChave.append(
        PalavrasChave(palavra)
    )
    j = 1
    try:
        while (req.form['palavra_chave_' + str(j)] != None or j < 3):
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
    return json_res.get_ok('Projeto cadastrado com sucesso')

def grava_projeto(
    projeto
):
    bd_conn.bd_gravar(
        'insert into projetos'+
        '(tituloProjeto, subTitulo, descricao, nomeArquivo, notaProjeto, dataAvaliacao, codGerenciador, codCurso, ativo)'+
        'values(%s,%s,%s,%s,%s,%s,%s,%s,1)',
        (projeto.tituloProjeto,
        projeto.subTitulo,
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

def projeto_existe(codProjeto):
    query = 'select * from projetos where codProjeto = (%s)'
    ret = bd_conn.bd_busca_um(query,(codProjeto,))
    if ret:
        return ret
    return None

def desativa_projeto(codProjeto):
    query = 'update projetos set ativo = 0 where codProjeto = (%s)'

    bd_conn.bd_gravar(query, (codProjeto,))

def ativa_projeto(codProjeto):
    query = 'update projetos set ativo = 1 where codProjeto = (%s)'

    bd_conn.bd_gravar(query, (codProjeto,))

def edita_projeto(codProjeto, titulo, descricao, subtitulo):
    query = 'update projetos set tituloProjeto = (%s), descricao = (%s), subTitulo = (%s) where codProjeto = (%s)'

    bd_conn.bd_gravar(query, (titulo, descricao, subtitulo, codProjeto))

def is_ativo_filename(filename):
    query = 'select codProjeto from projetos where nomeArquivo = (%s) and ativo = 1'

    ret = bd_conn.bd_busca_um(query, (filename,))

    if ret:
        return ret['codProjeto']
    return None

def download_file(codProjeto):
    query = 'UPDATE projetos SET numDownloads = numDownloads + 1 WHERE codProjeto = (%s)'

    bd_conn.bd_gravar(query, (codProjeto,))

def __busca_projeto_full(query, *args):
    ret = bd_conn.bd_busca(query, *args)

    prenche_projetos(ret)
    
    return ret

def prenche_projetos(ret):
    for item in ret:
        item['autores'] = autores_dao.busca_autores_proj(item['codProjeto'])
        item['palavrasChave'] = palavras_chave_dao.busca_palavras_chave(item['codProjeto'])
        item['curso'] = cursos_dao.busca_curso_cod(item['codCurso'])
        item['orientadores'] = orientadores_dao.busca_orientadores_codProjeto(item['codProjeto'])

def prenche_projeto(ret):
    ret['autores'] = autores_dao.busca_autores_proj(ret['codProjeto'])
    ret['palavrasChave'] = palavras_chave_dao.busca_palavras_chave(ret['codProjeto'])
    ret['curso'] = cursos_dao.busca_curso_cod(ret['codCurso'])
    ret['orientadores'] = orientadores_dao.busca_orientadores_codProjeto(ret['codProjeto'])

def __grava_proj_ori(codProjeto, codOrientador):
    query = 'insert into projeto_orientador values(%s, %s)'

    bd_conn.bd_gravar(query, (codOrientador, codProjeto))

def __get_limit(pag, tam = 20):
    fi = 1 + ((pag - 1) * tam)
    ff = pag * tam

    return ' LIMIT {}, {}'.format(fi, ff)
    