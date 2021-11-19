from flask import request
from enum import IntEnum

class Lang(IntEnum):
    PtBr = 1
    EnUs = 2

def get_lang():
    lang = request.args.get('lang')
    if not lang:
        lang = ''
        return Lang.PtBr.value
    
    if lang.lower() == 'pt-br':
        return Lang.PtBr.value
    elif lang.lower() == 'en-us':
        return Lang.EnUs.value
    else:
        return Lang.PtBr.value

def get_msg(msg_pt, msg_en):
    lang = get_lang()
    if lang == Lang.PtBr.value:
        return msg_pt
    elif lang == Lang.EnUs.value:
        return msg_en

def ACESSO_EXPIRADO():
    return get_msg(
        'Seu acesso está expirado', 
        'Your eccess expired'
    )
def SEM_AUTORIZACAO():
    return get_msg(
        'Sem autorização para esta ação', 
        'You do not have authorization to perform this action'
    )
def TOKEN_EXPIRADO():
    return get_msg(
        'Token expirado', 
        'Your token has expired'
    )
def TOKEN_NAO_ENVIADO():
    return get_msg(
        'Nenhum token enviado', 
        'No authorization token has been sent'
    )
def TOKEN_TIPO_INVALIDO():
    return get_msg(
        'O Token enviado é invalido', 
        'The token sent is invalid'
    )
def USUARIO_SENHA_INCORRETOS():
    return get_msg(
        'Usuario ou senha incorretos', 
        'User and password sent are invalid'
    )
def EMAIL_ENVIADO_SENHA_NOVA():
    return get_msg(
        'Um email foi enviado para você sobre sua nova senha', 
        'An e-mail were were sent to you about you new password'
    )

def PARAMETRO_NAO_ENVIADO(parametros):
    return get_msg(
        'O(s) parametro(s) {0} deve(m) ser enviado(s)'.format(parametros), 
        'The parameters {0} must be sent'.format(parametros)
    )
def CAMPOS_OBRIGATORIOS(campos):
    return get_msg(
        'A requisicao deve conter o(s) campo(s) {0} em seu corpo'.format(campos), 
        'The request must have the following fields in its body: {0}'.format(campos)
    )
def ATRIBUTO_OBRIGATORIO(campos):
    return get_msg(
        'O(s) campo(s) {0} deve(m) ser preenchido(s)'.format(campos), 
        'The folowing fields must be filled with data: {0}'.format(campos)
    )
def PREENCHIMENTO_OBRIGATORIO():
    return get_msg(
        'O(s) campo(s) enviado(s) deve(m) ser preenchido(s)', 
        'The fields that were sent must be filled'
    )
def NOME_ARQUIVO_MUITO_GRANDE():
    return get_msg(
        'O nome do arquivo enviado é muito grande', 
        'The file name sent is too long'
    )

def ENTIDADE_GRAVADA(entidade):
    return get_msg(
        '{0} gravado(a) com suscesso'.format(entidade), 
        '{0} were successfully recorded'.format(entidade)
    )
def ENTIDADE_ATIVADA(entidade):
    return get_msg(
        '{0} ativado(a) com sucesso'.format(entidade), 
        '{0} were successfully activated'.format(entidade)
    )
def ENTIDADE_DESATIVADA(entidade):
    return get_msg(
        '{0} desativado(a) com sucesso'.format(entidade), 
        '{0} were successfully disabled'.format(entidade)
    )
def ENTIDADE_EDITADA(entidade):
    return get_msg(
        '{0} editado(a) com sucesso'.format(entidade), 
        '{0} were successfully edited'.format(entidade)
    )
def ENTIDADE_DELETADA(entidade):
    return get_msg(
        '{0} deletado(a) com sucesso'.format(entidade), 
        '{0} were successfully deleted'.format(entidade)
    )
def ERRO_INTEGRIDADE(campo):
    return get_msg(
        '{0} ja cadastrado(s)'.format(campo), 
        '{0} has alredy been registered'.format(campo)
    )
def ERRO_INESPERADO(): 
    return get_msg(
        'Um erro inesperado ocorreu', 
        'An unexpected error has ocurred'
    )
def METODO_NAO_PERMITIDO():
    return get_msg(
        'Método não permitido', 
        'Method not allowed'
    )
def PAGINA_NAO_ENCONTRADA():
    return get_msg(
        'Página não encontrada', 
        'Page not found'
    )

