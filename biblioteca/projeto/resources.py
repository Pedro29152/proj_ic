import os, json, tempfile, shutil

from json.decoder import JSONDecodeError
from smtplib import SMTPAuthenticationError
from flask_restful import Resource
from flask import request, send_from_directory, current_app as app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from datetime import datetime
from random import randint
from PyPDF2 import PdfFileReader, PdfFileWriter
from mysql.connector.errors import IntegrityError
from biblioteca import db

from biblioteca.db import Db
from biblioteca import mailer, response_messages
from biblioteca.curso.cursos_dao import CursosDAO
from biblioteca.autor.autores_dao import AutoresDAO
from biblioteca.autor.projeto_autor_dao import ProjetoAutorDAO
from biblioteca.orientador.orientadores_dao import OrientadoresDAO
from biblioteca.usuarios.usuario_orientado_dao import UsuarioOrientadoDAO
from biblioteca.pdf_generator import TermoCompromisso
from biblioteca.responses import (
    get_data,
    get_falha,
    get_erro,
    get_ok,
    get_count as get_res_count,
    get_bad_request,
    get_response_code,
    get_not_found,
    get_no_content,
    get_success
)
from biblioteca.extensions import(
    admin_token_required,
    secretaria_token_required,
    aluno_token_required,
    professor_token_required,
    coordenador_token_required,
    professor_coordenador_secretaria_token_required,
    aluno_professor_coordenador_token_required,
    is_valid_email,
    get_enum_obj,
    TiposUsuario,
    LinguagemProjeto,
    ModalidadeProjeto,
    AtributosEspeciaisProjeto
)
from .projetos_dao import ProjetosDAO
from .schemas import Projetos, Autores, PalavrasChave

MINIMO_AUTORES = 2
MAXIMO_AUTORES = 5
MINIMO_PALAVRAS_CHAVE = 1
MAXIMO_PALAVRAS_CHAVE = 5
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
        with Db() as db:
            orientadoresDao = OrientadoresDAO(db)
                
            orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

            res, cod = busca_projetos_orientador(orientador['codOrientador'], db)
            return get_response_code(res, cod)

class BuscarProjetosOrientadorNovo(Resource):
    @professor_token_required
    def get(self, user_info):
        with Db() as db:
            orientadoresDao = OrientadoresDAO(db)
                
            orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

            res, cod = busca_projetos_orientador_novo(orientador['codOrientador'], db)
            return get_response_code(res, cod)

class BuscarProjetosCurso(Resource):
    @coordenador_token_required
    def get(self, user_info):
        with Db() as db:
            cursosDao = CursosDAO(db)

            curso = cursosDao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
            if not curso:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

            res, cod = busca_projetos_curso(curso['codCurso'], db)
            return get_response_code(res, cod)

class GetProjetoNovo(Resource):
    @aluno_professor_coordenador_token_required
    def get(self, user_info):
        with Db() as db:
            projetosDao = ProjetosDAO(db)
            orientadoresDao = OrientadoresDAO(db)
            cursosDao = CursosDAO(db)
            autoresDao = AutoresDAO(db)

            if user_info['tipoUsuario'] == TiposUsuario.Professor.value:
                orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
                if not orientador:
                    return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

                proj = projetosDao.get_projeto_novo_codOrientador(orientador['codOrientador'], True)
                if proj:
                    return get_response_code(proj, 200)
                return get_not_found(response_messages.NAO_ENCONTRADO('Trabalho'))
            elif user_info['tipoUsuario'] == TiposUsuario.Aluno.value:
                autor = autoresDao.get_autor_codUsuario(user_info['codUsuario'])
                if not autor:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO_AUT()), 400
                
                proj = projetosDao.get_projeto_novo_codAutor(autor['codAutor'], True)
                if proj:
                    return get_response_code(proj, 200)
                return get_not_found(response_messages.NAO_ENCONTRADO('Trabalho'))
            elif user_info['tipoUsuario'] == TiposUsuario.Coordenador.value:
                curso = cursosDao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
                if not curso:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO_CURSO()), 400
                    
                proj = projetosDao.get_projeto_novo_codCurso(curso['codCurso'], True)
                if proj:
                    return get_response_code(proj, 200)
                return get_not_found(response_messages.NAO_ENCONTRADO('Trabalho'))
            
            return get_response_code(response_messages.ERRO_INESPERADO(), 500)

