from biblioteca.cls.curso import curso_bd

def grava_curso(req):
    nome = req.form['nomeCurso']
    abbr = req.form['abreviacao']

    curso_bd.grava_curso(nome, abbr)
