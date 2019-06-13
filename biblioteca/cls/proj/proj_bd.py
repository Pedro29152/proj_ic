from  biblioteca import bd_conn

def busca_projeto(titulo):
    titulo = "%" + titulo + "%"
    return bd_conn.bd_busca('select * from projetos where tituloProjeto like (%s)', titulo)

def grava_projeto(titulo, nomeOrientador, descricao, nomeArquivo, notaProj, dataAvaliacao,codGer,codCurso):
    bd_conn.bd_gravar(
        'insert into projetos'+
        '(tituloProjeto,nomeOrientador,descricao,nomeArquivo,notaProjeto,dataAvaliacao,codGerenciador,codCurso,ativo)'+
        'values(%s,%s,%s,%s,%s,%s,%s,%s,1)',
        (titulo,nomeOrientador,descricao,nomeArquivo,notaProj,dataAvaliacao,codGer,codCurso)
    )

