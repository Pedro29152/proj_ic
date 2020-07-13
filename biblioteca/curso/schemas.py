from biblioteca import db

class Cursos:
    def __init__(self, descricaoCurso="", abreviacao="", codUsuario="", codCurso=0):
        self.codCurso = codCurso
        self.descricaoCurso = descricaoCurso
        self.abreviacao = abreviacao
        self.codUsuario = codUsuario

    def __str__(self):
        return str(self.codCurso) + ' ' + self.descricaoCurso + ' ' + self.abreviacao

    def grava_curso(self):
        if(self.descricaoCurso and self.abreviacao and self.codUsuario):
            db.bd_gravar(
                'insert into cursos(descricaoCurso, abreviacao, ativo, codUsuario) values(%s,%s,1,%s)',
                (self.descricaoCurso, self.abreviacao, self.codUsuario)
            )
            return True
        else:
            return False

    def edita_curso(self):
        if not (self.codCurso or self.descricaoCurso or self.abreviacao):
            raise AttributeError('Os campos "codCurso", "descricaoCurso" e "abreviacao" devem ser preenchidos')
        
        db.bd_gravar(
            'update cursos set descricaoCurso = (%s), abreviacao = (%s) where codCurso = (%s)',
            (self.descricaoCurso, self.abreviacao, self.codCurso)
        )