def ARQUIVO_NAO_ENVIADO():
    return get_msg(
        'Nenhum arquivo foi enviado', 
        'No file has been sent'
    )
def EXTENSAO_NAO_SUPORTADA():
    return get_msg(
        'Extensão não suportada', 
        'Extension not supported'
    )
def NAO_ENCONTRADO(campo):
    return get_msg(
        '{0} não encontrado(a)'.format(campo), 
        '{0} not found'.format(campo)
    )
def NAO_FOI_POSSIVEL(acao):
    return get_msg(
        'Não foi possivel {0}'.format(acao), 
        'It was not possible to {0}'.format(acao)
    )
def NAO_FOI_POSSIVEL_ENVIAR_EMAIL():
    return get_msg(
        'Não foi possivel enviar o e-mail, por favor tente novamente mais tarde',
        'It was not possible to send the e-mail, please try again later'
    )
def ATRIBUTO_INVALIDO(campo):
    return get_msg(
        'O valor do campo {0} enviado é inválido'.format(campo), 
        'The value of the field {0} sent is invalid'.format(campo)
    )
def VALIDACAO_DEVE(campo, validacao):
    return get_msg(
        'O campo {0} deve {1}'.format(campo, validacao), 
        'The field {0} must {1}'.format(campo, validacao)
    )
def VALIDACAO_DEVEM(campos, validacao):
    return get_msg(
        'Os campos {0} devem {1}'.format(campos, validacao), 
        'The fields {0} must {1}'.format(campos, validacao)
    )
def EMAIL_ENVIADO():
    return get_msg(
        'Email enviado com sucesso', 
        'Email successfully sent'
    )
def SEM_PERMICAO(acao):
    return get_msg(
        'Voce nao pode {0}'.format(acao), 
        'You cannot {0}'.format(acao)
    )

def DADOS_PARAMETRO_INVALIDOS(parametros):
    return get_msg(
        'Os dados enviados nos parâmetros {0} são inválidos'.format(parametros), 
        'The data sent in the parameters {0} are invalid'.format(parametros)
    )
def TRABALHO_APROVADO():
    return get_msg(
        'Trabalho aprovado com sucesso', 
        'Work successfully approved'
    )
def TRABALHO_REPROVADO():
    return get_msg(
        'Trabalho reprovado com sucesso', 
        'Work successfullt refused'
    )
def USUARIO_NAO_EXISTE():
    return get_msg(
        'O usuario enviado nao existe ou está desativado',
        'The user sent does not exist or is disabled'
    )
def TIPO_USUARIO_ERRADO(tipoUsuario):
    return get_msg(
        'O usuario deve ser do tipo {0}'.format(tipoUsuario),
        'The user must be a {0}'.format(tipoUsuario)
    )
def USUARIO_NAO_RELACIONADO():
    return get_msg(
        'O usuário utilizado não possui um orientador ligado a ele', 
        'The user being utilized does not have an advisor related to it'
    )
def USUARIO_NAO_RELACIONADO_AUT():
    return get_msg(
        'O usuário utilizado não possui um autor ligado a ele', 
        'The user being utilized does not have an author related to it'
    )
def USUARIO_NAO_RELACIONADO_CURSO():
    return get_msg(
        'O usuário utilizado não possui um curso ligado a ele', 
        'The user being utilized does not have an course related to it'
    )
def SOLICITACAO_REVISAO_ENVIADA():
    return get_msg(
        'Solicitação de revisao enviada', 
        'The revision solicitation were sent'
    )
def ORIENTACAO_NECESSARIA():
    return get_msg(
        'Você precisa orientar este trabalho para efetuar esta ação', 
        'You need to be the advisor of this work to perform this action'
    )
def NAO_PODE_ALTERAR_PROJETO():
    return get_msg(
        'Você não pode cadastrar mais um trabalho, somente alterar o ja cadastrado caso ele ainda não tenha sido aprovado', 
        "You cannot register another work, you can only change the one alredy registered if it hasn't been alredy acknowledged"
    )

def CURSO_REATIVADO():
    return get_msg(
        'O curso ja existia, porem estava inativo. O curso foi reativado com os dados novos',
        'The course alredy existed, however, it was inactive. The course has been rectivated with the new information'
    )
def NOVA_ROTA_CADASTRO(entidade, uri):
    return get_msg(
        'Para cadastrar um {0} utilize a rota {1}'.format(entidade, uri),
        'To create a {0} use the route {1}'.format(entidade, uri)
    )
