from biblioteca.models.classes import Gerenciadores
from biblioteca.models.dao import gerenciadores_dao

def grava_gerenciador(req):
    gerenciador = Gerenciadores(
        cpfGerenciador=req['cpfGerenciador'],
        instituicao=req['instituicao'],
        nomeGerenciador=req['nomeGerenciador']
    )

    if gerenciador.grava_gerenciador():
        return {
            'status': 'OK',
            'message': 'Gerenciador gravado com sucesso'
        }

    else:
        return {
            'status': 'falha',
            'message': 'Falha ao gravar o gerenciador'
        }

def busca_gerenciador(req):
    query = req.args.get('nomeGerenciador')

    if query:
        ret = gerenciadores_dao.busca_gerenciadores_nome(query)
    else:
        ret = gerenciadores_dao.busca_gerenciadores()
        
    return {
        'status': 'OK',
        'data': ret
    }