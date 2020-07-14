from mysql.connector.errors import DataError, IntegrityError

from biblioteca import db
from biblioteca.ext_dao import palavras_chave_dao
from biblioteca.autor import autores_dao, projeto_autor_dao
from biblioteca.curso import cursos_dao
from biblioteca.usuarios import usuario_dao, usuario_orientado_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.responses import (
    get_erro,
    get_ok
)
from biblioteca.extensions import (
    TiposUsuario
)

QUERY_CURSO = '''
    select distinct pj.* 
    FROM projetos as pj
    NATURAL JOIN cursos 
    WHERE (descricaoCurso LIKE (%s) OR abreviacao LIKE (%s)) AND ativo = 1 and status = 1 '''
QUERY_TITULO = '''
    SELECT * 
    FROM projetos 
    WHERE tituloProjeto LIKE (%s) AND ativo = 1 and status = 1 '''
QUERY_DESCRICAO = '''
    SELECT * 
    FROM projetos 
    WHERE descricao LIKE (%s) AND ativo = 1 and status = 1 '''
QUERY_ORIENTADOR = '''
    select distinct pj.*
    FROM proj_ic.projetos as pj
    natural join projeto_orientador 
    natural join orientadores 
    where nomeOrientador like (%s) AND ativo = 1 and status = 1 
    '''
QUERY_AUTOR = '''
    select distinct pj.*
    from autores natural 
    join projeto_autor 
    natural join projetos pj 
    where nomeAutor like (%s) AND ativo = 1 and status = 1 
    '''
QUERY_PALAVRAS_CHAVE = '''
    select distinct pj.*
    from palavras_chave natural 
    join projetos pj 
    where palavraChave like (%s) AND ativo = 1 and status = 1 
    '''
    
def busca_projeto_tipo(tipo, query = '', ordem = 0, crescente = True):
    query = '%' + query + '%'

    ret = None

    if tipo == 'titulo':
        ret = __busca_projeto_full(
            QUERY_TITULO + 
            __ordena(ordem,crescente),
            (query,)   
        )
    elif tipo == 'curso':
        ret = __busca_projeto_full(
            QUERY_CURSO + 
            __ordena(ordem,crescente),
            (query, query)
        )
    elif tipo == 'descricao':
        ret = __busca_projeto_full(
            QUERY_DESCRICAO + 
            __ordena(ordem,crescente),
            (query,)
        )
    elif tipo == 'orientador':
        ret = __busca_projeto_full(
            QUERY_ORIENTADOR + __ordena(ordem,crescente),
            (query,)
        )
    elif tipo == 'autor':
        ret = __busca_projeto_full(
            QUERY_AUTOR + __ordena(ordem,crescente),
            (query,)
        )

    elif tipo == 'palavrasChave':
        ret = __busca_projeto_full(
            QUERY_PALAVRAS_CHAVE +
            __ordena(ordem, crescente),
            (query,)
        )
    else:
        ret = None

    return ret

def busca_projeto_tipo_pag(tipo, query = '', ordem = 0, crescente = True, pag = 1):
    query = '%' + query + '%'

    ret = None

    if tipo == 'titulo':
        ret = __busca_projeto_full(
            QUERY_TITULO + 
            __ordena(ordem,crescente) + __get_limit(pag),
            (query,)   
        )
    elif tipo == 'curso':
        ret = __busca_projeto_full(
            QUERY_CURSO + 
            __ordena(ordem,crescente) + __get_limit(pag),
            (query, query)
        )
    elif tipo == 'descricao':
        ret = __busca_projeto_full(
            QUERY_DESCRICAO + 
            __ordena(ordem,crescente) + __get_limit(pag),
            (query,)
        )
    elif tipo == 'orientador':
        ret = __busca_projeto_full(
            QUERY_ORIENTADOR + __ordena(ordem,crescente) + __get_limit(pag),
            (query,)
        )
    elif tipo == 'autor':
        ret = __busca_projeto_full(
            QUERY_AUTOR + __ordena(ordem,crescente) + __get_limit(pag),
            (query,)
        )

    elif tipo == 'palavrasChave':
        ret = __busca_projeto_full(
            QUERY_PALAVRAS_CHAVE +
            __ordena(ordem, crescente) + __get_limit(pag),
            (query,)
        )
    else:
        ret = None

    return ret

