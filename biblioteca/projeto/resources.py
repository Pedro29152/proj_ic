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

from biblioteca import mailer
from biblioteca.usuarios import usuario_orientado_dao
from biblioteca.curso import cursos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.autor import autores_dao, projeto_autor_dao
from biblioteca.responses import (
    get_data,
    get_falha,
    get_erro,
    get_ok,
    get_count as get_res_count,
    get_bad_request,
    get_response_code,
    get_not_found
)
from biblioteca.extensions import(
    admin_token_required,
    secretaria_token_required,
    aluno_token_required,
    professor_token_required,
    coordenador_token_required,
    professor_coordenador_secretaria_token_required,
    is_valid_email,
    TiposUsuario,
    LinguagemProjeto
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
        
        return get_response_code(projs, cod)

class BuscaRankingResource(Resource):
    def get(self):
        projs = None
        cod = 200
        if request.args.get('page'):
            page = request.args.get('page')
            projs, cod = busca_ranking_pag(page)
        else:
            projs, cod = busca_ranking()

        return get_response_code(projs, cod)

class BuscarProjetosOrientador(Resource):
    @professor_token_required
    def get(self, user_info):
        orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
        if not orientador:
            return get_bad_request('O usuario sendo utilizado nao possui um orientador relacionado consigo mesmo, contate a secretaria para efetuar o cadastro')

        res, cod = busca_projetos_orientador(orientador['codOrientador'])
        return get_response_code(res, cod)

class BuscarProjetosCurso(Resource):
    @coordenador_token_required
    def get(self, user_info):
        curso = cursos_dao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
        if not curso:
            return get_bad_request('O usuario sendo utilizado nao possui um curso relacionado consigo mesmo, contate a secretaria para efetuar o cadastro')

        res, cod = busca_projetos_curso(curso['codCurso'])
        return get_response_code(res, cod)

class GetProjetoOrientador(Resource):
    @professor_token_required
    def get(self, user_info, id):
        orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
        if not orientador:
            return get_bad_request('O usuario sendo utilizado nao possui um orientador relacionado consigo mesmo, contate a secretaria para efetuar o cadastro')

        res, cod = get_projeto_orientador(orientador['codOrientador'], id)
        return get_response_code(res, cod)

class BuscarProjetosInativosResource(Resource):
    @secretaria_token_required
    def get(self):
        ret, cod = busca_projeto_inativo()
        return get_response_code(ret, cod)

class GetProjetoInativoResource(Resource):
    @secretaria_token_required
    def get(self, id):
        ret, cod = get_projeto_inativo(id)
        return get_response_code(ret, cod)

class BuscarProjetosOrientadorId(Resource):
    def get(self, id):
        orientador = orientadores_dao.get_orientador_codigo(id, False)
        if not orientador:
            return get_bad_request('O usuario sendo utilizado nao possui um orientador relacionado consigo mesmo, contate a secretaria para efetuar o cadastro')

        res, cod = busca_projetos_orientador_publico(orientador['codOrientador'])
        return get_response_code(res, cod)

class AprovarProjetoResource(Resource):
    @professor_coordenador_secretaria_token_required
    def post(self, id, user_info, is_admin, is_secretaria):
        res, cod = aprovar_projeto(id, user_info, is_admin, is_secretaria)
        return get_response_code(res, cod)

class RecusarProjetoResource(Resource):
    @professor_coordenador_secretaria_token_required
    def post(self, id, user_info, is_admin, is_secretaria):
        res, cod = recusar_projeto(id, user_info, is_admin, is_secretaria)
        return get_response_code(res, cod)

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
        return get_response_code(status, cod)

class AlteraProjetoAlunoResource(Resource):
    @aluno_token_required
    def put(self, id, user_info):
        has_file = False
        r, code = check_file()
        if not r:
            has_file = True
        status, cod = edita_projeto_aluno(id, user_info, has_file)
        return get_response_code(status, cod)

class GetProjetoResource(Resource):
    def get(self, id):
        status, cod = get_projeto(id)
        return get_response_code(status, cod)

class GetProjetoAutorResource(Resource):
    @aluno_token_required
    def get(self, user_info):
        status, cod = get_projeto_autor(user_info)
        return get_response_code(status, cod)

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
        return get_not_found('Arquivo não encontrado')

class DownloadArquivoProjetoNovoResource(Resource):
    @aluno_token_required
    def get(self, filename, user_info):
        attatch = False
        if request.args.get('as_attachment'):
            attatch = True if request.args.get('as_attachment').lower() == 'true' else False

        autor = autores_dao.get_autor_codUsuario(user_info['codUsuario'])
        if not autor:
            return get_erro('O usuario utilizado não possui ligação com nenhum autor cadastrado'), 400
        proj = projetos_dao.get_projeto_novo_codAutor(autor['codAutor'], True)
        if filename == proj['nomeArquivo']:
            if download_arquivo(filename):
                f = send_from_directory(    
                        app.config['UPLOAD_FOLDER'],
                        filename, 
                        as_attachment=attatch
                    )

                return f
        return get_not_found('Arquivo não encontrado')

class CountProjetosResource(Resource):
    def get(self):
        status, cod = get_count()
        return get_response_code(status, cod)

class DesativaProjetoResource(Resource):
    @admin_token_required
    def delete(self, id):
        status, cod = desativa_projeto(id)
        return get_response_code(status, cod)

class AtivaProjetoResource(Resource):
    @admin_token_required
    def post(self, id):
        status, cod = ativa_projeto(id)
        return get_response_code(status, cod)


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

def busca_projetos_orientador(codOrientador):
    res = projetos_dao.busca_projeto_orientador(codOrientador)
    if not res:
        return None, 204
    return get_data(res), 200

def busca_projetos_curso(codCurso):
    res = projetos_dao.busca_projetos_codCurso(codCurso)
    if not res:
        return None, 204
    return get_data(res), 200

def busca_projetos_orientador_publico(codOrientador):
    res = projetos_dao.busca_projeto_orientador_publico(codOrientador)
    if not res:
        return None, 204
    return get_data(res), 200   

def busca_projeto_inativo():
    res = projetos_dao.busca_projeto_inativo()
    if res:
        return get_data(res), 200
    return None, 204

def get_projeto_inativo(id):
    res = projetos_dao.get_projeto_inativo(id)
    if res:
        return get_data(res), 200
    return get_erro('Projeto não encontrado'), 404

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
        subTitulo = request.form['subTitulo']
        linguagem = int(request.form['linguagem'])
        if user_info == None:
            raOrientador = request.form['raOrientador']
            codCurso = request.form['codCurso']
        else:
            orientador = orientadores_dao.get_orientador_orientando_codUsuario(user_info['codUsuario'])
            curso = cursos_dao.get_curso_codUsuario(user_info['codUsuario'])
            if not (orientador and curso):
                return get_erro('O usuario sendo utilizado nao possui um orientador relacionado consigo mesmo, contate a secretaria ou seu orientador para efetuar o cadastro'), 400
            raOrientador = orientador.raOrientador
            codCurso = curso['codCurso']
            
        autores = request.form['autores']
        palavras = request.form['palavras_chave']
    except BadRequestKeyError:
        return get_erro('A requisicao deve conter os campos "titulo", {}"descricao", "dataAvaliacao", "subTitulo", "autores", "linguagem" e "palavras_chave"'.format('"raOrientador", "codCurso", ' if user_info==None else '')), 400
    except ValueError:
        return get_erro(
            'O campo "linguagem" deve ser do tipo inteiro entre 0 e 2'
        ), 400

    if not(titulo and raOrientador and descricao and dataAvaliacao and 
            codCurso and subTitulo):
        return get_erro('Os valores de "titulo", {}"descricao", "dataAvaliacao", "linguagem" e "subTitulo" nao podem ser nulos'.format('"raOrientador", "codCurso", ' if user_info==None else '')), 400
    if not (linguagem) in range(LinguagemProjeto.Espanhol.value + 1):
        return get_falha('O campo linguagem deve ser um campo com numeros entre 0 e 2'), 400

    projeto = Projetos(
        tituloProjeto = titulo,
        subTitulo = subTitulo,
        descricao = descricao,
        dataAvaliacao = dataAvaliacao,
        linguagem = linguagem,
        autores = [], 
        palavrasChave = [],
        curso = cursos_dao.get_curso_codCurso(codCurso),
        orientador = orientadores_dao.get_orientador(raOrientador)
    )
    
    if not projeto.curso:
        return get_erro('O campo "curso" deve conter um código de curso existente'), 400
    if not projeto.orientador:
        return get_falha('O codigo do orientador enviado é invalido'), 400
    
    try:
        autores_obj = json.loads(autores)
    except JSONDecodeError:
        return get_erro('O campo "autores" deve ser um array contendo objetos JSON com os atributos: "nome", "ra" e "email"'), 400
    try:
        palavras_obj = json.loads(palavras)
    except JSONDecodeError:
        return get_erro('O campo "palavras_chave" deve ser um array contendo objetos JSON com o atributo: "palavra"'), 400

    if not user_info:
        if len(autores_obj) < 1:
            return get_erro('Cada projeto deve ter no mínimo 1 autor'), 400
        if len(autores_obj) > 5:
            return get_erro('Cada projeto deve ter no máximo 5 autores'), 400
    else:
        if len(autores_obj) > 4:
            return get_erro('Cada projeto deve ter no máximo 4 autores'), 400

    if len(palavras_obj) < 1:
        return get_erro('Cada projeto deve ter no mínimo 1 palavra-chave'), 400
    if len(palavras_obj) > 5:
        return get_erro('Cada projeto deve ter no máximo 5 palavras-chave'), 400 
    
    if user_info:
        lider = autores_dao.get_autor_codUsuario(user_info['codUsuario'])
        if not lider:
            return get_erro('Não foi possivel obter os dados do autor principal'), 400
        projeto.autores.append(Autores(lider['raAutor'], lider['nomeAutor'], lider['email']))

        if not projetos_dao.is_valid_project(lider['codAutor']):
            return get_erro('Você não pode cadastrar mais um projeto, somente alterar o ja cadastrado caso ele ainda não tenha sido aprovado'), 400
        
    for item in autores_obj:
        try:
            if item['nome'] and item['ra'] and item['email']:
                if not is_valid_email(item['email']):
                    return get_erro('O email "{}" não é um email valido'.format(item['email'])), 400
                projeto.autores.append(Autores(item['ra'], item['nome'], item['email']))
            else:
                return get_erro('Os objetos de autor devem conter os campos "nome", "ra" e "email"'), 400
        except KeyError:
            return get_erro('Cada objeto do campo "autores" deve conter os atributos: "nome", "ra" e "email"'), 400
    
    for item in palavras_obj:
        try:
            if item['palavra']:
                projeto.palavrasChave.append(PalavrasChave(item['palavra']))
            else:
                return get_erro('Os objetos de palavra chave devem conter o campo "palavra"'), 400
        except KeyError:
            return get_erro('Cada objeto do campo "palavras_chave" deve conter o atributo: "palavra"'), 400


    file = request.files['file']
    filename = __get_nome_arquivo_projeto(titulo, file.filename, projeto.curso.abreviacao)
    
    projeto.nomeArquivo = filename
    try:
        if user_info:
            proj = projetos_dao.grava_projeto(
                projeto, is_secretaria=False
            )

            usuario_orientado_dao.add_projeto(user_info['codUsuario'], projeto.codProjeto)
        else:
            proj = projetos_dao.grava_projeto(
                projeto, is_secretaria=True
            )
    except Exception as ex:
        return get_erro(ex.__str__()), 400

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'], 
        filename
    )
    file.save(
        filepath
    )

    capa = os.path.join(app.static_folder, 'Capa.pdf')
    __adicionar_cabecalio([capa, filepath], filepath)

    return get_ok('Projeto cadastrado com sucesso'), 200

