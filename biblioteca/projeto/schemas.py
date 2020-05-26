from mysql.connector.errors import IntegrityError

from biblioteca import db

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
    palavrasChave=None):

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
        self.palavrasChave = palavrasChave

class Avalicoes:
    def __init__(self, likes, deslikes, numVisitas, numDownloads):
        self.likes = likes
        self.deslikes = deslikes
        self.numVisitas = numVisitas
        self.numDownloads = numDownloads

class PalavrasChave:
    def __init__(self, palavraChave='', codPalavra = 0, projeto = None):
        self.codPalavra = codPalavra
        self.palavraChave = palavraChave

        self.projeto = projeto

    def grava_palavra_chave(self, codProjeto):
        db.bd_gravar("INSERT INTO palavras_chave(palavraChave, codProjeto) values(%s,%s)",
            (self.palavraChave, codProjeto))

        return True

class Autores:
    def __init__(self, raAutor="", nomeAutor=""):        
        self.raAutor = raAutor
        self.nomeAutor = nomeAutor

    def grava_autor(self, codProjeto):
        try:
            db.bd_gravar("INSERT INTO autores(raAutor, nomeAutor) values(%s,%s)",
            (self.raAutor, self.nomeAutor))
        except IntegrityError:
            pass
        return db.bd_busca_um("select codAutor from autores where raAutor = %s",(self.raAutor,))['codAutor']
