from biblioteca import db
from .schemas import Orientadores
from biblioteca.projeto import projetos_dao
from biblioteca.usuarios import usuario_dao

def get_orientador(raOrientador):
    query = 'select * from orientadores where raOrientador = (%s) and ativo = 1'
    ret = db.bd_busca_um(query, (raOrientador,))

    if ret:
        ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'], ret['email'], ret['currLattes'])
        return ori
    return None

def get_orientador_codigo(codOrientador, is_instance=True):
    query = 'select * from orientadores where codOrientador = (%s) and ativo = 1'
    ret = db.bd_busca_um(query, (codOrientador,))

    if ret:
        if is_instance:
            ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'], ret['email'], ret['currLattes'])
            return ori
        return ret
    return None

def get_orientador_orientando_codUsuario(codUsuario, is_instance=True):
    query = '''
        select distinct o.codOrientador, nomeOrientador, raOrientador, currLattes, o.email 
        from orientadores as o 
        join usuario_orientado as uo 
        on o.codOrientador = uo.codOrientador 
        join usuarios as u 
        on uo.codUsuario = u.codUsuario 
        where u.codUsuario = (%s) and o.ativo = 1 and (uo.dataValidade > current_date())
    '''
    ret = db.bd_busca_um(query, (codUsuario,))
    if ret:
        if is_instance:
            ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'], ret['email'], ret['currLattes'])
            return ori
        return ret
    return None

def get_orientador_codUsuario(codUsuario):
    query = '''
        select o.codOrientador, o.nomeOrientador, o.raOrientador, o.currLattes, o.email 
        from orientadores as o 
        join usuarios as u 
        on u.codUsuario = o.codUsuario 
        where u.codUsuario = (%s)
    '''
    return db.bd_busca_um(query, (codUsuario,))

def get_orientador_codProjeto(codProjeto):
    query = '''
        select o.* from orientadores as o
        join usuario_orientado as uo on uo.codOrientador = o.codOrientador
        where uo.codProjeto = (%s)
    '''
    ret = db.bd_busca_um(query, (codProjeto,))
    return ret

def busca_orientadores_codProjeto(codProjeto):
    val = db.bd_busca(
        '''
            select codOrientador, nomeOrientador, raOrientador, email, currLattes, tipoOrientador 
            from orientadores 
            natural join projeto_orientador 
            where codProjeto = (%s)
        ''',
        (codProjeto,)
    )

    return val

def busca_todos_orientadores():
    val = db.bd_busca(
        'select * from orientadores',
        None
    )

    return val

def busca_orientadores():    
    val = db.bd_busca(
        'select * from orientadores where ativo = 1',
        None
    )

    return val

def busca_todos_orientadores_nome(nome):
    nome = '%{}%'.format(nome)
    
    val = db.bd_busca(
        'select * from orientadores where nomeOrientador like (%s)',
        (nome,)
    )

    return val

def busca_orientadores_nome(nome):
    nome = '%{}%'.format(nome)
    
    val = db.bd_busca(
        'select * from orientadores where nomeOrientador like (%s) and ativo = 1',
        (nome,)
    )

    return val

def buscar_revisoes():
    query = '''
        select * from solicitacoes_revisao
    '''
    ret = db.bd_busca(query, None)

    for revisao in ret:
        revisao['projeto'] = projetos_dao.get_projeto_codUsuarioOrientado(revisao['codUsuarioOrientado'])
    return ret

def get_revisao(codSolicitacao):
    query = '''
        select * from solicitacoes_revisao 
        where codSolicitacao = (%s)
    '''
    ret = db.bd_busca_um(query, (codSolicitacao,))
    if ret:
        ret['projeto'] = projetos_dao.get_projeto_codUsuarioOrientado(ret['codUsuarioOrientado'])

    return ret

def get_revisao_codUsuario_autor(codSolicitacao, codUsuario):
    query = '''
        select sr.* from solicitacoes_revisao as sr
        join usuario_orientado as uo
        on sr.codUsuarioOrientado = uo.codUsuarioOrientado
        join usuarios as u 
        on u.codUsuario = uo.codUsuario
        where uo.codUsuario = (%s) and ativo = 1 and codSolicitacao = (%s)
    '''
    ret = db.bd_busca_um(query, (codUsuario, codSolicitacao))
    return ret

def ativa_orientador(codOrientador):
    query = 'update orientadores set ativo = 1 where codOrientador = (%s)'

    db.bd_gravar(query, (codOrientador,))

def desativa_orientador(codOrientador):
    ori = get_orientador_codigo(codOrientador, False)
    if ori['codUsuario']:
        query = '''
            update usuarios set ativo = 0 where codUsuario = (%s)
        '''
        db.bd_gravar(query, (ori['codUsuario'],))

    query = 'update orientadores set ativo = 0, codUsuario = null where codOrientador = (%s)'

    db.bd_gravar(query, (codOrientador,))
    usuario_dao.remove_responsabilidade_orientador(codOrientador)

def deleta_orientador(codOrientador):
    query = '''
        delete from orientadores where codOrientador = (%s)
    '''
    db.bd_gravar(query, (codOrientador,))

def exists(codOrientador):
    query = 'select codOrientador from orientadores where codOrientador = (%s)'
    ret = db.bd_busca_um(query, (codOrientador,))

    if ret:
        return True
    return False

def get_count():
    query = 'select count(*) as orientadores from orientadores'
    ret = db.bd_busca_um(query, None)
    return ret['orientadores']