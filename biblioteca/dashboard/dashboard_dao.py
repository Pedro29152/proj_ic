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
        where year(dataAvaliacao) = (%s)
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
        where year(dataAvaliacao) between (%s) and (%s)
        group by year(dataAvaliacao)
        order by 1
    '''
    ret = db.bd_busca(query, (anoI, anoF))
    if not ret:
        return None
    
    for item in ret:
        item['semestre1'] = int(item['semestre1'])
        item['semestre2'] = int(item['semestre2'])

    return ret

def valid_int(val):
    try:
        t = int(val)
    except ValueError:
        return False
    return True
