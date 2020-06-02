import os, json

from json.decoder import JSONDecodeError
from flask_restful import Resource
from flask import request, jsonify, send_from_directory, abort, current_app as app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from datetime import date, datetime
from random import randint
from PyPDF2 import PdfFileReader, PdfFileWriter
from mysql.connector.errors import IntegrityError

from biblioteca.curso import cursos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.responses import (
    get_data,
    get_falha,
    get_erro,
    get_ok,
    get_count as get_res_count,
    get_bad_request,
    get_response_code
)
from biblioteca.extensions import(
    admin_token_required,
    secretaria_token_required,
    aluno_token_required,
    is_valid_email,
    TiposUsuario
)
from . import projetos_dao
from .schemas import Projetos, Autores, PalavrasChave

ALLOWED_EXTENSIONS = set(['pdf'])

class BuscaProjetoResource(Resource):
    #Parametros: "query", "ordem", "crescente" e "page"
    def get(self, id=None):
        projs = None
        cod = 200
        if request.args.get('page'):
            page = request.args.get('page')
            projs, cod = busca_pag(id, page)
        else:
            projs, cod = busca(id)
        
        resp = jsonify(projs)
        resp.status_code = cod
        return resp

class UploadProjetoResource(Resource):
    @secretaria_token_required
    def post(self):
        r, code = check_file()
        if r:
            return get_response_code(r, code)
        data, cod = upload_projeto()
        return get_response_code(data, cod)

class UploadProjetoAlunoResource(Resource):
    @aluno_token_required
    def post(self, user_info):
        r, code = check_file()
        if r:
            return get_response_code(r, code)
        data, cod = upload_projeto(user_info)
        return get_response_code(data, cod)


class AlteraProjetoResource(Resource):
    @admin_token_required
    def put(self, id):
        status, cod = edita_projeto(id)
    
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
            projs, cod = busca_ranking_pag(page)
        else:
            projs, cod = busca_ranking()

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


def busca(tipo = ''):
    dados, ordem, cres = __get_filtro()

    if tipo:
        ret = projetos_dao.busca_projeto_tipo(tipo,dados,ordem,cres)
    else:
        ret = projetos_dao.busca_projeto()

    if ret:
        return get_data(ret), 200
    else:
        return get_falha('Nenhum projeto listado'), 204

def busca_pag(tipo='', pag = 1):
    dados, ordem, cres = __get_filtro()
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
        return get_falha('Nenhum projeto listado'), 204

def check_file():
    if 'file' not in request.files:
        return get_falha('Nenhum arquivo foi enviado'), 400

    if request.files['file'].filename == '':
        return get_falha('Nenhum arquivo selecionado'), 400

    if not __allowed_file(request.files['file'].filename):
        return get_falha('Erro: extensão nao suportada'), 415
    
    if request.files['file']:
        return None, None
            
    return get_erro('Um erro inesperado occoreu'), 500