def busca_projeto():
    query = 'select * from projetos where ativo = 1 and status = 1 '

    ret = db.bd_busca(
        query,None
    )

    prenche_projetos(ret)

    return ret

def busca_projeto_pag(pag):
    query = 'select * from projetos where ativo = 1 and status = 1 ' + __get_limit(pag)

    ret = db.bd_busca(
        query,None
    )

    prenche_projetos(ret)

    return ret

def busca_projeto_ranking(titulo, tipo, ordem):
    titulo = '%{}%'.format(titulo)
    
    query = 'select * from projetos where tituloProjeto like (%s) and ativo = 1 and status = 1 '
    
    if tipo == 'numVisitas':
        query += 'order by numVisitas' + ordem
    elif tipo == 'numDownloads':
        query += 'order by numDownloads' + ordem
    else:
        query += 'order by numVisitas' + ordem

    return __busca_projeto_full(query, (titulo,))

def busca_projeto_ranking_pag(titulo, tipo, ordem, pag):
    titulo = '%{}%'.format(titulo)

    query = 'select * from projetos where tituloProjeto like (%s) and ativo = 1 and status = 1 '
    
    if tipo == 'numVisitas':
        query += 'order by numVisitas' + ordem
    elif tipo == 'numDownloads':
        query += 'order by numDownloads' + ordem
    
    query += __get_limit(pag, 5)

    return __busca_projeto_full(query, (titulo,))

def busca_projeto_orientador(codOrientador):
    query = '''
        select distinct p.*
        from projetos as p
        natural join projeto_orientador
        where ativo = 1 and status = 0 and codOrientador = (%s)
    '''
    ret = db.bd_busca(query, (codOrientador,))

    prenche_projetos(ret)

    return ret

def busca_projetos_codCurso(codCurso):
    query = '''
        select p.* from projetos as p
        natural join cursos as c 
        where p.ativo = 1 and p.status = 1 and p.codCurso = (%s)
    '''
    ret = db.bd_busca(query, (codCurso,))

    prenche_projetos(ret)

    return ret

def get_projeto_orientador(codOrientador, codProjeto):
    query = '''
        select p.*
        from projetos as p
        natural join projeto_orientador
        where ativo = 1 and status = 0 and codOrientador = (%s) and codProjeto = (%s)
    '''
    ret = db.bd_busca_um(query, (codOrientador, codProjeto))

    prenche_projeto(ret)

    return ret

def busca_projeto_orientador_publico(codOrientador):
    query = '''
        select p.*
        from projetos as p
        natural join projeto_orientador
        where ativo = 1 and status = 1 and codOrientador = (%s)
    '''
    ret = db.bd_busca(query, (codOrientador,))

    prenche_projetos(ret)

    return ret

def busca_projeto_inativo():
    query = '''
        select * from projetos where ativo = 0 and status = 1
    '''
    ret = db.bd_busca(query, None)

    if ret:
        prenche_projetos(ret)

    return ret

def busca_todos_projetos():
    query = '''
        select * from projetos where status = 1
    '''
    ret = db.bd_busca(query, None)

    if ret:
        prenche_projetos(ret)

    return ret


def buscar_projetos_codCurso_novo(codCurso, is_full=False):
    query = '''
        select * from projetos 
        where codCurso = (%s) and ativo = 1 and status = 0
    ''' 
    ret = db.bd_busca(query, (codCurso,))
    if is_full and ret:
        prenche_projetos(ret)
    return ret

def get_cod_projeto_titulo(titulo):
    query = 'SELECT codProjeto FROM projetos WHERE tituloProjeto = (%s) ORDER BY codProjeto DESC'

    val = db.bd_busca_um(
        query, 
        (titulo,)
    )

    return val['codProjeto']

def get_count(codOrientador=None):
    if codOrientador:
        query = 'select count(*) as projetos from projetos natural join projeto_orientador where ativo = 1 and codOrientador = (%s)'
        ret = db.bd_busca_um(query, (codOrientador,))
    else:
        query = 'select count(*) as projetos from projetos where ativo = 1'
        ret = db.bd_busca_um(query, None)
    return ret['projetos']

