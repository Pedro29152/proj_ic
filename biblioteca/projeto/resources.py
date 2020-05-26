import os

from flask_restful import Resource
from flask import request, jsonify, send_from_directory, abort, current_app as app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from datetime import date, datetime
from random import randint
from PyPDF2 import PdfFileReader, PdfFileWriter

from biblioteca.curso import cursos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.responses import (
    get_data,
    get_falha,
    get_erro,
    get_ok,
    get_count as get_res_count
)
from biblioteca.extensions import(
    admin_token_required,
    token_required
)
from . import projetos_dao
from .schemas import Projetos, Autores, PalavrasChave

ALLOWED_EXTENSIONS = set(['pdf'])

class BuscaProjetoResource(Resource):
    #Parametros: "query", "ordem" e "crescente"
    def get(self, id=None):
        projs = None
        cod = 200
        if request.args.get('page'):
            page = request.args.get('page')
            projs, cod = busca_pag(request, id, page)
        else:
            projs, cod = busca(request, id)
        
        resp = jsonify(projs)
        resp.status_code = cod
        return resp

class UploadProjetoResource(Resource):
    @token_required
    def post(self):
        status, cod = upload(request)

        resp = jsonify(status)
        resp.status_code = cod
        return resp

class AlteraProjetoResource(Resource):
    @admin_token_required
    def put(self, id):
        status, cod = edita_projeto(id, request)
    
        resp = jsonify(status)
        resp.status_code = cod
        return resp

class GetProjetoResource(Resource):
    def get(self, id):
        status, cod = get_projeto(id)
        
        resp = jsonify(status)
        resp.status_code = cod
        return resp

class BuscaRankingResource(Resource):
    def get(self):
        projs = None
        cod = 200
        if request.args.get('page'):
            page = request.args.get('page')
            projs, cod = busca_ranking_pag(request, page)
        else:
            projs, cod = busca_ranking(request)

        resp = jsonify(projs)
        resp.status_code = cod
        return resp

class DownloadArquivoProjetoResource(Resource):
    def get(self, filename):
        attatch = False
        if request.args.get('as_attachment'):
            attatch = True if request.args.get('as_attachment').lower() == 'true' else False

        if download_arquivo(filename):
            f = send_from_directory(    
                    app.config['UPLOAD_FOLDER'],
                    filename, 
                    as_attachment=attatch
                )

            return f
        
        abort(404)

class CountProjetosResource(Resource):
    def get(self):
        status, cod = get_count()
    
        resp = jsonify(status)
        resp.status_code = cod
        return resp

class DesativaProjetoResource(Resource):
    @admin_token_required
    def delete(self, id):
        status, cod = desativa_projeto(id)
        
        resp = jsonify(status)
        resp.status_code = cod
        return resp

class AtivaProjetoResource(Resource):
    @admin_token_required
    def post(self, id):
        status, cod = ativa_projeto(id)
        
        resp = jsonify(status)
        resp.status_code = cod
        return resp


def busca(req = None, tipo = ''):
    dados, ordem, cres = __get_filtro(req)

    if tipo:
        ret = projetos_dao.busca_projeto_tipo(tipo,dados,ordem,cres)
    else:
        ret = projetos_dao.busca_projeto()

    if ret:
        return get_data(ret), 200
    else:
        return get_falha('Nenhum projeto listado'), 404

def busca_pag(req = None, tipo='', pag = 1):
    dados, ordem, cres = __get_filtro(req)
    try:
        pag = int(pag)
    except ValueError:
        return get_erro('O valor do parametro "page" deve ser do tipo inteiro'), 404
    
    if tipo: 
        ret = projetos_dao.busca_projeto_tipo_pag(tipo,dados,ordem,cres)
    else:
        ret = projetos_dao.busca_projeto_pag(pag)

    if ret:
        return get_data(ret), 200
    else:
        return get_falha('Nenhum projeto listado'), 404

def upload(req):
    if 'file' not in req.files:
        return get_falha('Nenhum arquivo foi enviado'), 400

    if req.files['file'].filename == '':
        return get_falha('Nenhum arquivo selecionado'), 400

    if req.files['file'] and __allowed_file(req.files['file'].filename):
        return upload_projeto(req)
            
    elif not __allowed_file(req.files['file'].filename):
        return get_falha('Erro: extensão nao suportada'), 415
    
    return get_erro('Um erro inesperado occoreu'), 500