def upload_projeto(user_info=None):
    try:
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        dataAvaliacao = request.form['dataAvaliacao']
        codCurso = request.form['codCurso']
        subTitulo = request.form['subTitulo']
        if user_info == None:
            raOrientador = request.form['raOrientador']
        else:
            raOrientador = orientadores_dao.get_orientador_orientando_codUsuario(user_info['codUsuario'])
            if not raOrientador:
                return get_erro('O usuario sendo utilizado nao possui um orientador relacionado consigo mesmo, contate a secretaria ou seu orientador para efetuar o cadastro')
            
        autores = request.form['autores']
        palavras = request.form['palavras_chave']
    except BadRequestKeyError:
        return get_erro('A requisicao deve conter os campos "titulo", {}"descricao", "dataAvaliacao", "subTitulo", "autores", "palavras_chave" e "codCurso"'.format('"raOrientador", ' if user_info==None else '')), 400


    if not(titulo and raOrientador and descricao and dataAvaliacao and 
            codCurso and subTitulo):
        return get_erro('Os valores de "titulo", ' + '"raOrientador", ' if user_info==None else '' + '"descricao", "dataAvaliacao", "subTitulo" e "curso" nao podem ser nulos'), 400

    projeto = Projetos(
        tituloProjeto = titulo,
        subTitulo = subTitulo,
        descricao = descricao,
        dataAvaliacao = dataAvaliacao,
        autores = [], 
        palavrasChave = [],
        curso = cursos_dao.get_curso_codCurso(codCurso),
        orientador = orientadores_dao.get_orientador(raOrientador)
    )
    
    if not projeto.curso:
        return get_erro('O campo "curso" deve conter um codigo de curso existente'), 400
    if not projeto.orientador:
        return get_falha('O codigo do orientador enviado e invalido'), 400
    
    try:
        autores_obj = json.loads(autores)
    except JSONDecodeError:
        return get_erro('O campo "autores" deve ser um array contendo objetos JSON com os campos: "nome", "ra" e "email"'), 400
    try:
        palavras_obj = json.loads(palavras)
    except JSONDecodeError:
        return get_erro('O campo "palavras_chave" deve ser um array contendo objetos JSON com o campo: "palavra"'), 400

    if len(autores_obj) < 1:
        return get_erro('Cada projeto deve ter no mínimo 1 autor'), 400
    if len(palavras_obj) < 1:
        return get_erro('Cada projeto deve ter no mínimo 1 palavra-chave'), 400
    if len(autores_obj) > 5:
        return get_erro('Cada projeto deve ter no máximo 5 autores'), 400
    if len(palavras_obj) > 5:
        return get_erro('Cada projeto deve ter no máximo 5 palavras-chave'), 400 

    for item in autores_obj:
        if item['nome'] and item['ra'] and item['email']:
            if not is_valid_email(item['email']):
                return get_erro('Os campos "email" de autores devem ser emails validos'), 400
            projeto.autores.append(Autores(item['ra'], item['nome'], item['email']))
        else:
            return get_erro('Os objetos de autor devem conter os campos "nome", "ra" e "email"'), 400
    for item in palavras_obj:
        if item['palavra']:
            projeto.palavrasChave.append(PalavrasChave(item['palavra']))
        else:
            return get_erro('Os objetos de palavra chave devem conter o campo "palavra"'), 400

    file = request.files['file']
    filename = __get_nome_arquivo_projeto(titulo, file.filename, projeto.curso.abreviacao)
    
    projeto.nomeArquivo = filename
    ret, cod = projetos_dao.grava_projeto(
        projeto
    )

    if cod == 200: 
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], 
            filename
        )
        file.save(
            filepath
        )

        capa = os.path.join(app.static_folder, 'Capa.pdf')
        __adicionar_cabecalio([capa, filepath], filepath)

    return ret, cod

# def upload_projeto_aluno():
#     #ja vem: dados do autor lider e orientador
#     #precisa: dados de outros autores, curso e palavras chave
#     pass

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

def edita_projeto(codProjeto):
    if not __cod_valido(codProjeto):
        return get_erro('O valor enviado deve ser do tipo inteiro'), 400
    
    if projetos_dao.get_projeto(codProjeto):
        try:
            titulo = request.form['tituloProjeto']
            descricao = request.form['descricao']
            subtitulo = request.form['subTitulo']
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

def busca_ranking():
    query, tipo, ordem = __get_filtro_rank()

    ret = projetos_dao.busca_projeto_ranking(query, tipo, ordem)

    if ret == None:
        return get_falha('Nenhum projeto listado'), 204

    return get_data(ret), 200

def busca_ranking_pag(page = 1):
    query, tipo, ordem = __get_filtro_rank()
    
    if not __cod_valido(page):
        return get_erro('O valor do parametro "page" deve ser do tipo inteiro'), 404

    ret = projetos_dao.busca_projeto_ranking_pag(query, tipo, ordem, page)

    if ret == None:
        return get_falha('Nenhum projeto listado'), 204

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
def __get_filtro():
    desc = request.args.get('query')
    if not desc:
        desc = ''

    if request.args.get('ordem'):
        ordem = int(request.args.get('ordem'))
    else:
        ordem = 0
    
    cres = request.args.get('crescente')
    if cres:
        if(cres == '0'):
            cres = False
        else:
            cres = True
    else: 
        cres = True

    return desc, ordem, cres
def __get_filtro_rank():
    query = request.args.get('query')
    if not query :
        query = ''
    
    tipo = request.args.get('tipo')
    if not tipo:
        tipo = 'like'

    ordem = request.args.get('ordem')
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
def __get_nome_arquivo_projeto(titulo_projeto, nome_arquivo, curso):
    rand = hex(randint(0x100000,0xffffff))
    data = datetime.now().date()

    filename = secure_filename(nome_arquivo)
    nfilename = filename.rsplit('.',2)[0]

    descricaoCurso = curso

    titulo = titulo_projeto
    if len(titulo) > 41:
        aux = titulo.split()
        titulo = ""
        for div in aux:
            titulo += div[0]

    filename = filename.replace(
        nfilename,
        descricaoCurso.replace(' ', '-') + '-' +
        titulo.replace(' ', '-') + '-' + 
        str(data) + "-" + str(rand).replace('0X','')
    )
    return filename.upper()

