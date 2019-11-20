from biblioteca.models.classes import Cursos
from biblioteca.models.dao import cursos_dao
from biblioteca.util import json_res
from mysql.connector.errors import IntegrityError
from werkzeug.exceptions import BadRequestKeyError

def grava_curso(req):
    try:
        nomeCurso = req.form['nomeCurso'] 
        abreviacao = req.form['abreviacao']
    except BadRequestKeyError:
        return json_res.get_erro('A requisicao deve conter os campos "nomeCurso" e "abreviacao" em seu corpo')

    if not (nomeCurso and abreviacao):
        return json_res.get_falha('Os campos enviados devem sem preenchidos')

    curso = Cursos(
        nomeCurso, 
        abreviacao
    )
    try:
        curso.grava_curso()
        return json_res.get_ok('Curso gravado com suscesso')
    except IntegrityError:
        if not cursos_dao.is_ativo(curso):
            cursos_dao.reativa_curso(curso)
            return json_res.get_ok('O curso ja existia, porem esta inativo. O curso foi reativado com os dados novos')
        else:
            return json_res.get_erro('O nome ou a breviacao desse curso ja foi cadastrado')

def desativa_curso(codCurso):
    cursos_dao.desativa_curso(codCurso)

    return json_res.get_ok('Curso desativado com sucesso')

def ativa_curso(codCurso):
    cursos_dao.ativa_curso(codCurso)

    return json_res.get_ok('Curso ativado com sucesso')


def buscar_curso():
    cursos = cursos_dao.busca_cursos()
    
    return json_res.get_data(cursos)

def buscar_curso_inativo():
    cursos = cursos_dao.busca_cursos_inativo()
    
    return json_res.get_data(cursos)

def get_count():
    count = cursos_dao.get_count()
    return json_res.get_count(count)