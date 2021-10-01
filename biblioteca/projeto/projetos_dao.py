import os
from os import getenv

from flask import current_app as app
from mysql.connector.errors import DataError, IntegrityError, ProgrammingError

from biblioteca.db import Db, response_messages
from biblioteca.ext_dao import palavras_chave_dao
from biblioteca.autor import autores_dao, projeto_autor_dao
from biblioteca.curso import cursos_dao
from biblioteca.usuarios import usuario_orientado_dao
from biblioteca.usuarios import usuario_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.responses import (
    get_erro,
    get_ok
)
from biblioteca.extensions import (
    TiposUsuario,
    TiposOrientador,
    AtributosEspeciaisProjeto,
    get_enum_obj,
    separate_camel_case as scc
)

QUERY_CURSO = '''
    select distinct pj.* 
    FROM projetos as pj
    NATURAL JOIN cursos 
    WHERE (descricaoCurso LIKE (%s) OR abreviacao LIKE (%s)) AND ativo = 1 and status = 1 '''
QUERY_TITULO = '''
    SELECT * 
    FROM projetos 
    WHERE tituloProjeto LIKE (%s) AND ativo = 1 and status = 1
    '''
QUERY_DESCRICAO = '''
    SELECT * 
    FROM projetos 
    WHERE descricao LIKE (%s) AND ativo = 1 and status = 1 '''
