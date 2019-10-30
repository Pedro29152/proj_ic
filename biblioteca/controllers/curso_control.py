from biblioteca.models import classes
from biblioteca.models.dao import cursos_dao
from flask import redirect, url_for

def grava_curso(req):
    curso = classes.Cursos(
        req.form['nomeCurso'], 
        req.form['abreviacao']
    )

    return curso.grava_curso()

