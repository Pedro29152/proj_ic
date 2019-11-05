from biblioteca.models.classes import Gerenciadores
from biblioteca.models.dao import gerenciadores_dao
from biblioteca.util import json_res

def grava_gerenciador(req):
    gerenciador = Gerenciadores(
        cpfGerenciador=req.form['cpfGerenciador'],
        instituicao=req.form['instituicao'],
        nomeGerenciador=req.form['nomeGerenciador'],
        emailGerenciador=req.form['emailGerenciador']
    )

    if gerenciador.grava_gerenciador():
        return json_res.get_ok('Gerenciador gravado com sucesso')

    else:
        return json_res.get_falha('Falha ao gravar o gerenciador')

def busca_gerenciador(req):
    query = req.args.get('nomeGerenciador')

    if query:
        ret = gerenciadores_dao.busca_gerenciadores_nome(query)
    else:
        ret = gerenciadores_dao.busca_gerenciadores()
        
    return json_res.get_data(ret)

def get_count():
    count = gerenciadores_dao.get_count()
    return json_res.get_ok(count)