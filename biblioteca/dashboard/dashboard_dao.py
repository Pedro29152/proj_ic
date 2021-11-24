from biblioteca.projeto import projetos_dao
from biblioteca.extensions import ModalidadeProjeto, get_enum_obj

class DashboardDAO:
    def __init__(self, db, projetosDaoArg=None):
        self.db = db
        self.projetosDao = projetosDaoArg if projetosDaoArg else projetos_dao.ProjetosDAO(self.db)

    def get_count_projetos_semestre(self, ano, semestre):
        if not self.__valid_int(ano):
            return None
        if not self.__valid_int(semestre):
            return None
        
        semestre = int(semestre)
        ano = int(ano)
        
        self.projetosDao.reprova_projetos_invalidos()

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
        res = self.db.busca_um(query, (ano,))
        
        count = res['count']
        if not count:
            return 0 
        return int(count)

    def get_count_projetos_semestres(self, anoI, anoF):
        if not self.__valid_int(anoI):
            return None
        if not self.__valid_int(anoF):
            return None
        
        anoI = int(anoI)
        anoF = int(anoF)
        
        if anoI > anoF:
            return None

        self.projetosDao.reprova_projetos_invalidos()

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
        ret = self.db.busca(query, (anoI, anoF))
        if not ret:
            return None
        
        self.__remove_decimais(ret)

        return ret

    def get_count_projetos_curso(self, anoI, anoF):
        self.projetosDao.reprova_projetos_invalidos()

        query = '''
            SELECT
                codCurso,
                descricaoCurso,
                abreviacao,
                year(dataAvaliacao) as ano,
                sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
                sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
            FROM projetos natural join cursos
            where (ativo = 1 and status = 1) and year(dataAvaliacao) between %s and %s
            group by year(dataAvaliacao), codCurso
            order by descricaoCurso, year(dataAvaliacao)
        '''
        ret = self.db.busca(query, (anoI, anoF))
        if not ret:
            return ret

        self.__remove_decimais(ret)
        
        cursos = self.__gerar_obj_proj(ret, 'abreviacao', order_ano=True)

        return cursos

    def get_count_projetos_orientador(self, anoI, anoF, orientadores= tuple()):
        self.projetosDao.reprova_projetos_invalidos()

        baseQuery = '''
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
            where 
                (p.ativo = 1 and p.status = 1) and
                (year(dataAvaliacao) between %s and %s)
                {0}
            group by year(dataAvaliacao), codOrientador
            order by nomeOrientador	, year(dataAvaliacao)
        '''

        if orientadores:
            query = baseQuery.format('and (o.raOrientador in (%s))' % ','.join(['%s'] * len(orientadores)))
            ret = self.db.busca(query, (anoI, anoF) + orientadores)
        else:
            query = baseQuery.format('')
            ret = self.db.busca(query, (anoI, anoF))

        if not ret:
            return ret

        self.__remove_decimais(ret)
        
        orientadores = self.__gerar_obj_proj(ret, 'nomeOrientador', order_ano=True)
        ret = None

        return orientadores

    def get_count_projetos_formandos_curso(self, anoI, anoF):
        self.projetosDao.reprova_projetos_invalidos()

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
            where (p.ativo = 1 and p.status = 1) and year(dataAvaliacao) between %s and %s
            group by p.codCurso,  year(dataAvaliacao)
            order by p.codCurso, year(dataAvaliacao)
        '''
        ret = self.db.busca(query, (anoI, anoF))
        if not ret:
            return ret

        self.__remove_decimais(ret)
        
        cursos = self.__gerar_obj_proj(ret, 'abreviacao', order_ano=True)
        ret = None

        return cursos

    def get_count_projetos_status(self, anoI, anoF):
        self.projetosDao.reprova_projetos_invalidos()
        
        query = '''
            select
                (case when status = 0 then 'processando' when status = 1 then 'aceito' when status = 2 then 'rejeitado' else 'erro' end) as status,
                year(dataAvaliacao) as ano,
                sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
                sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
            FROM projetos as p
            where (p.ativo = 1) and year(dataAvaliacao) between %s and %s
            group by 1, year(dataAvaliacao)
            order by status, year(dataAvaliacao);
        '''
        ret = self.db.busca(query, (anoI, anoF))
        if not ret:
            return ret

        self.__remove_decimais(ret)
        
        status = self.__gerar_obj_proj(ret, 'status', order_ano=True)
        ret = None

        return status

    def get_count_projetos_modalidade(self, anoI, anoF):
        self.projetosDao.reprova_projetos_invalidos()

        modalidades = get_enum_obj(ModalidadeProjeto)
        query = '''
            select 
                year(dataAvaliacao) as ano,
                (case {0} else 'erro' end) as modalidade,
                sum(case when month(dataAvaliacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
                sum(case when month(dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
            from projetos
            where (ativo = 1 and status = 1) and year(dataAvaliacao) between %s and %s
            group by year(dataAvaliacao), modalidade
            order by 1
        '''.format(' '.join(["when modalidade = {0} then '{1}'".format(mod, modalidades[mod]) for mod in modalidades]))
        ret = self.db.busca(query, (anoI, anoF))
        if not ret:
            return ret
        
        self.__remove_decimais(ret)
        
        modalidade = self.__gerar_obj_proj(ret, 'modalidade', order_ano=True)
        ret = None

        return modalidade

    def get_count_solicitacoes_revisao(self, anoI, anoF):
        query = '''
            select
                year(dataSolicitacao) as ano,
                sum(case when month(dataSolicitacao) between 1 and 7 then 1 else 0 end)  AS 'semestre1',
                sum(case when month(dataSolicitacao) between 8 and 12 then 1 else 0 end) AS 'semestre2'
            FROM solicitacoes_revisao as sr
            where year(dataSolicitacao) between %s and %s
            group by 1
            order by 1
        '''
        ret = self.db.busca(query, (anoI, anoF))
        if not ret:
            return ret

        self.__remove_decimais(ret)
        
        solic = {}
        for item in ret:
            solic[item['ano']] = [item['semestre1'], item['semestre2']]

        return solic

    def get_count_usuarios_tipo(self, ):
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
        ret = self.db.busca(query, None)
        if not ret:
            return ret

        tipos = {}
        for item in ret:
            tipos[item['tipo']] = item['usuarios']
        
        return tipos

    def get_anos(self, ):
        query = '''
            select
                min(year(dataAvaliacao)) as min, 
                max(year(dataAvaliacao)) as max
            from projetos as p
            where (p.ativo = 1 and p.status = 1)
        '''
        ret = self.db.busca_um(query, None)
        if not ret or (not ret['min'] or not ret['max']):
            return []
        return list(range(ret['min'], ret['max'] + 1))


    def __valid_int(self, val):
        try:
            t = int(val)
        except ValueError:
            return False
        return True

    def __remove_decimais(self, obj):
        for item in obj:
            item['semestre1'] = int(item['semestre1'])
            item['semestre2'] = int(item['semestre2'])    

    def __gerar_obj_proj(self, obj, attr, order_ano=False, ano_attr='ano'):
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