def upload_projeto(req):
    file = req.files['file']

    try:
        titulo = req.form['titulo']
        raOrientador = req.form['raOrientador']
        descricao = req.form['descricao']
        dataAvaliacao = req.form['dataAvaliacao']
        codCurso = req.form['curso']
        subTitulo = req.form['subTitulo']
    except BadRequestKeyError:
        return get_erro('A requisicao deve conter os campos "titulo", "raOrientador", "descricao", "dataAvaliacao", "subTitulo" e "curso"'), 400

    if not(titulo and raOrientador and descricao and dataAvaliacao and codCurso and subTitulo):
        return get_erro('Os valores de "titulo", "raOrientador", "descricao", "dataAvaliacao", "subTitulo" e "curso" nao podem ser nulos'), 400
    
    try:
        projeto = Projetos(
            tituloProjeto = titulo,
            subTitulo = subTitulo,
            descricao = descricao,
            dataAvaliacao = dataAvaliacao,
            autores=[], 
            palavrasChave=[],
            curso = cursos_dao.get_curso_codCurso(codCurso)
        )
    except Warning:
        return get_erro('O campo "curso" deve conter um codigo de curso existente'), 400


    orientador= orientadores_dao.get_orientador(raOrientador)
    if not orientador:
        return get_falha('O codigo do orientador enviado e invalido'), 400
    projeto.orientador = orientador

    try:
        ra_autor = req.form['ra_autor']
        autor = req.form['autor']
    except BadRequestKeyError:
        return get_erro('A requisicao deve conter ao menos um campo "ra_autor" e um "autor"'), 400

    if not (ra_autor and autor):
        return get_erro('Os valores de "ra_autor" e "autor" nao podem ser nulos'), 400

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
        return get_erro('A requisicao deve conter ao menos um campo "palavra_chave". Os demais campos devem estar no formato: palavra_chave_(numero da palavra)'), 400

    if not palavra:
        return get_erro('O valor de "palavra_chave" nao pode ser nulo'), 400

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
        str(data) + "-" + str(rand).upper().replace('0X','')
    )
    
    projeto.nomeArquivo = filename

    ret = projetos_dao.grava_projeto(
        projeto
    )

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'], 
        filename
    )
    file.save(
        filepath
    )

    capa = os.path.join(app.static_folder, 'Capa.pdf')

    __adicionar_cabecalio([capa, filepath], filepath)

    return ret

def download_arquivo(filename):
    codProj = projetos_dao.is_ativo_filename(filename)
    if codProj:
        projetos_dao.download_file(codProj)
        return True
    else:
        return False

def desativa_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 404

    if projetos_dao.projeto_existe(codProjeto):
        projetos_dao.desativa_projeto(codProjeto)

        return get_ok('Projeto desativado com sucesso'), 200
    return get_falha('Projeto requisitado nao existe'), 404

def ativa_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 404

    if projetos_dao.projeto_existe(codProjeto):
        projetos_dao.ativa_projeto(codProjeto)

        return get_ok('Projeto ativado com sucesso'), 200
    return get_falha('Projeto requisitado nao existe'), 404

def edita_projeto(codProjeto, req):
    if not __cod_valido(codProjeto):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400
    
    if projetos_dao.get_projeto(codProjeto):
        try:
            titulo = req.form['tituloProjeto']
            descricao = req.form['descricao']
            subtitulo = req.form['subTitulo']
        except BadRequestKeyError:
            return get_erro('A requsicao deve ter os campos "tituloProjeto","descricao" e "subTitulo" em seu corpo (deixe em branco para manter inalterado)'), 400

        if titulo:
            projetos_dao.edita_titulo(codProjeto, titulo)
        if descricao:
            projetos_dao.edita_descricao(codProjeto, descricao)
        if subtitulo:
            projetos_dao.edita_subtitulo(codProjeto, subtitulo)
        
        return get_ok('Projeto editado com sucesso'), 200
    return get_falha('Projeto requisitado nao existe'), 404

def get_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400

    ret = projetos_dao.get_projeto(codProjeto)
    if ret:
        projetos_dao.prenche_projeto(ret)
        projetos_dao.add_view(codProjeto)
        return get_data(ret), 200
    return get_falha('Projeto requisitado nao existe'), 404

def busca_ranking(req = None):    
    query, tipo, ordem = __get_filtro_rank(req)

    ret = projetos_dao.busca_projeto_ranking(query, tipo, ordem)

    if ret == None:
        return get_falha('Nenhum projeto listado'), 404

    return get_data(ret), 200

def busca_ranking_pag(req = None, page = 1):
    query, tipo, ordem = __get_filtro_rank(req)
    
    if not __cod_valido(page):
        return get_erro('O valor do parametro "page" deve ser do tipo inteiro'), 404

    ret = projetos_dao.busca_projeto_ranking_pag(query, tipo, ordem, page)

    if ret == None:
        return get_falha('Nenhum projeto listado'), 404

    return get_data(ret), 200

def get_count():
    count = projetos_dao.get_count()
    return get_res_count(count), 200

def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
def __adicionar_cabecalio(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)
