from biblioteca.models.classes import Cursos
from biblioteca.models.dao import cursos_dao
from biblioteca.util import json_res

def grava_curso(req):
    curso = Cursos(
        req.form['nomeCurso'], 
        req.form['abreviacao']
    )

    return curso.grava_curso()

def desativa_curso(codCurso):
    cursos_dao.desativa_curso(codCurso)

    return json_res.get_ok('Curso desativado com sucesso')

def ativa_curso(codCurso):
    cursos_dao.ativa_curso(codCurso)

    return json_res.get_ok('Curso ativado com sucesso')


def buscar_curso():
    cursos = cursos_dao.busca_cursos()
    
    return json_res.get_data(cursos)

def get_count():
    count = cursos_dao.get_count()
    return json_res.get_count(count)