from biblioteca.models.classes import Gerenciadores
from biblioteca.models.dao import gerenciadores_dao
from biblioteca.util import json_res
from werkzeug.exceptions import BadRequestKeyError
from mysql.connector.errors import IntegrityError

def grava_gerenciador(req):
    try:
        cpfGerenciador = req.form['cpfGerenciador']
        instituicao = req.form['instituicao']
        nomeGerenciador = req.form['nomeGerenciador']
        emailGerenciador = req.form['emailGerenciador']
    except BadRequestKeyError:
        return json_res.get_erro('A requisicao deve conter os campos "cpfGerenciador", "instituicao", "nomeGerenciador" e "emailGerenciador" em seu corpo')

    if not (cpfGerenciador and instituicao and nomeGerenciador and emailGerenciador):
        return json_res.get_falha('Os campos enviados deve ser preenchidos')

    gerenciador = Gerenciadores(
        cpfGerenciador= cpfGerenciador,
        instituicao= instituicao,
        nomeGerenciador= nomeGerenciador,
        emailGerenciador= emailGerenciador
    )
    try:
        gerenciador.grava_gerenciador()
        return json_res.get_ok('Gerenciador gravado com sucesso')
    except IntegrityError:
        if not gerenciadores_dao.is_ativo(gerenciador.cpfGerenciador):
            gerenciadores_dao.ativa_gerenciador(gerenciador)
            return json_res.get_ok('O gerenciador ja existia, porem esta inativo. O gerenciador foi reativado com os dados novos')
        else:
            return json_res.get_erro('O cpf {} ja foi cadastrado anteriormente'.format(cpfGerenciador))

def busca_gerenciador(req):
    query = req.args.get('nomeGerenciador')

    if query:
        ret = gerenciadores_dao.busca_gerenciadores_nome(query)
    else:
        ret = gerenciadores_dao.busca_gerenciadores()
        
    return json_res.get_data(ret)

def get_count():
    count = gerenciadores_dao.get_count()
    return json_res.get_count(count)

def deleta_gerenciador(codGerenciador):
    if not __cod_valido(codGerenciador):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    codGerenciador = int(codGerenciador)
    
    gerenciadores_dao.deleta_gerenciador(codGerenciador)
    return json_res.get_ok('Gerenciador deletado com sucesso')

def get_gerenciador(codGerenciador):
    if not __cod_valido(codGerenciador):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')
    codGerenciador = int(codGerenciador)

    ret = gerenciadores_dao.get_gerenciador(codGerenciador)
    if ret:
        return json_res.get_data(ret)
    return json_res.get_falha('Gerenciador requisitado nao existe')

def edita_gerenciador(codGerenciador, req):
    if not __cod_valido(codGerenciador):
        return json_res.get_erro('O valor enviado deve ser do tipo inteiro')

    try:
        nomeGerenciador = req.form['nomeGerenciador']
        instituicao = req.form['instituicao']
        emailGerenciador = req.form['emailGerenciador']
    except BadRequestKeyError:
        return json_res.get_erro('A requsicao deve conter os campos "nomeGerenciador", "instituicao" e "emailGerenciador" em seu corpo')
        
    codGerenciador = int(codGerenciador)

    if nomeGerenciador and instituicao and emailGerenciador:
        gerenciadores_dao.edita_gerenciador(codGerenciador, nomeGerenciador, instituicao, emailGerenciador)
        return json_res.get_ok('Gerenciador editado com sucesso')
    return json_res.get_falha('Os campos enviados nao podem ser vazios')

def __cod_valido(codGerenciador):
    try:
        int(codGerenciador)
        return True
    except ValueError:
        return False