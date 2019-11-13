from biblioteca.models.dao import projetos_dao
from biblioteca.util import json_res 
from werkzeug.exceptions import BadRequestKeyError
from flask import session, current_app as app
import os

ALLOWED_EXTENSIONS = set(['pdf'])

def busca(req = None, tipo = ''):
    dados, ordem, cres = __get_filtro(req)
    ret = None

    if tipo == 'titulo':
        ret = projetos_dao.busca_projeto_titulo(dados, ordem, cres)
    elif tipo == 'curso':
        ret = projetos_dao.busca_projeto_curso(dados, ordem, cres)
    elif tipo == 'descricao':
        ret = projetos_dao.busca_projeto_descricao(dados, ordem, cres)
    elif tipo == 'orientador':
        ret = projetos_dao.busca_projeto_orientador(dados, ordem, cres)
    elif tipo == 'autor':
        ret = projetos_dao.busca_projeto_autor(dados, ordem, cres)
    elif tipo == 'palavrasChave':
        ret = projetos_dao.busca_projeto_palavras_chave(dados, ordem, cres)
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

    ret = None

    if tipo == 'titulo':
        ret = projetos_dao.busca_projeto_titulo_pag(dados, ordem, cres, pag)
    elif tipo == 'curso':
        ret = projetos_dao.busca_projeto_curso_pag(dados, ordem, cres, pag)
    elif tipo == 'descricao':
        ret = projetos_dao.busca_projeto_descricao_pag(dados, ordem, cres, pag)
    elif tipo == 'orientador':
        ret = projetos_dao.busca_projeto_orientador_pag(dados, ordem, cres, pag)
    elif tipo == 'autor':
        ret = projetos_dao.busca_projeto_autor_pag(dados, ordem, cres, pag)
    elif tipo == 'palavrasChave':
        ret = projetos_dao.busca_projeto_palavras_chave_pag(dados, ordem, cres, pag)
    else:
        ret = projetos_dao.busca_projeto_titulo_pag(pag= pag)
    
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
        return projetos_dao.upload_projeto(req, session['username'])
            
    elif not allowed_file(req.files['file'].filename):
        return json_res.get_falha('Erro: extensão nao suportada')
    
    else:
        return json_res.get_erro('Um erro inesperado occoreu')

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

    ret = projetos_dao.projeto_existe(codProjeto)
    if ret:
        projetos_dao.prenche_projeto(ret)
        return json_res.get_data(ret)
    return json_res.get_falha('Projeto requisitado nao existe')

def edita_projeto(codProjeto, req):
    if not __cod_valido(codProjeto):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    
    if projetos_dao.projeto_existe(codProjeto):
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