def __ordena(ordem, crescente):
    cres = ''
    if(not crescente):
        cres = 'DESC'

    if(ordem == 0):
        return ''
    
    elif(ordem == 3):
        return 'ORDER BY numVisitas  ' + cres
    
    elif(ordem == 4):
        return 'ORDER BY numDownloads  ' + cres
    
    elif(ordem == 5):
        return 'ORDER BY dataAvaliacao ' + cres
    
    elif(ordem == 6):
        return 'ORDER BY dataEnvio  ' + cres
    else:
        return ''


def grava_projeto(projeto, is_secretaria=True):
    if is_secretaria:
        db.bd_gravar(
            'insert into projetos'+
            '(tituloProjeto, subTitulo, descricao, nomeArquivo, dataAvaliacao, codCurso, status, linguagem)'+
            'values(%s,%s,%s,%s,%s,%s,1,%s)',
            (projeto.tituloProjeto,
            projeto.subTitulo,
            projeto.descricao, 
            projeto.nomeArquivo, 
            projeto.dataAvaliacao,
            projeto.curso.codCurso,
            projeto.linguagem)
        )
    else:
        db.bd_gravar(
            'insert into projetos'+
            '(tituloProjeto, subTitulo, descricao, nomeArquivo, dataAvaliacao, codCurso, linguagem)'+
            'values(%s,%s,%s,%s,%s,%s,%s)',
            (projeto.tituloProjeto,
            projeto.subTitulo,
            projeto.descricao, 
            projeto.nomeArquivo, 
            projeto.dataAvaliacao,
            projeto.curso.codCurso,
            projeto.linguagem)
        )

    projeto.codProjeto = get_cod_projeto_titulo(projeto.tituloProjeto)
    
    for aut in projeto.autores:
        try:
            codAutor = aut.tenta_gravar_autor(projeto.codProjeto)
        except DataError:
            deleta_projeto(projeto.codProjeto)
            raise Exception('O ra enviado deve ter no maximo 13 caracteres e o nome deve ter no maximo 200')
        try:
            projeto_autor_dao.grava_autor_proj(projeto.codProjeto, codAutor)
        except IntegrityError:
            deleta_projeto(projeto.codProjeto)
            raise Exception('Voce nao pode cadastrar dois alunos com o mesmo ra no mesmo projeto')

    for palavra in projeto.palavrasChave:
        palavra.grava_palavra_chave(projeto.codProjeto)

    __grava_proj_ori(projeto.codProjeto, projeto.orientador.codOrientador)

    return projeto

def deleta_projeto(codProjeto):
    query = 'delete from projetos where codProjeto = (%s)'
    db.bd_gravar(query, (codProjeto,))

def get_projeto_novo(codProjeto, is_full=False):
    query = 'select * from projetos where codProjeto = (%s) and status = 0'
    proj = db.bd_busca_um(query,(codProjeto,))
    if is_full and proj:
        prenche_projeto(proj)
    return proj

def get_projeto_novo_codAutor(codAutor, is_full=False):
    query = 'select p.* from projetos as p natural join projeto_autor where codAutor = (%s) and status = 0'
    proj = db.bd_busca_um(query,(codAutor,))
    if is_full:
        prenche_projeto(proj)
    return proj

def get_projeto(codProjeto, is_full=False):
    query = 'select * from projetos where codProjeto = (%s) and ativo = 1 and status = 1'
    proj = db.bd_busca_um(query,(codProjeto,))
    if is_full and proj:
        prenche_projeto(proj)
    return proj

def get_projeto_inativo(codProjeto):
    query = '''
        select * from projetos where codProjeto = (%s) and ativo = 0 and status = 1
    '''
    ret = db.bd_busca_um(query, (codProjeto,))

    if ret:
        prenche_projeto(ret)

    return ret

def desativa_projeto(codProjeto):
    query = 'update projetos set ativo = 0 where codProjeto = (%s)'

    db.bd_gravar(query, (codProjeto,))