class BuscarProjetosInativosResource(Resource):
    @secretaria_token_required
    def get(self):
        ret, cod = busca_projeto_inativo()
        return get_response_code(ret, cod)

class BuscaTodosProjetosResource(Resource):
    @secretaria_token_required
    def get(self):
        ret, cod = busca_todos_projetos()
        return get_response_code(ret, cod)

class GetProjetoInativoResource(Resource):
    @secretaria_token_required
    def get(self, id):
        ret, cod = get_projeto_inativo(id)
        return get_response_code(ret, cod)

class BuscarProjetosOrientadorId(Resource):
    def get(self, id):
        with Db() as db:
            orientadoresDao = OrientadoresDAO(db)
                
            orientador = orientadoresDao.get_orientador_codigo(id, False)
            if not orientador:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

            res, cod = busca_projetos_orientador_publico(orientador['codOrientador'], db)
            return get_response_code(res, cod)

class BuscarAtributosProjetoResource(Resource):
    @admin_token_required
    def get(self):
        with Db() as db:
            projetosDao = ProjetosDAO(db)

            separate = True
            if not request.args.get('separate') == None:
                separate = False if request.args.get('separate') == 'false' else True
            
            ret = projetosDao.busca_atributos_projeto(separate_camel_case=separate)
            if not ret:
                return get_no_content()
            return get_success(ret)

class BuscarAtributosEspeciaisProjetoResource(Resource):
    @admin_token_required
    def get(self):
        separate = True
        if not request.args.get('separate') == None:
            separate = False if request.args.get('separate') == 'false' else True
        
        ret = get_enum_obj(AtributosEspeciaisProjeto, separate=separate)
        return get_success(ret)

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
        has_file = False
        r, code = check_file()
        if not r:
            has_file = True
        status, cod = edita_projeto(id, has_file)
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

class AlteraLocalPublicacaoResource(Resource):
    @professor_token_required
    def put(self, user_info, id):
        with Db() as db:
            orientadoresDao = OrientadoresDAO(db)
                
            orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
            if not orientador:
                return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

            status, cod = edita_publicacao(id, orientador['codOrientador'], db)
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
        with Db() as db:
            attatch = False
            if request.args.get('as_attachment'):
                attatch = True if request.args.get('as_attachment').lower() == 'true' else False

            if download_arquivo(filename, db):
                f = send_from_directory(    
                        app.config['UPLOAD_FOLDER'],
                        filename, 
                        as_attachment=attatch
                    )

                return f
            return get_not_found(response_messages.NAO_ENCONTRADO('Arquivo'))

class DownloadArquivoProjetoNovoResource(Resource):
    @aluno_professor_coordenador_token_required
    def get(self, filename, user_info):
        with Db() as db:
            projetosDao = ProjetosDAO(db)
            orientadoresDao = OrientadoresDAO(db)
            cursosDao = CursosDAO(db)
            autoresDao = AutoresDAO(db)

            attatch = False
            if request.args.get('as_attachment'):
                attatch = True if request.args.get('as_attachment').lower() == 'true' else False

            if user_info['tipoUsuario'] == TiposUsuario.Aluno.value:
                autor = autoresDao.get_autor_codUsuario(user_info['codUsuario'])
                if not autor:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO_AUT()), 400
                
                proj = projetosDao.get_projeto_novo_codAutor_nomeArquivo(autor['codAutor'], filename)
                if not proj:
                    return get_erro(response_messages.SEM_AUTORIZACAO()), 401
                
                if download_arquivo(filename, db):
                    f = send_from_directory(    
                            app.config['UPLOAD_FOLDER'],
                            filename, 
                            as_attachment=attatch
                        )

                    return f
            elif user_info['tipoUsuario'] == TiposUsuario.Professor.value:
                orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
                if not orientador:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400

                proj = projetosDao.get_projeto_novo_codOrientador_nomeArquivo(orientador['codOrientador'], filename)
                if not proj:
                    return get_erro(response_messages.SEM_AUTORIZACAO()), 401
                
                if download_arquivo(filename, db):
                    f = send_from_directory(    
                            app.config['UPLOAD_FOLDER'],
                            filename, 
                            as_attachment=attatch
                        )

                    return f
            elif user_info['tipoUsuario'] == TiposUsuario.Coordenador.value:
                curso = cursosDao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
                if not curso:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO_CURSO()), 400

                proj = projetosDao.get_projeto_novo_codCurso_nomeArquivo(curso['codCurso'], filename)
                if not proj:
                    return get_erro(response_messages.SEM_AUTORIZACAO()), 401

                if download_arquivo(filename, db):
                    f = send_from_directory(    
                            app.config['UPLOAD_FOLDER'],
                            filename, 
                            as_attachment=attatch
                        )

                    return f

            return get_not_found(response_messages.NAO_ENCONTRADO('Arquivo'))

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
    with Db() as db:
        projetosDao = ProjetosDAO(db)

        dados, ordem, cres = __get_filtro()

        if tipo:
            ret = projetosDao.busca_projeto_tipo(tipo,dados,ordem,cres)
        else:
            ret = projetosDao.busca_projeto()

        if ret:
            return get_data(ret), 200
        else:
            return None, 204

