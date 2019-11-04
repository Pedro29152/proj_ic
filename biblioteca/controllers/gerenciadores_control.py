from biblioteca.models.classes import Gerenciadores

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