QUERY_ORIENTADOR = '''
    select distinct pj.*
    FROM projetos as pj
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
QUERY_MODALIDADE = '''
    SELECT * 
    FROM projetos 
    WHERE modalidade = (%s) AND ativo = 1 and status = 1
    '''

def busca_projeto_tipo(tipo, query = '', ordem = 0, crescente = True):
    queryBase = query
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
    elif tipo == 'orientadores':
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
    elif tipo == 'modalidade':
        ret = __busca_projeto_full(
            QUERY_MODALIDADE +
            __ordena(ordem, crescente),
            (queryBase,)
        )
    else:
        ret = None

    return ret

def busca_projeto_tipo_pag(tipo, query = '', ordem = 0, crescente = True, pag = 1):
    queryBase = query
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
    elif tipo == 'orientadores':
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
    elif tipo == 'modalidade':
        ret = __busca_projeto_full(
            QUERY_MODALIDADE +
            __ordena(ordem, crescente) + __get_limit(pag),
            (queryBase,)
        )
    else:
        ret = None

    return ret

def busca_projeto(proj_attr=[], proj_attr_esp=None, data_i= None, data_f= None):
    with Db() as db:
        attr = busca_atributos_projeto()
        keys = list(attr.keys())
        atributos = list(set(proj_attr) & set(keys))

        if len(atributos) > 0:
            atrib = ', '.join([attr[a] for a in atributos])
        else:
            atrib = ', '.join([attr[a] for a in keys])
        
        if not (proj_attr_esp == None): 
            attrEsp = get_enum_obj(AtributosEspeciaisProjeto)
            keysEsp = list(attrEsp.keys())
            atributosEsp = list(set(proj_attr_esp) & set(keysEsp))
        else:
            atributosEsp = None
        
        if data_i and data_f:
            query = f'''
                select codProjeto, codCurso, {atrib}
                from projetos
                where (ativo = 1 and status = 1) and dataAvaliacao between %s and %s
            '''
            try:
                ret = db.busca(query, (data_i, data_f))
            except ProgrammingError:
                return None
        else:
            query = f'''
                select codProjeto, codCurso, {atrib}
                from projetos
                where (ativo = 1 and status = 1)
            '''
            try:
                ret = db.busca(query)
            except ProgrammingError:
                return None

        prenche_projetos(ret, attrs=atributosEsp)

        return ret

def busca_reltorio_projeto_orientador(codOrientador, proj_attr=[], proj_attr_esp=None, data_i= None, data_f= None):
    with Db() as db:
        attr = busca_atributos_projeto()
        keys = list(attr.keys())
        atributos = list(set(proj_attr) & set(keys))

        if len(atributos) > 0:
            atrib = ', '.join([attr[a] for a in atributos])
        else:
            atrib = ', '.join([attr[a] for a in keys])
        
        if not (proj_attr_esp == None): 
            attrEsp = get_enum_obj(AtributosEspeciaisProjeto)
            keysEsp = list(attrEsp.keys())
            atributosEsp = list(set(proj_attr_esp) & set(keysEsp))
        else:
            atributosEsp = None
        
        if data_i and data_f:
            query = f'''
                select codProjeto, codCurso, {atrib}
                from projetos as p
                natural join projeto_orientador as po
                where (ativo = 1 and status = 1) and (and dataAvaliacao between %s and %s) and (po.codOrientador = %s and po.tipoOrientador = 0)
                order by p.tituloProjeto, p.dataAvaliacao
            '''
            try:
                ret = db.busca(query, (data_i, data_f, codOrientador))
            except ProgrammingError:
                return None
        else:
            query = f'''
                select codProjeto, codCurso, {atrib}
                from projetos as p
                natural join projeto_orientador as po
                where (ativo = 1 and status = 1) and (po.codOrientador = %s and po.tipoOrientador = 0)
                order by p.tituloProjeto, p.dataAvaliacao
            '''
            try:
                ret = db.busca(query, (codOrientador,))
            except ProgrammingError:
                return None

        prenche_projetos(ret, attrs=atributosEsp)

        return ret

def busca_projeto_pag(pag):
    with Db() as db:
        query = 'select * from projetos where ativo = 1 and status = 1 ' + __get_limit(pag)

        ret = db.busca(
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
    else:
        query += 'order by numVisitas' + ordem
    
    query += __get_limit(pag, 5)

    return __busca_projeto_full(query, (titulo,))

def busca_projeto_orientador(codOrientador):
    with Db() as db:
        query = '''
            select p.*
            from projetos as p
            natural join projeto_orientador
            where ativo = 1 and status = 1 and codOrientador = (%s)
        '''
        ret = db.busca(query, (codOrientador,))

        if ret:
            prenche_projetos(ret)

        return ret

def busca_projeto_orientador_novo(codOrientador):
    with Db() as db:
        query = '''
            select distinct p.*
            from projetos as p
            natural join projeto_orientador as po
            natural join usuario_orientado as uo
            where p.ativo = 1 and p.status = 0 and po.codOrientador = (%s) and uo.dataValidade >= current_timestamp()
        '''
        ret = db.busca(query, (codOrientador,))
        
        if ret:
            prenche_projetos(ret)

        return ret

def busca_projetos_codCurso(codCurso):
    with Db() as db:
        query = '''
            select p.* from projetos as p
            natural join cursos as c 
            where p.ativo = 1 and p.status = 1 and p.codCurso = (%s)
        '''
        ret = db.busca(query, (codCurso,))

        prenche_projetos(ret)

        return ret

def get_projeto_orientador(codOrientador, codProjeto):
    with Db() as db:
        query = '''
            select p.*
            from projetos as p
            natural join projeto_orientador
            where ativo = 1 and status = 1 and codOrientador = (%s) and codProjeto = (%s)
        '''
        ret = db.busca_um(query, (codOrientador, codProjeto))

        return ret

def busca_projeto_orientador_publico(codOrientador):
    with Db() as db:
        query = '''
            select p.*
            from projetos as p
            natural join projeto_orientador
            where (ativo = 1 and status = 1) and codOrientador = (%s)
        '''
        ret = db.busca(query, (codOrientador,))

        prenche_projetos(ret)

        return ret

def busca_projeto_inativo():
    with Db() as db:
        query = '''
            select * from projetos where ativo = 0 and status = 1
        '''
        ret = db.busca(query, None)

        if ret:
            prenche_projetos(ret)

        return ret

def busca_todos_projetos():
    with Db() as db:
        query = '''
            select * from projetos where status = 1
        '''
        ret = db.busca(query, None)

        if ret:
            prenche_projetos(ret)

        return ret

def buscar_projetos_codCurso_novo(codCurso, is_full=False):
    with Db() as db:
        query = '''
            select * from projetos 
            where codCurso = (%s) and ativo = 1 and status = 0
        ''' 
        ret = db.busca(query, (codCurso,))
        if is_full and ret:
            prenche_projetos(ret)
        return ret

def get_cod_projeto_titulo(titulo):
    with Db() as db:
        query = 'SELECT codProjeto FROM projetos WHERE tituloProjeto = (%s) ORDER BY codProjeto DESC'

        val = db.busca_um(
            query, 
            (titulo,)
        )

        return val['codProjeto']

def get_count(codOrientador=None):
    with Db() as db:
        if codOrientador:
            query = 'select count(*) as projetos from projetos natural join projeto_orientador where ativo = 1 and codOrientador = (%s)'
            ret = db.busca_um(query, (codOrientador,))
        else:
            query = 'select count(*) as projetos from projetos where ativo = 1'
            ret = db.busca_um(query, None)
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
    with Db() as db:
        if is_secretaria:
            query = '''
                insert into projetos 
                (tituloProjeto, subtitulo, descricao, nomeArquivo, dataAvaliacao, codCurso, status, linguagem, modalidade, localPublicacao) 
                values(%s,%s,%s,%s,%s,%s,1,%s,%s,%s)
            '''
        else:
            query = '''
                insert into projetos 
                (tituloProjeto, subtitulo, descricao, nomeArquivo, dataAvaliacao, codCurso, linguagem, modalidade, localPublicacao) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        
        db.gravar_autocommit(query,
            (projeto.tituloProjeto,
            projeto.subTitulo,
            projeto.descricao, 
            projeto.nomeArquivo, 
            projeto.dataAvaliacao,
            projeto.curso.codCurso,
            projeto.linguagem,
            projeto.modalidade,
            projeto.localPublicacao)
        )

        projeto.codProjeto = get_cod_projeto_titulo(projeto.tituloProjeto)
        
        for aut in projeto.autores:
            try:
                codAutor = aut.tenta_gravar_autor(projeto.codProjeto)
            except DataError:
                deleta_projeto(projeto.codProjeto)
                raise Exception(response_messages.VALIDACAO_DEVE('ra', 'ter no maximo 13 caracteres e o nome deve ter no maximo 200'))
            try:
                projeto_autor_dao.grava_autor_proj(projeto.codProjeto, codAutor)
            except IntegrityError:
                deleta_projeto(projeto.codProjeto)
                raise Exception(response_messages.SEM_PERMICAO('cadastrar dois alunos com o mesmo ra no mesmo trabalho'))

        for palavra in projeto.palavrasChave:
            palavra.grava_palavra_chave(projeto.codProjeto)

        __grava_proj_ori(projeto.codProjeto, projeto.orientador.codOrientador, TiposOrientador.Principal.value)
        if projeto.coOrientador:
            __grava_proj_ori(projeto.codProjeto, projeto.coOrientador.codOrientador, TiposOrientador.CoOrientador.value)


        return projeto