def busca_pag(tipo='', pag = 1):
    dados, ordem, cres = __get_filtro()
    try:
        pag = int(pag)
    except ValueError:
        return get_erro(response_messages.VALIDACAO_DEVE('"page"', 'ser do tipo inteiro')), 404
    
    with Db() as db:
        projetosDao = ProjetosDAO(db)

        if tipo: 
            ret = projetosDao.busca_projeto_tipo_pag(tipo,dados,ordem,cres)
        else:
            ret = projetosDao.busca_projeto_pag(pag)

        if ret:
            return get_data(ret), 200
        else:
            return None, 204

def busca_projetos_orientador(codOrientador, db):
    projetosDao = ProjetosDAO(db)

    res = projetosDao.busca_projeto_orientador(codOrientador)
    if not res:
        return None, 204
    return get_data(res), 200

def busca_projetos_orientador_novo(codOrientador, db):
    projetosDao = ProjetosDAO(db)
        
    res = projetosDao.busca_projeto_orientador_novo(codOrientador)
    if not res:
        return None, 204
    return get_data(res), 200

def busca_projetos_curso(codCurso, db):
    projetosDao = ProjetosDAO(db)
        
    res = projetosDao.buscar_projetos_codCurso_novo(codCurso, True)
    if not res:
        return None, 204
    return get_data(res), 200

def busca_projetos_orientador_publico(codOrientador, db):
    projetosDao = ProjetosDAO(db)

    res = projetosDao.busca_projeto_orientador_publico(codOrientador)
    if not res:
        return None, 204
    return get_data(res), 200   

def busca_projeto_inativo():
    with Db() as db:
        projetosDao = ProjetosDAO(db)

        res = projetosDao.busca_projeto_inativo()
        if res:
            return get_data(res), 200
        return None, 204

def busca_todos_projetos():
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        res = projetosDao.busca_todos_projetos()
        if res:
            return get_data(res), 200
        return None, 204

