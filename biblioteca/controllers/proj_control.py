from biblioteca.models.dao import projetos_dao, gerenciadores_dao, cursos_dao, orientadores_dao
from biblioteca.models.classes import Projetos, Autores, Cursos, PalavrasChave, Gerenciadores, Orientadores
from random import randint
from werkzeug.utils import secure_filename
from datetime import date, datetime
from biblioteca.util import json_res 
from werkzeug.exceptions import BadRequestKeyError
from flask import session, current_app as app
import os

ALLOWED_EXTENSIONS = set(['pdf'])

def busca(req = None, tipo = ''):
    dados, ordem, cres = __get_filtro(req)

    if tipo:
        ret = projetos_dao.busca_projeto_tipo(tipo,dados,ordem,cres)
    else:
        ret = projetos_dao.busca_projeto()

    if ret:
        return json_res.get_data(ret)
    else:
        return json_res.get_falha('Nenhum projeto listado')

def busca_pag(req = None, tipo='', pag = 1):
    dados, ordem, cres = __get_filtro(req)
    try:
        pag = int(pag)
    except ValueError:
        return json_res.get_erro('O valor do parametro "page" deve ser do tipo inteiro')
    
    if tipo: 
        ret = projetos_dao.busca_projeto_tipo_pag(tipo,dados,ordem,cres)
    else:
        ret = projetos_dao.busca_projeto_pag(pag)

    if ret:
        return json_res.get_data(ret)
    else:
        return json_res.get_falha('Nenhum projeto listado')

def busca_ranking(req = None, pag = 1):    
    query, tipo, ordem = __get_filtro_rank(req)

    ret = projetos_dao.busca_projeto_ranking(query, tipo, ordem)

    if ret == None:
        return json_res.get_falha('Nenhum projeto listado')

    return json_res.get_data(ret)

def busca_ranking_pag(req = None, page = 1):
    query, tipo, ordem = __get_filtro_rank(req)
    
    if not __cod_valido(page):
        return json_res.get_erro('O valor do parametro "page" deve ser do tipo inteiro')

    ret = projetos_dao.busca_projeto_ranking_pag(query, tipo, ordem, page)

    if ret == None:
        return json_res.get_falha('Nenhum projeto listado')

    return json_res.get_data(ret)

def get_count():
    count = projetos_dao.get_count()
    return json_res.get_count(count)

def upload(req):
    if 'file' not in req.files:
        return json_res.get_falha('Nenhum arquivo foi enviado')

    if req.files['file'].filename == '':
        return json_res.get_falha('Nenhum arquivo selecionado')

    if req.files['file'] and allowed_file(req.files['file'].filename):
        return upload_projeto(req, session['username'])
            
    elif not allowed_file(req.files['file'].filename):
        return json_res.get_falha('Erro: extensão nao suportada')
    
    return json_res.get_erro('Um erro inesperado occoreu')

def upload_projeto(req, nomeUsr):
    file = req.files['file']

    codGer = gerenciadores_dao.get_codGer_nomeUsuario(nomeUsr)

    try:
        titulo = req.form['titulo']
        raOrientador = req.form['raOrientador']
        descricao = req.form['descricao']
        dataAvaliacao = req.form['dataAvaliacao']
        codCurso = req.form['curso']
        subTitulo = req.form['subTitulo']
    except BadRequestKeyError:
        return json_res.get_erro('A requisicao deve conter os campos "titulo", "raOrientador", "descricao", "dataAvaliacao", "subTitulo" e "curso"')

    if not(titulo and raOrientador and descricao and dataAvaliacao and codCurso and subTitulo):
        return json_res.get_erro('Os valores de "titulo", "raOrientador", "descricao", "dataAvaliacao", "subTitulo" e "curso" nao podem ser nulos')

    projeto = Projetos(
        tituloProjeto = titulo,
        subTitulo = subTitulo,
        descricao = descricao,
        dataAvaliacao = dataAvaliacao,
        autores=[], 
        palavrasChave=[],
        curso = cursos_dao.get_curso_codCurso(codCurso),
        gerenciador = gerenciadores_dao.get_gerenciador_cod_ger(codGer)
    )

    orientador= orientadores_dao.get_orientador(raOrientador)
    if not orientador:
        return json_res.get_falha('O codigo do orientador enviado e invalido')
    projeto.orientador = orientador

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

    try:
        i = 1
        while req.form['autor_' + str(i)] != None or i < 5:
            nome = req.form['autor_' + str(i)]
            ra = req.form['ra_autor_' + str(i)]
            if(nome and ra):
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

    try:
        j = 1
        while (req.form['palavra_chave_' + str(j)] != None or j < 3):
            palavra = req.form['palavra_chave_' + str(j)]
            if(palavra):
                projeto.palavrasChave.append(
                    PalavrasChave(palavra)
                )
                j += 1
    except BadRequestKeyError:
        pass
    
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

    ret = projetos_dao.grava_projeto(
        projeto
    )

    file.save(
        os.path.join(
            app.config['UPLOAD_FOLDER'], 
            filename
        )
    )

    return ret

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_arquivo(filename):
    codProj = projetos_dao.is_ativo_filename(filename)
    if codProj:
        projetos_dao.download_file(codProj)
        return True
    else:
        return False

def desativa_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')

    if projetos_dao.projeto_existe(codProjeto):
        projetos_dao.desativa_projeto(codProjeto)

        return json_res.get_ok('Projeto desativado com sucesso')
    return json_res.get_falha('Projeto requisitado nao existe')

def ativa_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')

    if projetos_dao.projeto_existe(codProjeto):
        projetos_dao.ativa_projeto(codProjeto)

        return json_res.get_ok('Projeto ativado com sucesso')
    return json_res.get_falha('Projeto requisitado nao existe')

def get_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')

    ret = projetos_dao.get_projeto(codProjeto)
    if ret:
        projetos_dao.prenche_projeto(ret)
        return json_res.get_data(ret)
    return json_res.get_falha('Projeto requisitado nao existe')

def edita_projeto(codProjeto, req):
    if not __cod_valido(codProjeto):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    
    if projetos_dao.get_projeto(codProjeto):
        try:
            titulo = req.form['tituloProjeto']
            descricao = req.form['descricao']
            subtitulo = req.form['subTitulo']
        except BadRequestKeyError:
            return json_res.get_erro('A requsicao deve ter os campos "tituloProjeto","descricao" e "subTitulo" em seu corpo')

        if titulo and descricao and subtitulo:
            projetos_dao.edita_projeto(codProjeto, titulo, descricao, subtitulo)
            return json_res.get_ok('Projeto editado com sucesso')
        return json_res.get_falha('Os campos enviados devem possuir algum valor')
    return json_res.get_falha('Projeto requisitado nao existe')

def __cod_valido(codProj):
    try:
        int(codProj)
        return True
    except ValueError:
        return False


def __get_filtro(req = None):
    
    desc = req.args.get('query')
    if not desc:
        desc = ''

    if req.args.get('ordem'):
        ordem = int(req.args.get('ordem'))
    else:
        ordem = 0
    
    cres = req.args.get('crescente')
    if cres:
        if(cres == '0'):
            cres = False
        else:
            cres = True
    else: 
        cres = True

    return desc, ordem, cres

def __get_filtro_rank(req = None):
    query = req.args.get('query')
    if not query :
        query = ''
    
    tipo = req.args.get('tipo')
    if not tipo:
        tipo = 'like'

    ordem = req.args.get('ordem')
    if ordem:
        if(not (ordem == '' or ordem == 'desc')):
            ordem = ''
    else:
        ordem = ''

    return query, tipo, ordem