def deleta_projeto(codProjeto):
    with Db() as db:
        query = 'delete from projetos where codProjeto = (%s)'
        db.gravar_autocommit(query, (codProjeto,))

def get_projeto_novo(codProjeto, is_full=False):
    with Db() as db:
        query = 'select * from projetos where codProjeto = (%s) and status = 0'
        proj = db.busca_um(query,(codProjeto,))
        if is_full and proj:
            prenche_projeto(proj)
        return proj

def get_projeto_novo_codAutor(codAutor, is_full=False):
    with Db() as db:
        query = '''
            select p.* from projetos as p 
            natural join projeto_autor 
            where codAutor = (%s) and status = 0
        '''
        proj = db.busca_um(query,(codAutor,))
        if is_full and proj:
            prenche_projeto(proj)
        return proj

def get_projeto_novo_codOrientador(codOrientador, is_full=False):
    with Db() as db:
        query = '''
            select p.* from projetos as p 
            natural join projeto_orientador 
            where codOrientador = (%s) and status = 0
        '''
        proj = db.busca_um(query,(codOrientador,))
        if is_full and proj:
            prenche_projeto(proj)
        return proj

def get_projeto_novo_codCurso(codCurso, is_full=False):
    with Db() as db:
        query = '''
            select * from projetos 
            where codCurso = (%s) and status = 0
        '''
        proj = db.busca_um(query,(codCurso,))
        if is_full and proj:
            prenche_projeto(proj)
        return proj