def get_projeto_inativo(id):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        res = projetosDao.get_projeto_inativo(id)
        if res:
            return get_data(res), 200
        return get_erro(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def check_file():
    if 'file' not in request.files:
        return get_falha(response_messages.ARQUIVO_NAO_ENVIADO()), 400

    if request.files['file'].filename == '':
        return get_falha(response_messages.ARQUIVO_NAO_ENVIADO()), 400

    if not __allowed_file(request.files['file'].filename):
        return get_falha(response_messages.EXTENSAO_NAO_SUPORTADA()), 415
    
    if request.files['file']:
        return None, None
            
    return get_erro(response_messages.ERRO_INESPERADO()), 500

def upload_projeto(user_info=None):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
        orientadoresDao = OrientadoresDAO(db)
        usuarioOrientadoDao = UsuarioOrientadoDAO(db)
        cursosDao = CursosDAO(db)
        autoresDao = AutoresDAO(db)
            
        try:
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            subTitulo = request.form['subTitulo']
            dataAvaliacao = request.form['dataAvaliacao']
            linguagem = int(request.form['linguagem'])
            modalidade = int(request.form['modalidade'])
            raCoOrientador = request.form['raCoOrientador']
            localPublicacao = request.form['localPublicacao']
            if user_info == None:
                raOrientador = request.form['raOrientador']
                codCurso = request.form['codCurso']
            else:
                orientador = orientadoresDao.get_orientador_orientando_codUsuario(user_info['codUsuario'])
                curso = cursosDao.get_curso_codUsuario(user_info['codUsuario'])
                if not (orientador and curso):
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400
                raOrientador = orientador.raOrientador
                codCurso = curso['codCurso']
                
            autores = request.form['autores']
            palavras = request.form['palavras_chave']
        except BadRequestKeyError:
            return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"titulo", "localPublicacao", {}"descricao", "dataAvaliacao", "modalidade", "subTitulo", "autores", "linguagem", "raCoOrientador" e "palavras_chave"'.format('"raOrientador", "codCurso", ' if user_info==None else ''))), 400
        except ValueError:
            return get_erro(response_messages.VALIDACAO_DEVEM('"linguagem" e "modalidade"', 'ser do tipo inteiro')), 400

        if not(titulo and raOrientador and dataAvaliacao and codCurso):
            return get_erro(response_messages.ATRIBUTO_OBRIGATORIO('"titulo", {}"dataAvaliacao" e "linguagem"'.format('"raOrientador", "codCurso", ' if user_info==None else ''))), 400
        if not (linguagem) in range(LinguagemProjeto.Espanhol.value + 1):
            return get_falha(response_messages.VALIDACAO_DEVE('linguagem','ser um campo de numeros entre 0 e 2')), 400
        if not (modalidade) in range(ModalidadeProjeto.GDD.value + 1):
            return get_falha(response_messages.VALIDACAO_DEVE('modalidade', 'ser um campo de numeros entre 0 e 2')), 400

        projeto = Projetos(
            tituloProjeto = titulo,
            subTitulo = subTitulo,
            descricao = descricao,
            dataAvaliacao = dataAvaliacao,
            linguagem = linguagem,
            modalidade = modalidade,
            localPublicacao = localPublicacao,
            autores = [], 
            palavrasChave = [],
            curso = cursosDao.get_curso_codCurso(codCurso),
            orientador = orientadoresDao.get_orientador(raOrientador),
            coOrientador = orientadoresDao.get_orientador(raCoOrientador)
        )
        
        if not projeto.curso:
            return get_erro(response_messages.VALIDACAO_DEVE('curso', 'conter um código de curso existente')), 400
        if raOrientador == raCoOrientador:
            return get_erro(response_messages.VALIDACAO_DEVE('orientador', 'ser diferente do coOrientador')), 400
        if not projeto.orientador:
            return get_falha(response_messages.ATRIBUTO_INVALIDO('raOrientador')), 400
        if raCoOrientador:
            if not projeto.coOrientador:
                return get_falha(response_messages.ATRIBUTO_INVALIDO('raCoOrientador')), 400
        
        try:
            autores_obj = json.loads(autores)
        except JSONDecodeError:
            return get_erro(response_messages.VALIDACAO_DEVE('autores', 'ser um array contendo objetos JSON com os atributos: "nome", "ra" e "email"')), 400
        try:
            palavras_obj = json.loads(palavras)
        except JSONDecodeError:
            return get_erro(response_messages.VALIDACAO_DEVE('palavras_chave', 'ser um array contendo objetos JSON com o atributo: "palavra"')), 400

        if len(autores_obj) < (MINIMO_AUTORES - 1 if user_info else MINIMO_AUTORES):
            return get_erro(response_messages.VALIDACAO_DEVE('autores', 'ter no mínimo {0} autor'.format(MINIMO_AUTORES))), 400
        if len(autores_obj) > MAXIMO_AUTORES:
            return get_erro(response_messages.VALIDACAO_DEVE('autores', 'ter no máximo {0} autores'.format(MAXIMO_AUTORES))), 400

        if len(palavras_obj) < MINIMO_PALAVRAS_CHAVE:
            return get_erro(response_messages.VALIDACAO_DEVE('palavras_chave', 'ter no mínimo {0} palavra-chave'.format(MINIMO_PALAVRAS_CHAVE))), 400
        if len(palavras_obj) > MAXIMO_PALAVRAS_CHAVE:
            return get_erro(response_messages.VALIDACAO_DEVE('palavras_chave', 'ter no máximo {0} palavras-chave'.format(MAXIMO_PALAVRAS_CHAVE))), 400 
        
        if user_info:
            lider = autoresDao.get_autor_codUsuario(user_info['codUsuario'])
            if not lider:
                return get_erro(response_messages.NAO_FOI_POSSIVEL('obter os dados do autor principal')), 400
            removed = 0
            for i in range(len(autores_obj)):
                if autores_obj[i - removed]['ra'] == lider['raAutor']:
                    autores_obj.pop(i - removed)
                    removed = removed + 1
            projeto.autores.append(Autores(lider['raAutor'], lider['nomeAutor'], lider['email'], db=db))

            if not projetosDao.is_valid_project(lider['codAutor']):
                return get_erro(response_messages.NAO_PODE_ALTERAR_PROJETO()), 400
            
        for item in autores_obj:
            try:
                if item['nome'] and item['ra'] and item['email']:
                    if not is_valid_email(item['email']):
                        return get_erro(response_messages.ATRIBUTO_INVALIDO('email')), 400
                    projeto.autores.append(Autores(item['ra'], item['nome'], item['email'], db=db))
                else:
                    return get_erro(response_messages.VALIDACAO_DEVE('autores', 'conter os campos "nome", "ra" e "email"')), 400
            except KeyError:
                return get_erro(response_messages.VALIDACAO_DEVE('autores', 'conter os campos "nome", "ra" e "email"')), 400
        
        for item in palavras_obj:
            try:
                if item['palavra']:
                    projeto.palavrasChave.append(PalavrasChave(item['palavra'], db=db))
                else:
                    return get_erro(response_messages.VALIDACAO_DEVE('palavras_chave', 'conter o campo "palavra"')), 400
            except KeyError:
                return get_erro(response_messages.VALIDACAO_DEVE('palavras_chave', 'conter o campo "palavra"')), 400

        file = request.files['file']
        filename = __get_nome_arquivo_projeto(titulo, file.filename, projeto.curso.abreviacao)
        
        projeto.nomeArquivo = filename
        try:
            if user_info:
                proj = projetosDao.grava_projeto(
                    projeto, is_secretaria=False
                )

                usuarioOrientadoDao.add_projeto(user_info['codUsuario'], projeto.codProjeto)
            else:
                proj = projetosDao.grava_projeto(
                    projeto, is_secretaria=True
                )

                try:
                    for autor in projeto.autores:
                        enviar_email_permissao(
                            autor, 
                            projeto.curso.descricaoCurso, 
                            projeto.tituloProjeto, 
                            projeto.dataAvaliacao.split('-')[0]
                        )
                except SMTPAuthenticationError as se:
                    raise Exception(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL())
        except Exception as ex:
            db.rollback()
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

        return get_ok(response_messages.ENTIDADE_GRAVADA('Trabalho')), 200

def aprovar_projeto(codProjeto, user_info, is_admin, is_secretaria):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
        orientadoresDao = OrientadoresDAO(db)
        cursosDao = CursosDAO(db)
            
        proj = projetosDao.get_projeto_novo(codProjeto, True)
        if not proj:
            return get_erro(response_messages.NAO_ENCONTRADO('Projeto')), 404
        
        try:
            if is_admin or is_secretaria:
                projetosDao.aprovar_projeto(proj['codProjeto'])
                
                enviar_email_aprovacao(proj['autores'], proj['tituloProjeto'])
                for autor in proj['autores']:
                    enviar_email_permissao(
                        autor,
                        proj['curso']['descricaoCurso'],
                        proj['tituloProjeto'],
                        proj['dataAvaliacao'].strftime('%Y')
                    )

                return get_ok(response_messages.TRABALHO_APROVADO()), 200
            elif user_info['tipoUsuario'] == TiposUsuario.Coordenador.value:
                curso = cursosDao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
                if curso['abreviacao'] == proj['curso']['abreviacao']:
                    projetosDao.aprovar_projeto(proj['codProjeto'])
                    
                    enviar_email_aprovacao(proj['autores'], proj['tituloProjeto'])
                    for autor in proj['autores']:
                        enviar_email_permissao(
                            autor,
                            proj['curso']['descricaoCurso'],
                            proj['tituloProjeto'],
                            proj['dataAvaliacao'].strftime('%Y')
                        )

                    return get_ok(response_messages.TRABALHO_APROVADO()), 200
                return get_erro(response_messages.SEM_PERMICAO('aprovar este trabalho'))
            else:
                orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
                if not orientador:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400

                if projetosDao.is_orientador_projeto_novo(proj['codProjeto'], orientador['codOrientador']):
                    projetosDao.aprovar_projeto(proj['codProjeto'])

                    enviar_email_aprovacao(proj['autores'], proj['tituloProjeto'])
                    for autor in proj['autores']:
                        enviar_email_permissao(
                            autor,
                            proj['curso']['descricaoCurso'],
                            proj['tituloProjeto'],
                            proj['dataAvaliacao'].strftime('%Y')
                        )

                    return get_ok(response_messages.TRABALHO_APROVADO()), 200
                return get_erro(response_messages.SEM_PERMICAO('aprovar este trabalho')), 400
        except SMTPAuthenticationError as ae:
            db.rollback()
            return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL()), 500
        except Exception as ex:
            db.rollback()
            return get_erro(ex.__str__()), 400