def aprovar_projeto(codProjeto, user_info, is_admin, is_secretaria):
    proj = projetos_dao.get_projeto_novo(codProjeto, True)
    if not proj:
        return get_erro('Nenhum projeto (não aprovado) com o código de projeto enviado foi encontrado'), 404
    
    if is_admin or is_secretaria:
        projetos_dao.aprovar_projeto(proj['codProjeto'])
        return get_ok('Projeto aprovado com sucesso'), 200
    elif user_info['tipoUsuario'] == TiposUsuario.Coordenador.value:
        curso = cursos_dao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
        if curso['abreviacao'] == proj['curso']['abreviacao']:
            projetos_dao.aprovar_projeto(proj['codProjeto'])
            return get_ok('Projeto aprovado com sucesso'), 200
        return get_erro('Você não pode aprovar este projeto')
    else:
        orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
        if not orientador:
            return get_erro('O usuario sendo utilizado não possui um orientador relacionado consigo mesmo, contate a secretaria para efetuar o cadastro'), 400

        if projetos_dao.is_orientador_projeto_novo(proj['codProjeto'], orientador['codOrientador']):
            projetos_dao.aprovar_projeto(proj['codProjeto'])

            for autor in proj['autores']:
                enviar_email_aprovacao(autor, proj['tituloProjeto'])

            return get_ok('Projeto aprovado com sucesso'), 200
        return get_erro('Você não pode aprovar este projeto pois você nâo está o orientando'), 400

