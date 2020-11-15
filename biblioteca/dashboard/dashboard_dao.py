from biblioteca import db

def get_count_projetos_semestre(ano, semestre):
    if not valid_int(ano):
        return None
    if not valid_int(semestre):
        return None
    
    semestre = int(semestre)
    ano = int(ano)

    dataQuery = ''
    if semestre == 1:
        dataQuery = "sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end) AS 'count'"
    elif semestre == 2:
        dataQuery = "sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'count'"
    else:
        return None
    
    query = '''
        SELECT
            {0}
        FROM projetos
        where year(dataAvaliacao) = (%s) and (ativo = 1 and status = 1)
    '''.format(dataQuery)
    res = db.bd_busca_um(query, (ano,))
    
    count = res['count']
    if not count:
        return 0 
    return int(count)

def get_count_projetos_semestres(anoI, anoF):
    if not valid_int(anoI):
        return None
    if not valid_int(anoF):
        return None
    
    anoI = int(anoI)
    anoF = int(anoF)
    
    if anoI > anoF:
        return None

    query = '''
        SELECT
            year(dataAvaliacao) as 'ano',
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end) AS 'semestre1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        FROM projetos
        where year(dataAvaliacao) between (%s) and (%s) and (ativo = 1 and status = 1)
        group by year(dataAvaliacao)
        order by 1
    '''
    ret = db.bd_busca(query, (anoI, anoF))
    if not ret:
        return None
    
    __remove_decimais(ret)

    return ret

def get_count_projetos_curso():
    query = '''
        SELECT
            codCurso,
            descricaoCurso,
            abreviacao,
            year(dataAvaliacao) as ano,
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        FROM projetos natural join cursos
        where (ativo = 1 and status = 1)
        group by year(dataAvaliacao), codCurso
        order by descricaoCurso, year(dataAvaliacao)
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret

    __remove_decimais(ret)
    
    cursos = __gerar_obj_proj(ret, 'abreviacao', order_ano=True)
    ret = None

    return cursos

def get_count_projetos_orientador():
    query = '''
        SELECT
            o.codOrientador,
            o.raOrientador,
            o.nomeOrientador,
            year(dataAvaliacao) as ano,
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        FROM projetos as p 
        join projeto_orientador as po on po.codProjeto = p.codProjeto
        join orientadores as o on o.codOrientador = po.codOrientador
        where (p.ativo = 1 and p.status = 1)
        group by year(dataAvaliacao), codOrientador
        order by nomeOrientador	, year(dataAvaliacao)
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret

    __remove_decimais(ret)
    
    orientadores = __gerar_obj_proj(ret, 'nomeOrientador', order_ano=True)
    ret = None

    return orientadores

def get_count_projetos_formandos_curso():
    query =  '''
        SELECT
            p.codCurso,
            abreviacao,
            year(dataAvaliacao) as ano,
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        FROM projeto_autor as pa 
        natural join projetos as p
        join cursos as c on c.codCurso = p.codCurso
        group by p.codCurso,  year(dataAvaliacao)
        order by p.codCurso, year(dataAvaliacao)
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret

    __remove_decimais(ret)
    
    cursos = __gerar_obj_proj(ret, 'abreviacao', order_ano=True)
    ret = None

    return cursos

def get_count_projetos_status():
    query = '''
        select
            (case when status = 0 then 'processando' when status = 1 then 'aceito' when status = 2 then 'rejeitado' else 'erro' end) as status,
            year(dataAvaliacao) as ano,
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        FROM projetos as p
        where (p.ativo = 1)
        group by 1, year(dataAvaliacao)
        order by status, year(dataAvaliacao);
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret

    __remove_decimais(ret)
    
    status = __gerar_obj_proj(ret, 'status', order_ano=True)
    ret = None

    return status

def get_count_projetos_modalidade():
    query = '''
        select 
            year(dataAvaliacao) as ano,
            (case 
                when modalidade = 0 then 'Artigo Cientifico'
                when modalidade = 1 then 'Relatorio Tecnico'
                when modalidade = 2 then 'Monografia'
                when modalidade = 3 then 'Relatorio Tecnico Atividades Porfolio'
                when modalidade = 4 then 'Resumo'
                when modalidade = 5 then 'GDD'
                else 'erro'
            end) as modalidade,
            sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
            sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        from projetos
        where (ativo = 1 and status = 1)
        group by year(dataAvaliacao), modalidade
        order by 1
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret
    
    __remove_decimais(ret)
    
    modalidade = __gerar_obj_proj(ret, 'modalidade', order_ano=True)
    ret = None

    return modalidade

def get_count_solicitacoes_revisao():
    query = '''
        select
            year(dataSolicitacao) as ano,
            sum(case when month(dataSolicitacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
            sum(case when month(dataSolicitacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
        FROM solicitacoes_revisao as sr
        group by 1
        order by 1
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret

    __remove_decimais(ret)
    
    solic = {}
    for item in ret:
        solic[item['ano']] = [item['semestre1'], item['semestre2']]

    return solic

def get_count_usuarios_tipo():
    query = '''
        select
            (case
                when tipoUsuario = 1 then 'aluno'
                when tipoUsuario = 2 then 'orientador'
                when tipoUsuario = 3 then 'secretaria'
                when tipoUsuario = 4 then 'administrador'
                when tipoUsuario = 5 then 'coordenador'
                else 'erro'
            end) as tipo,
            count(*) as usuarios
        from usuarios
        where ativo = 1
        group by tipoUsuario
        order by 1
    '''
    ret = db.bd_busca(query, None)
    if not ret:
        return ret

    tipos = {}
    for item in ret:
        tipos[item['tipo']] = item['usuarios']
    
    return tipos

def get_anos():
    query = '''
        select
            min(year(dataAvaliacao)) as min, 
            max(year(dataAvaliacao)) as max
        from projetos as p
        where (p.ativo = 1 and p.status = 1)
    '''
    ret = db.bd_busca_um(query, None)
    if not ret or (not ret['min'] or not ret['max']):
        return []
    return list(range(ret['min'], ret['max'] + 1))

def valid_int(val):
    try:
        t = int(val)
    except ValueError:
        return False
    return True

def __remove_decimais(obj):
    for item in obj:
        item['semestre1'] = int(item['semestre1'])
        item['semestre2'] = int(item['semestre2'])    

def __gerar_obj_proj(obj, attr, order_ano=False, ano_attr='ano'):
    ret = {}
    for item in obj:
        try:
            ret[item[attr]].append(item)
        except KeyError:
            ret[item[attr]] = [item]

    if order_ano:
        for chave in ret.keys():
            att = ret[chave]
            ret[chave] = {}
            for a in att:
                dataset = []
                dataset.append(a['semestre1'])
                dataset.append(a['semestre2'])
                ano = a['ano']
                ret[chave][ano] = dataset

    return ret