def recusar_projeto(codProjeto, user_info, is_admin, is_secretaria):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
        orientadoresDao = OrientadoresDAO(db)
        cursosDao = CursosDAO(db)
            
        proj = projetosDao.get_projeto_novo(codProjeto, True)
        if not proj:
            return get_erro(response_messages.NAO_ENCONTRADO('Trabalho')), 404

        arquivo_rm = os.path.join(app.config['UPLOAD_FOLDER'], proj['nomeArquivo'])
        tmp_file = os.path.join(tempfile.gettempdir(), proj['nomeArquivo'])
        deleted = False

        try:
            if is_admin or is_secretaria:
                projetosDao.recusar_projeto(proj['codProjeto'])

                try:
                    shutil.move(arquivo_rm, tmp_file)
                    deleted = True
                except FileNotFoundError as fe:
                    pass

                enviar_email_reprovacao(proj['autores'], proj['tituloProjeto'])

                return get_ok(response_messages.TRABALHO_REPROVADO()), 200
            elif user_info['tipoUsuario'] == TiposUsuario.Coordenador.value:
                curso = cursosDao.get_curso_codUsuario_coordenador(user_info['codUsuario'])
                if curso['abreviacao'] == proj['curso']['abreviacao']:
                    projetosDao.recusar_projeto(proj['codProjeto'])

                    try:
                        shutil.move(arquivo_rm, tmp_file)
                        deleted = True
                    except FileNotFoundError as fe:
                        pass

                    enviar_email_reprovacao(proj['autores'], proj['tituloProjeto'])

                    return get_ok(response_messages.TRABALHO_REPROVADO()), 200
                return get_erro(response_messages.SEM_PERMICAO('reprovar este projeto')), 401
            else:
                orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
                if not orientador:
                    return get_erro(response_messages.USUARIO_NAO_RELACIONADO()), 400

                if projetosDao.is_orientador_projeto_novo(proj['codProjeto'], orientador['codOrientador']):
                    projetosDao.recusar_projeto(proj['codProjeto'])

                    try:
                        shutil.move(arquivo_rm, tmp_file)
                        deleted = True
                    except FileNotFoundError as fe:
                        pass

                    enviar_email_reprovacao(proj['autores'], proj['tituloProjeto'])

                    return get_ok(response_messages.TRABALHO_REPROVADO()), 200
                return get_erro(response_messages.SEM_PERMICAO('aprovar este trabalho')), 400
        except SMTPAuthenticationError as se:
            db.rollback()
            if deleted:
                try:
                    shutil.move(tmp_file, arquivo_rm)
                except FileNotFoundError as fe:
                    pass
            return get_erro(response_messages.NAO_FOI_POSSIVEL_ENVIAR_EMAIL()), 500
        except Exception as ex:
            db.rollback()
            if deleted:
                try:
                    shutil.move(tmp_file, arquivo_rm)
                except FileNotFoundError as fe:
                    pass
            return get_erro(ex.__str__()), 400

