from biblioteca.models.dao import projetos_dao
from biblioteca.util import json_res 
from flask import session, current_app as app
import os

ALLOWED_EXTENSIONS = set(['pdf'])

def busca(req = None, tipo = ''):
    dados, ordem, cres = __get_filtro(req)
    ret = None
    if tipo == 'titulo':
        ret = projetos_dao.busca_projeto_titulo(dados, ordem, cres)

    if tipo == 'curso':
        ret = projetos_dao.busca_projeto_curso(dados, ordem, cres)

    if tipo == 'descricao':
        ret = projetos_dao.busca_projeto_descricao(dados, ordem, cres)

    if tipo == 'orientador':
        ret = projetos_dao.busca_projeto_orientador(dados, ordem, cres)

    if tipo == 'autor':
        ret = projetos_dao.busca_projeto_autor(dados, ordem, cres)

    if tipo == 'palavrasChave':
        ret = projetos_dao.busca_projeto_palavras_chave(dados, ordem, cres)
    
    if ret:
        return json_res.get_data(ret)
    else:
        return json_res.get_falha('Tipo de pesquisa nao reconhecido')

def busca_pag(req = None, tipo='', pag = 1):
    dados, ordem, cres = __get_filtro(req)
    try:
        pag = int(pag)
    except ValueError:
        return json_res.get_erro('O valor do parametro "page" deve ser do tipo inteiro')

    ret = None
    if tipo == 'titulo':
        ret = projetos_dao.busca_projeto_titulo_pag(dados, ordem, cres, pag)

    if tipo == 'curso':
        ret = projetos_dao.busca_projeto_curso_pag(dados, ordem, cres, pag)

    if tipo == 'descricao':
        ret = projetos_dao.busca_projeto_descricao_pag(dados, ordem, cres, pag)

    if tipo == 'orientador':
        ret = projetos_dao.busca_projeto_orientador_pag(dados, ordem, cres, pag)

    if tipo == 'autor':
        ret = projetos_dao.busca_projeto_autor_pag(dados, ordem, cres, pag)

    if tipo == 'palavrasChave':
        ret = projetos_dao.busca_projeto_palavras_chave_pag(dados, ordem, cres, pag)
    
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
    
    try:
        page = int(page)
    except TypeError:
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
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    file = open(uploads + '/' + filename, 'r')
    return file

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