def get_projeto(codProjeto, is_full=False):
    with Db() as db:
        query = 'select * from projetos where codProjeto = (%s) and ativo = 1 and status = 1'
        proj = db.busca_um(query,(codProjeto,))
        if is_full and proj:
            prenche_projeto(proj)
        return proj

def get_projeto_inativo(codProjeto):
    with Db() as db:
        query = '''
            select * from projetos where codProjeto = (%s) and ativo = 0 and status = 1
        '''
        ret = db.busca_um(query, (codProjeto,))

        if ret:
            prenche_projeto(ret)

        return ret

def get_projeto_codUsuarioOrientado(codUsuarioOrientado):
    with Db() as db:
        query = '''
            select * from projetos as p
            join usuario_orientado as uo
            on uo.codProjeto = p.codProjeto
            where codUsuarioOrientado = (%s)
        '''
        ret = db.busca_um(query, (codUsuarioOrientado,))

        if ret:
            prenche_projeto(ret)
        
        return ret

def desativa_projeto(codProjeto):
    with Db() as db:
        query = 'update projetos set ativo = 0 where codProjeto = (%s)'

        db.gravar_autocommit(query, (codProjeto,))

def ativa_projeto(codProjeto):
    with Db() as db:
        query = 'update projetos set ativo = 1 where codProjeto = (%s)'

        db.gravar_autocommit(query, (codProjeto,))

def aprovar_projeto(codProjeto):
    with Db() as db:
        usuarioDao = usuario_dao.UsuarioDAO(db)

        query = '''
            update projetos set status = 1 where codProjeto = (%s)
        '''
        db.gravar_autocommit(query, (codProjeto,))

        user = usuario_orientado_dao.get_usuario_codProjeto(codProjeto)
        if user:
            if user['tipoUsuario'] == TiposUsuario.Aluno.value:
                usuarioDao.desativar_aluno(user['codUsuario'])
            else:
                usuarioDao.desativa_usuario(user['codUsuario'])

def recusar_projeto(codProjeto):
    with Db() as db:
        usuarioDao = usuario_dao.UsuarioDAO(db)

        query = '''
            update projetos set status = 2 where codProjeto = (%s)
        '''
        db.gravar_autocommit(query, (codProjeto,))
        
        user = usuario_orientado_dao.get_usuario_codProjeto(codProjeto)
        if user:    
            if user['tipoUsuario'] == TiposUsuario.Aluno.value:
                usuarioDao.desativar_aluno(user['codUsuario'])
            else:
                usuarioDao.desativa_usuario(user['codUsuario'])

def edita_titulo(codProjeto, titulo):
    with Db() as db:
        query = 'update projetos set tituloProjeto = (%s) where codProjeto = (%s)'

        db.gravar_autocommit(query, (titulo, codProjeto))

def edita_descricao(codProjeto, descricao):
    with Db() as db:
        query = 'update projetos set descricao = (%s) where codProjeto = (%s)'

        db.gravar_autocommit(query, (descricao, codProjeto))

def edita_subtitulo(codProjeto, subtitulo):
    with Db() as db:
        query = 'update projetos set subtitulo = (%s) where codProjeto = (%s)'

        db.gravar_autocommit(query, (subtitulo, codProjeto))

def edita_publicacao(codProjeto, localPublicacao):
    with Db() as db:
        query = 'update projetos set localPublicacao = (%s) where codProjeto = (%s)'

        db.gravar_autocommit(query, (localPublicacao, codProjeto))

def is_ativo_filename(filename):
    with Db() as db:
        query = 'select codProjeto from projetos where nomeArquivo = (%s) and ativo = 1 and not status = 2 '

        ret = db.busca_um(query, (filename,))

        if ret:
            return ret['codProjeto']
        return None

def is_valid_project(codAutor):
    with Db() as db:
        query = '''
            select * from projeto_autor 
            natural join projetos 
            where codAutor = (%s) and (status = 0)
        '''
        res = db.busca_um(query, (codAutor,))

        if res:
            return False
        return True