def ativa_projeto(codProjeto):
    query = 'update projetos set ativo = 1 where codProjeto = (%s)'

    db.bd_gravar(query, (codProjeto,))

def aprovar_projeto(codProjeto):
    query = '''
        update projetos set status = 1 where codProjeto = (%s)
    '''
    db.bd_gravar(query, (codProjeto,))

    user = usuario_orientado_dao.get_usuario_codProjeto(codProjeto)
    if user:
        if user['tipoUsuario'] == TiposUsuario.Aluno.value:
            usuario_dao.desativar_aluno(user['codUsuario'])
        else:
            usuario_dao.desativa_usuario(user['codUsuario'])

def recusar_projeto(codProjeto):
    query = '''
        update projetos set status = 2 where codProjeto = (%s)
    '''
    db.bd_gravar(query, (codProjeto,))
    
    user = usuario_orientado_dao.get_usuario_codProjeto(codProjeto)
    if user:    
        if user['tipoUsuario'] == TiposUsuario.Aluno.value:
            usuario_dao.desativar_aluno(user['codUsuario'])
        else:
            usuario_dao.desativa_usuario(user['codUsuario'])

def edita_titulo(codProjeto, titulo):
    query = 'update projetos set tituloProjeto = (%s) where codProjeto = (%s)'

    db.bd_gravar(query, (titulo, codProjeto))

def edita_descricao(codProjeto, descricao):
    query = 'update projetos set descricao = (%s) where codProjeto = (%s)'

    db.bd_gravar(query, (descricao, codProjeto))

def edita_subtitulo(codProjeto, subtitulo):
    query = 'update projetos set subTitulo = (%s) where codProjeto = (%s)'

    db.bd_gravar(query, (subtitulo, codProjeto))

def is_ativo_filename(filename):
    query = 'select codProjeto from projetos where nomeArquivo = (%s) and ativo = 1 and not status = 2 '

    ret = db.bd_busca_um(query, (filename,))

    if ret:
        return ret['codProjeto']
    return None

def is_valid_project(codAutor):
    query = '''
        select * from projeto_autor 
        natural join projetos 
        where codAutor = (%s) and (status = 0)
    '''
    res = db.bd_busca_um(query, (codAutor,))

    if res:
        return False
    return True

def is_orientador_projeto_novo(codProjeto, codOrientador):
    query = '''
        select distinct p.codProjeto 
        from orientadores as o 
        natural join projeto_orientador as po 
        join projetos as p 
        on p.codProjeto = po.codProjeto 
        where p.codProjeto = (%s) and o.codOrientador = (%s) and p.status = 0
    '''
    if db.bd_busca_um(query, (codProjeto, codOrientador)):
        return True
    return False

def download_file(codProjeto):
    query = 'UPDATE projetos SET numDownloads = numDownloads + 1 WHERE codProjeto = (%s)'

    db.bd_gravar(query, (codProjeto,))

def add_view(codProjeto):
    query = 'UPDATE projetos SET numVisitas = numVisitas + 1 WHERE codProjeto = (%s)'

    db.bd_gravar(query, (codProjeto,))

def prenche_projetos(ret):
    for item in ret:
        prenche_projeto(item)

def prenche_projeto(ret):
    ret['autores'] = autores_dao.busca_autores_proj(ret['codProjeto'])
    ret['palavrasChave'] = palavras_chave_dao.busca_palavras_chave(ret['codProjeto'])
    ret['curso'] = cursos_dao.get_all_curso_cod(ret['codCurso'])
    ret['orientador'] = orientadores_dao.busca_orientadores_codProjeto(ret['codProjeto'])

def __grava_proj_ori(codProjeto, codOrientador):
    query = 'insert into projeto_orientador values(%s, %s)'

    db.bd_gravar(query, (codOrientador, codProjeto))

def __get_limit(pag, tam = 20):
    fi = 1 + ((pag - 1) * tam)
    ff = pag * tam

    return ' LIMIT {}, {}'.format(fi, ff)

def __busca_projeto_full(query, *args):
    ret = db.bd_busca(query, *args)

    prenche_projetos(ret)
    
    return ret
