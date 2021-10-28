from biblioteca.db import Db, response_messages

class Cursos:
    def __init__(self, descricaoCurso="", abreviacao="", codUsuario="", codCurso=0, db=None):
        self.codCurso = codCurso
        self.descricaoCurso = descricaoCurso
        self.abreviacao = abreviacao
        self.codUsuario = codUsuario
        
        self.db=db

    def __str__(self):
        return str(self.codCurso) + ' ' + self.descricaoCurso + ' ' + self.abreviacao

    def grava_curso(self):
        if(self.descricaoCurso and self.abreviacao and self.codUsuario):
            query = 'insert into cursos(descricaoCurso, abreviacao, ativo, codUsuario) values(%s,%s,1,%s)'
            self.db.gravar(query, (self.descricaoCurso, self.abreviacao, self.codUsuario))
            return True
        else:
            return False

    def edita_curso(self):
        if not (self.codCurso or self.descricaoCurso or self.abreviacao):
            raise AttributeError(response_messages.ATRIBUTO_OBRIGATORIO('"codCurso", "descricaoCurso" e "abreviacao"'))
        query = 'update cursos set descricaoCurso = (%s), abreviacao = (%s) where codCurso = (%s)'
        self.db.gravar(query, (self.descricaoCurso, self.abreviacao, self.codCurso))
