from biblioteca.models.dao import orientadores_dao
from biblioteca.models.classes import Orientadores
from biblioteca.util import json_res
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import DataError

def grava_orientador(req = None):
    try:
        orientadores = Orientadores(
            nomeOrientador=req.form['nomeOrientador'],
            raOrientador=req.form['raOrientador']
        )
        try:
            orientadores.grava_orientador()
        except DataError:
            return json_res.get_erro('O codigo do orientador deve ter no maximo 20 caracteres e seu nome no maximo 200')

        return json_res.get_ok('Orientador gravado com sucesso')
    except AttributeError:
        return json_res.get_erro('Valores invalidos para "nomeOrientador" e "raOrientador"')
    except BadRequestKeyError:
        return json_res.get_erro('Os campos "nomeOrientador" e "raOrientador" devem ser enviados no corpo da requisicao')

def busca_orientador(req):
    query = req.args.get('nomeOrientador')

    if query:
        ret = orientadores_dao.busca_orientadores_nome(query)
    else:
        ret = orientadores_dao.busca_orientadores()
    
    if ret:
        return json_res.get_data(ret)
    else:
        return json_res.get_falha('Nenhum orientador listado')

def get_count():
    count = orientadores_dao.get_count()
    return json_res.get_count(count)