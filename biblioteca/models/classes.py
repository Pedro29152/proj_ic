from biblioteca import bd_conn
from mysql.connector.errors import IntegrityError


class Autores:
    def __init__(self, raAutor="", nomeAutor="", projeto=None):        
        self.raAutor = raAutor
        self.nomeAutor = nomeAutor

        self.projeto = projeto

    def grava_autor(self, codProjeto):
        bd_conn.bd_gravar("INSERT INTO autores(raAutor, nomeAutor, codProjeto) values(%s,%s,%s)",
        (self.raAutor, self.nomeAutor, codProjeto))
        return bd_conn.bd_busca_um("select codAutor from autores where raAutor = %s",(self.raAutor,))['codAutor']

class Cursos:
    def __init__(self, descricaoCurso="", abreviacao="", codCurso=0):
        self.codCurso = codCurso
        self.descricaoCurso = descricaoCurso
        self.abreviacao = abreviacao

    def __str__(self):
        return str(self.codCurso) + ' ' + self.descricaoCurso + ' ' + self.abreviacao

    def grava_curso(self):
        try:
            if(self.descricaoCurso and self.abreviacao):
                bd_conn.bd_gravar(
                    'insert into cursos(descricaoCurso, abreviacao, ativo) values(%s,%s,1)',
                    (self.descricaoCurso, self.abreviacao)
                )

                return {
                    'status': 'sucesso',
                    'message': 'Curso gravado com sucesso'
                }

            else:
                return {
                    'status': 'falha',
                    'message': 'Erro ao gravar curso'
                }
        except IntegrityError:
            return {
                'status': 'erroIntegridade',
                'message': 'Curso ou abreviacao ja cadastrados'
            }


class Gerenciadores:
    def __init__(self, codGerenciador=0, cpfGerenciador='', instituicao='', nomeGerenciador='', emailGerenciador=''):
        self.codGerenciador = codGerenciador
        self.cpfGerenciador = cpfGerenciador
        self.instituicao = instituicao
        self.nomeGerenciador = nomeGerenciador
        self.emailGerenciador = emailGerenciador

    def grava_gerenciador(self):
        bd_conn.bd_gravar('insert into gerenciadores(cpfGerenciador, instituicao, nomeGerenciador, emailGerenciador) values(%s,%s,%s,%s)',
        (self.cpfGerenciador, self.instituicao, self.nomeGerenciador, self.emailGerenciador))
        return bd_conn.bd_busca_um("select codGerenciador from gerenciadores where cpfGerenciador = %s",(self.cpfGerenciador,))['codGerenciador']

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
    descricao='', 
    nomeArquivo='', 
    notaProjeto=0, 
    dataAvaliacao=None, 
    dataEnvio=None, 
    avaliacao=None, 
    gerenciador=None, 
    curso=None, 
    autores=None,
    orientador=None, 
    palavrasChave=None):

        self.codProjeto = codProjeto
        self.tituloProjeto = tituloProjeto
        self.descricao = descricao
        self.nomeArquivo = nomeArquivo
        self.notaProjeto = notaProjeto
        self.dataAvaliacao = dataAvaliacao
        self.dataEnvio = dataEnvio

        self.avaliacao = avaliacao
        self.gerenciador = gerenciador
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
    def __init__(self, codUsuario, nomeUsuario, senha, tipoUsuario, gerenciador):
        self.codUsuario = codUsuario
        self.nomeUsuario = nomeUsuario
        self.senha = senha
        self.tipoUsuario = tipoUsuario

        self.gerenciador = gerenciador

class Orientadores:
    def __init__(self, codOrientador=0, nomeOrientador='', raOrientador=''):
        self.codOrientador = codOrientador
        self.nomeOrientador = nomeOrientador
        self.raOrientador = raOrientador
    
    def grava_orientador(self):
        bd_conn.bd_gravar(
            'insert into orientadores(nomeOrientador, raOrientador) values(%s, %s)',
            (self.nomeOrientador, self.raOrientador)
        )
        self.codOrientador = bd_conn.bd_busca_um(
            'select codOrientador from orientadores where raOrientador = (%s)', 
            (self.raOrientador,)
        )['codOrientador']