def download_arquivo(filename, db):
    projetosDao = ProjetosDAO(db)
        
    codProj = projetosDao.is_ativo_filename(filename)
    if codProj:
        projetosDao.download_file(codProj)
        return True
    else:
        return False

def desativa_projeto(codProjeto):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        if projetosDao.get_projeto(codProjeto):
            projetosDao.desativa_projeto(codProjeto)

            return get_ok(response_messages.ENTIDADE_DESATIVADA('Trabalho')), 200
        return get_falha(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def ativa_projeto(codProjeto):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        if projetosDao.get_projeto_inativo(codProjeto):
            projetosDao.ativa_projeto(codProjeto)

            return get_ok(response_messages.ENTIDADE_ATIVADA('Trabalho')), 200
        return get_falha(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def edita_projeto(codProjeto, has_file):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        proj = projetosDao.get_projeto(codProjeto)
        if proj:
            try:
                titulo = request.form['tituloProjeto']
                descricao = request.form['descricao']
                subtitulo = request.form['subTitulo']
            except BadRequestKeyError:
                return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"tituloProjeto","descricao" e "subTitulo"')), 400

            if titulo:
                projetosDao.edita_titulo(codProjeto, titulo)
            if descricao:
                projetosDao.edita_descricao(codProjeto, descricao)
            if subtitulo:
                projetosDao.edita_subtitulo(codProjeto, subtitulo)
            
            if has_file:
                filepath = os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    proj['nomeArquivo']
                )

                file = request.files['file']
                file.save(filepath)
                capa = os.path.join(app.static_folder, 'Capa.pdf')
                __adicionar_cabecalio([capa, filepath], filepath)
            
            return get_ok(response_messages.ENTIDADE_EDITADA('Trabalho')), 200
        return get_falha(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def edita_projeto_aluno(codProjeto, user_info, has_file):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
        projetoAutorDao = ProjetoAutorDAO(db)
        autoresDao = AutoresDAO(db)
            
        proj = projetosDao.get_projeto_novo(codProjeto)
        if proj:
            autor = autoresDao.get_autor_codUsuario(user_info['codUsuario'])
            if not autor:
                return get_erro(response_messages.USUARIO_NAO_RELACIONADO_AUT()), 400
            
            if not projetoAutorDao.is_valid_autor(proj['codProjeto'], autor['codAutor']):
                return get_erro(response_messages.SEM_PERMICAO('editar este projeto')), 400
            
            try:
                titulo = request.form['tituloProjeto']
                descricao = request.form['descricao']
                subtitulo = request.form['subTitulo']
            except BadRequestKeyError:
                return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"tituloProjeto","descricao" e "subTitulo"')), 400

            if titulo:
                projetosDao.edita_titulo(codProjeto, titulo)
            if descricao:
                projetosDao.edita_descricao(codProjeto, descricao)
            if subtitulo:
                projetosDao.edita_subtitulo(codProjeto, subtitulo)
            
            if has_file:
                filepath = os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    proj['nomeArquivo']
                )

                file = request.files['file']
                file.save(filepath)
                capa = os.path.join(app.static_folder, 'Capa.pdf')
                __adicionar_cabecalio([capa, filepath], filepath)

            return get_ok(response_messages.ENTIDADE_EDITADA('Trabalho')), 200
        return get_falha(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def edita_publicacao(codProjeto, codOrientador, db):
    projetosDao = ProjetosDAO(db)
        
    proj = projetosDao.get_projeto_orientador(codOrientador, codProjeto)
    if proj:
        try:
            publicacao = request.form['publicacaoProjeto']
        except BadRequestKeyError:
            return get_erro(response_messages.CAMPOS_OBRIGATORIOS('"publicacaoProjeto"')), 400

        if not publicacao:
            return get_erro(response_messages.PREENCHIMENTO_OBRIGATORIO()), 400

        projetosDao.edita_publicacao(codProjeto, publicacao)

        return get_ok(response_messages.ENTIDADE_EDITADA('Publicação')), 200
    return get_falha(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def get_projeto(codProjeto):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        ret = projetosDao.get_projeto(codProjeto, True)
        if ret:
            projetosDao.add_view(codProjeto)
            return get_data(ret), 200
        return get_falha(response_messages.NAO_ENCONTRADO('Trabalho')), 404

def get_projeto_autor(user_info):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
        autoresDao = AutoresDAO(db)
            
        autor = autoresDao.get_autor_codUsuario(user_info['codUsuario'])
        if not autor:
            return get_erro(response_messages.USUARIO_NAO_RELACIONADO_AUT()), 400
        
        proj = projetosDao.get_projeto_novo_codAutor(autor['codAutor'], True)
        if not proj:
            return None, 404
        return get_data(proj), 200

def busca_ranking():
    with Db() as db:
        projetosDao = ProjetosDAO(db)

        query, tipo, ordem = __get_filtro_rank()

        ret = projetosDao.busca_projeto_ranking(query, tipo, ordem)

        if ret == None:
            return None, 204

        return get_data(ret), 200

def busca_ranking_pag(page = 1):
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        query, tipo, ordem = __get_filtro_rank()
        
        try:
            page = int(page)
        except:
            return get_erro(response_messages.VALIDACAO_DEVE('page', 'ser do tipo inteiro')), 404

        ret = projetosDao.busca_projeto_ranking_pag(query, tipo, ordem, page)

        if ret == None:
            return None, 204

        return get_data(ret), 200

def get_count():
    with Db() as db:
        projetosDao = ProjetosDAO(db)
            
        count = projetosDao.get_count()
        return get_res_count(count), 200

def enviar_email_permissao(autor, curso, titulo, anoAvaliacao):
    emails = [autor['email'], os.getenv('CONTACT_EMAIL')]

    path_termo = os.path.join(app.config['STATIC_FOLDER'], 'termos', 'termo.txt')
    nome_arquivo_pdf = 'termo_autorizacao.pdf'
    arquivo_pdf = (os.path.join(app.config['STATIC_FOLDER'], 'termos', nome_arquivo_pdf), nome_arquivo_pdf)
    
    with open(path_termo,'rb') as file_termo:
        txt = file_termo.read().decode('UTF-8').format(
            autor['nomeAutor'], 
            autor['raAutor'], 
            curso, 
            titulo, 
            anoAvaliacao)

        termo = TermoCompromisso()
        termo.create("TERMO DE PERMISSÃO DE ACESSO AO DOCUMENTO", txt)
        termo.output(arquivo_pdf[0])
    
    msg = mailer.generate_message_html(
        'Termo de permissão de accesso ao documento',
        os.getenv('MAILER_SENDER_EMAIL'),
        '''
            <div>
                <h2>TERMO DE PERMISSÃO DE ACESSO AO DOCUMENTO</h2>
                <p class="aling-justify">
                    Segue em anexo Termo de Permissão de Acesso, do autor {} portador do RA {}, ao projeto {} do curso {} publicado no ano {}.
                </p>
            </div>
        '''.format(
            autor['nomeAutor'], 
            autor['raAutor'],
            titulo,
            curso,
            anoAvaliacao,
        ),
        cco=emails,
        pdf_attachment=[arquivo_pdf]
    )
    mailer.send_email(emails, msg)

def enviar_email_aprovacao(autores, titulo_projeto):
    emails = []
    for item in autores:
        emails.append(item['email'])

    msg = mailer.generate_message_html(
        'Projeto Aceito',
        os.getenv('MAILER_SENDER_EMAIL'),
        '''
            <h2>Seu projeto foi aceito.</h2>

            <p>Olá.</p>

            <p>O seu projeto: <b>{0}</b>, foi aceito na Biblioteca de Trabalhos Acadêmicos e, a partir de agora estará visível para todos.</p>
        '''.format(titulo_projeto),
        cco=emails
    )

    mailer.send_email(emails, msg)

def enviar_email_reprovacao(autores, titulo_projeto):
    emails = []
    for item in autores:
        emails.append(item['email'])
    
    msg = mailer.generate_message_html(
        'Projeto Recusado',
        os.getenv('MAILER_SENDER_EMAIL'),
        '''
            <h2>Seu projeto foi recusado.</h2>

            <p>Olá.</p>

            <p>O seu projeto: <b>{0}</b>, foi recusado e não será exposto publicamente na Biblioteca de Trabalhos Acadêmicos.</p>
        '''.format(titulo_projeto),
        cco=emails
    )

    mailer.send_email(emails, msg)

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