def is_orientador_projeto_novo(codProjeto, codOrientador):
    with Db() as db:
        query = '''
            select distinct p.codProjeto 
            from orientadores as o 
            natural join projeto_orientador as po 
            join projetos as p 
            on p.codProjeto = po.codProjeto 
            where p.codProjeto = (%s) and o.codOrientador = (%s) and p.status = 0
        '''
        if db.busca_um(query, (codProjeto, codOrientador)):
            return True
        return False

def download_file(codProjeto):
    with Db() as db:
        query = 'UPDATE projetos SET numDownloads = numDownloads + 1 WHERE codProjeto = (%s)'

        db.gravar_autocommit(query, (codProjeto,))

def add_view(codProjeto):
    with Db() as db:
        query = 'UPDATE projetos SET numVisitas = numVisitas + 1 WHERE codProjeto = (%s)'

        db.gravar_autocommit(query, (codProjeto,))

def prenche_projetos(ret, attrs=None):
    for item in ret:
        prenche_projeto(item, attrs=attrs)

def prenche_projeto(ret, attrs=None):
    if attrs == None:
        ret['autores'] = autores_dao.busca_autores_proj(ret['codProjeto'])
        ret['palavrasChave'] = palavras_chave_dao.busca_palavras_chave(ret['codProjeto'])
        ret['curso'] = cursos_dao.get_all_curso_cod(ret['codCurso'])
        ret['orientadores'] = orientadores_dao.busca_orientadores_codProjeto(ret['codProjeto'])
    else:
        if AtributosEspeciaisProjeto.Autores.value in attrs:
            ret['autores'] = autores_dao.busca_autores_proj(ret['codProjeto'])

        if AtributosEspeciaisProjeto.PalavrasChave.value in attrs:
            ret['palavrasChave'] = palavras_chave_dao.busca_palavras_chave(ret['codProjeto'])

        if AtributosEspeciaisProjeto.Curso.value in attrs:
            ret['curso'] = cursos_dao.get_all_curso_cod(ret['codCurso'])

        if AtributosEspeciaisProjeto.Orientadores.value in attrs:
            ret['orientadores'] = orientadores_dao.busca_orientadores_codProjeto(ret['codProjeto'])

def reprova_projetos_invalidos():
    with Db() as db:
        query = '''
            select p.codProjeto, p.nomeArquivo
            from usuario_orientado as uo
            natural join projetos as p
            where status = 0 and dataValidade <= current_timestamp()
        '''
        ret = db.busca(query, None)

        for proj in ret:
            recusar_projeto(proj['codProjeto'])
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], proj['nomeArquivo']))
            except FileNotFoundError:
                pass

def busca_atributos_projeto(separate_camel_case=False):
    db = Db(database='information_schema')
    
    query = '''
        select c.ordinal_position as idx, c.column_name as coluna
        from information_schema.tables t
        inner join information_schema.COLUMNS c
            on c.table_schema=t.table_schema
            and c.table_name=t.table_name
        where (t.table_schema='{0}' and t.table_name='projetos') 
        and (not (c.ordinal_position in (1,10,11,12)))
        order by t.table_name, c.ordinal_position
    '''.format(getenv('MYSQL_DATABASE'))
    ret = db.busca(query)
    obj = {}
    for attr in ret:
        if separate_camel_case:
            obj[attr['idx']] = scc(attr['coluna'])
        else:
            obj[attr['idx']] = attr['coluna']
    return obj

def __grava_proj_ori(codProjeto, codOrientador, tipo):
    with Db() as db:
        query = 'insert into projeto_orientador values(%s, %s, %s)'

        db.gravar_autocommit(query, (codOrientador, codProjeto, tipo))

def __get_limit(pag, tam = 20):
    fi = 1 + ((pag - 1) * tam)
    ff = pag * tam

    return ' LIMIT {}, {}'.format(fi, ff)

def __busca_projeto_full(query, *args):
    with Db() as db:
        ret = db.busca(query, *args)

        prenche_projetos(ret)
        
        return ret
