from  biblioteca import bd_conn

def busca_gerenciador(cpf):

    cpf = '%' + cpf + '%'
    val = bd_conn.bd_busca(
        'select * from gerenciadores where cpfGerenciador like (%s)',
        (cpf,)
    )

    return val


def grava_gerenciador(cpf, inst, nome):
    bd_conn.bd_gravar('insert into gerenciadores(cpfGerenciador,instituicao,nomeGerenciador)'+
        'values(%s,%s,%s)',
        (cpf, inst, nome)
    )
        

def get_codGer_usr(nome): 
    val = ""

    query = bd_conn.bd_busca_um(
        'select gerenciadores.codGerenciador '+ 
        'from usuarios '+ 
        'natural join gerenciadores '+
        'where usuarios.nomeUsuario = (%s)',
        (nome, )
    )

    if(query != None):
        val = query['codGerenciador']

    return val

def get_codGer(nome):
    query = bd_conn.bd_busca_um(
        'select * from gerenciadores where nomeGerenciador = %s',
        (nome,)
    )

    val = ""
    if(query != None):
        val = query['codGerenciador']

    return val