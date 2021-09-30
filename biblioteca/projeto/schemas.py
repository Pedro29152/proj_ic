from mysql.connector.errors import DataError, IntegrityError

from biblioteca.db import Db
from biblioteca.extensions import is_valid_email

class Projetos:
    def __init__(self, 
    codProjeto=0, 
    tituloProjeto='',
    subTitulo='',
    descricao='', 
    nomeArquivo='', 
    dataAvaliacao=None, 
    dataEnvio=None, 
    avaliacao=None,
    curso=None, 
    autores=None,
    orientador=None,
    coOrientador=None, 
    palavrasChave=None,
    linguagem=None,
    modalidade=None,
    localPublicacao=None):

        self.codProjeto = codProjeto
        self.tituloProjeto = tituloProjeto
        self.subTitulo = subTitulo
        self.descricao = descricao
        self.nomeArquivo = nomeArquivo
        self.dataAvaliacao = dataAvaliacao
        self.dataEnvio = dataEnvio

        self.avaliacao = avaliacao
        self.curso = curso
        self.autores = autores
        self.orientador = orientador
        self.coOrientador = coOrientador
        self.palavrasChave = palavrasChave
        self.linguagem = linguagem
        self.modalidade = modalidade
        self.localPublicacao = localPublicacao

class Avalicoes:
    def __init__(self, numVisitas, numDownloads):
        self.numVisitas = numVisitas
        self.numDownloads = numDownloads

class PalavrasChave:
    def __init__(self, palavraChave='', codPalavra = 0, projeto = None):
        self.codPalavra = codPalavra
        self.palavraChave = palavraChave

        self.projeto = projeto

    def grava_palavra_chave(self, codProjeto):
        with Db() as db:
            query = "INSERT INTO palavras_chave(palavraChave, codProjeto) values(%s,%s)"
            db.gravar_autocommit(query, (self.palavraChave, codProjeto))

            return True

class Autores:
    def __init__(self, raAutor='', nomeAutor='', email=''):        
        self.raAutor = raAutor
        self.nomeAutor = nomeAutor
        self.email = email.lower()

        if not is_valid_email(self.email):
            raise AttributeError('O campo "email" dever ser um email valido')

    def __getitem__(self, attr):
        return getattr(self, attr)
    
    def tenta_gravar_autor(self, codProjeto):
        with Db() as db:
            try:
                query = 'INSERT INTO autores(raAutor, nomeAutor, email) values(%s,%s,%s)'
                db.gravar_autocommit(query, (self.raAutor, self.nomeAutor, self.email))
            except IntegrityError:
                db.rollback()
            except Exception as ex:
                db.rollback()
                raise ex

            return db.busca_um("select codAutor from autores where raAutor = %s",(self.raAutor,))['codAutor']
