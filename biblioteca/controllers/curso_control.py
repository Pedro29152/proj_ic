from biblioteca.models import classes
from biblioteca.models.dao import cursos_dao
from biblioteca.util import json_res

def grava_curso(req):
    curso = classes.Cursos(
        req.form['nomeCurso'], 
        req.form['abreviacao']
    )

    return curso.grava_curso()

def buscar_curso():
    cursos = cursos_dao.busca_cursos()
    
    return json_res.get_data(cursos)

def get_count():
    count = cursos_dao.get_count()
    return json_res.get_count(count)