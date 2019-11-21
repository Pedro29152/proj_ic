from biblioteca import bd_conn
from biblioteca.util import json_res
from mysql.connector.errors import IntegrityError

class Autores:
    def __init__(self, raAutor="", nomeAutor=""):        
        self.raAutor = raAutor
        self.nomeAutor = nomeAutor

    def grava_autor(self, codProjeto):
        try:
            bd_conn.bd_gravar("INSERT INTO autores(raAutor, nomeAutor) values(%s,%s)",
            (self.raAutor, self.nomeAutor))
        except IntegrityError:
            pass
        return bd_conn.bd_busca_um("select codAutor from autores where raAutor = %s",(self.raAutor,))['codAutor']

class Cursos:
    def __init__(self, descricaoCurso="", abreviacao="", codCurso=0):
        self.codCurso = codCurso
        self.descricaoCurso = descricaoCurso
        self.abreviacao = abreviacao

    def __str__(self):
        return str(self.codCurso) + ' ' + self.descricaoCurso + ' ' + self.abreviacao

    def grava_curso(self):
        if(self.descricaoCurso and self.abreviacao):
            bd_conn.bd_gravar(
                'insert into cursos(descricaoCurso, abreviacao, ativo) values(%s,%s,1)',
                (self.descricaoCurso, self.abreviacao)
            )
            return True

        else:
            return True

class PalavrasChave:
    def __init__(self, palavraChave='', codPalavra = 0, projeto = None):
        self.codPalavra = codPalavra
        self.palavraChave = palavraChave

        self.projeto = projeto

    def grava_palavra_chave(self, codProjeto):
        bd_conn.bd_gravar("INSERT INTO palavras_chave(palavraChave, codProjeto) values(%s,%s)",
            (self.palavraChave, codProjeto))

        return True

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


class Usuarios:
    def __init__(self, codUsuario, nomeUsuario, senha, tipoUsuario):
        self.codUsuario = codUsuario
        self.nomeUsuario = nomeUsuario
        self.senha = senha
        self.tipoUsuario = tipoUsuario
        
class Orientadores:
    def __init__(self, codOrientador=None, nomeOrientador=None, raOrientador=None):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
    
    def grava_orientador(self):
        if self.nomeOrientador and self.raOrientador:
            bd_conn.bd_gravar(
                'insert into orientadores(nomeOrientador, raOrientador) values(%s, %s)',
                (self.nomeOrientador, self.raOrientador)
            )
            self.codOrientador = bd_conn.bd_busca_um(
                'select codOrientador from orientadores where raOrientador = (%s)', 
                (self.raOrientador,)
            )['codOrientador']
        else:
            raise AttributeError('A classe deve possuir os campos "nomeOrientador" e "raOrientador" preenchidos')