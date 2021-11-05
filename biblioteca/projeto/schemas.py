from mysql.connector.errors import DataError, IntegrityError
from biblioteca.autor.autores_dao import AutoresDAO

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
    def __init__(self, palavraChave='', codPalavra = 0, projeto = None, db=None):
        self.codPalavra = codPalavra
        self.palavraChave = palavraChave

        self.projeto = projeto

        self.db = db

    def grava_palavra_chave(self, codProjeto):
        query = "INSERT INTO palavras_chave(palavraChave, codProjeto) values(%s,%s)"
        self.db.gravar(query, (self.palavraChave, codProjeto))

        return True

class Autores:
    def __init__(self, raAutor='', nomeAutor='', email='', db=None):        
        self.raAutor = raAutor
        self.nomeAutor = nomeAutor
        self.email = email.lower()

        self.db = db

        if not is_valid_email(self.email):
            raise AttributeError('O campo "email" dever ser um email valido')

    def __getitem__(self, attr):
        return getattr(self, attr)
    
    def tenta_gravar_autor(self):
        try:
            query = 'INSERT INTO autores(raAutor, nomeAutor, email) values(%s,%s,%s)'
            self.db.gravar(query, (self.raAutor, self.nomeAutor, self.email))
        except IntegrityError as ie:
            self.db.rollback()
            raise ie
        except Exception as ex:
            self.db.rollback()
            raise ex

        return self.db.busca_um("select codAutor from autores where raAutor = %s and email = %s",(self.raAutor, self.email))['codAutor']