def recusar_projeto(codProjeto, user_info, is_admin, is_secretaria):
    proj = projetos_dao.get_projeto_novo(codProjeto, True)
    if not proj:
        return get_erro('Nenhum projeto (não aprovado) com o código de projeto enviado foi encontrado'), 404
    
    if is_admin or is_secretaria:
        projetos_dao.recusar_projeto(proj['codProjeto'])
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], proj['nomeArquivo']))
        return get_ok('Projeto recusado com sucesso'), 200
    elif user_info['tipoUsuario'] == TiposUsuario.Coordenador.value:
        curso = cursos_dao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
        if curso['abreviacao'] == proj['curso']['abreviacao']:
            projetos_dao.recusar_projeto(proj['codProjeto'])
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], proj['nomeArquivo']))
            return get_ok('Projeto reprovado com sucesso'), 200
        return get_erro('Você não pode reprovar este projeto')
    else:
        orientador = orientadores_dao.get_orientador_codUsuario(user_info['codUsuario'])
        if not orientador:
            return get_erro('O usuario sendo utilizado não possui um orientador relacionado consigo mesmo, contate a secretaria para efetuar o cadastro'), 400

        if projetos_dao.is_orientador_projeto_novo(proj['codProjeto'], orientador['codOrientador']):
            projetos_dao.recusar_projeto(proj['codProjeto'])
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], proj['nomeArquivo']))

            for autor in proj['autores']:
                enviar_email_reprovacao(autor, proj['tituloProjeto'])

            return get_ok('Projeto recusado com sucesso'), 200
        return get_erro('Você não pode aprovar este projeto pois você nâo está o orientando'), 400

def download_arquivo(filename):
    codProj = projetos_dao.is_ativo_filename(filename)
    if codProj:
        projetos_dao.download_file(codProj)
        return True
    else:
        return False

def desativa_projeto(codProjeto):
    if projetos_dao.get_projeto(codProjeto):
        projetos_dao.desativa_projeto(codProjeto)

        return get_ok('Projeto desativado com sucesso'), 200
    return get_falha('Projeto requisitado nao existe'), 404

def ativa_projeto(codProjeto):
    if projetos_dao.get_projeto(codProjeto):
        projetos_dao.ativa_projeto(codProjeto)

        return get_ok('Projeto ativado com sucesso'), 200
    return get_falha('Projeto requisitado nao existe'), 404

def edita_projeto(codProjeto):
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

def edita_projeto_aluno(codProjeto, user_info, has_file):
    proj = projetos_dao.get_projeto_novo(codProjeto)
    if proj:
        autor = autores_dao.get_autor_codUsuario(user_info['codUsuario'])
        if not autor:
            return get_erro('O usuario utilizado não possui ligação com nenhum autor cadastrado'), 400
        
        if not projeto_autor_dao.is_valid_autor(proj['codProjeto'], autor['codAutor']):
            return get_erro('Voce não pode editar este projeto'), 400
        
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
        
        if has_file:
            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                proj['nomeArquivo']
            )

            file = request.files['file']
            file.save(filepath)
            capa = os.path.join(app.static_folder, 'Capa.pdf')
            __adicionar_cabecalio([capa, filepath], filepath)

        return get_ok('Projeto editado com sucesso'), 200
    return get_falha('Projeto requisitado nao existe'), 404

def get_projeto(codProjeto):
    ret = projetos_dao.get_projeto(codProjeto, True)
    if ret:
        projetos_dao.add_view(codProjeto)
        return get_data(ret), 200
    return get_falha('Projeto requisitado nao existe'), 404

def get_projeto_orientador(codOrientador, codProjeto):
    res = projetos_dao.get_projeto_orientador(codOrientador, codProjeto)
    if not res:
        return None, 404
    return get_data(res), 200

def get_projeto_autor(user_info):
    autor = autores_dao.get_autor_codUsuario(user_info['codUsuario'])
    if not autor:
        return get_erro('O usuario utilizado não possui ligação com nenhum autor cadastrado'), 400
    
    proj = projetos_dao.get_projeto_novo_codAutor(autor['codAutor'], True)
    if not proj:
        return None, 404
    return get_data(proj), 200

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

def enviar_email_aprovacao(autor, titulo_projeto):
    msg = mailer.generate_message(
        'BTA - Projeto Aceito',
        autor['email'],
        '''
        <html>
            <head></head>
            <body>
                <h2>Seu projeto foi aceito.</h2>

                <p>Ola, {0}.</p>

                <p>O seu projeto: <b>{1}</b>, foi aceito na Biblioteca de Trabalhos Academicos e, a partir de agora estará visivel para todos.</p>

                <p>Sistema de gerenciamento de trabalhos acadêmicos BTA.</p>
            </body>
        </html>
        '''.format(autor['nomeAutor'], titulo_projeto)
    )
    mailer.send_email(autor['email'], msg)

def enviar_email_reprovacao(autor, titulo_projeto):
    msg = mailer.generate_message(
        'BTA - Projeto Recusado',
        autor['email'],
        '''
        <html>
            <head></head>
            <body>
                <h2>Seu projeto foi recusado.</h2>

                <p>Ola, {0}.</p>

                <p>O seu projeto: <b>{1}</b>, foi recusado e não será exposto publicamente na Biblioteca de Trabalhos Academicos.</p>

                <p>Sistema de gerenciamento de trabalhos acadêmicos BTA.</p>
            </body>
        </html>
        '''.format(autor['nomeAutor'], titulo_projeto)
    )
    mailer.send_email(autor['email'], msg)

def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
        tipo = 'numVisitas'

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

    if descricaoCurso.upper() == "ADS":
        descricaoCurso = 'SIST'

    filename = filename.replace(
        nfilename,
        '{}-{}-{}-{}'.format(
            descricaoCurso.replace(' ', '-'), 
            titulo.replace(' ', '-'), 
            str(data), 
            str(rand).upper().replace('0X','')
        )
    )
    return filename.upper()

