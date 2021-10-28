from biblioteca.projeto import projetos_dao
from biblioteca.usuarios import usuario_dao
from .schemas import Orientadores

from mysql.connector.errors import ProgrammingError

class OrientadoresDAO:
    def __init__(self, db, projetosDaoArg=None, usuariosDaoArg=None):
        self.db = db
        self.usuarioDao = usuariosDaoArg if usuariosDaoArg else usuario_dao.UsuarioDAO(db, self)
        self.projetosDao = projetosDaoArg if projetosDaoArg else projetos_dao.ProjetosDAO(db, usuarioDaoArg=self.usuarioDao, orientadoresDaoArg=self)

    def get_orientador(self, raOrientador):
        query = 'select * from orientadores where raOrientador = (%s) and ativo = 1'
        ret = self.db.busca_um(query, (raOrientador,))

        if ret:
            ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'], ret['email'], ret['currLattes'], db=self.db)
            return ori
        return None

    def get_orientador_codigo(self, codOrientador, is_instance=True):
        query = 'select * from orientadores where codOrientador = (%s) and ativo = 1'
        ret = self.db.busca_um(query, (codOrientador,))

        if ret:
            if is_instance:
                ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'], ret['email'], ret['currLattes'], db=self.db)
                return ori
            return ret
        return None

    def get_orientador_orientando_codUsuario(self, codUsuario, is_instance=True):
        query = '''
            select distinct o.codOrientador, nomeOrientador, raOrientador, currLattes, o.email 
            from orientadores as o 
            join usuario_orientado as uo 
            on o.codOrientador = uo.codOrientador 
            join usuarios as u 
            on uo.codUsuario = u.codUsuario 
            where u.codUsuario = (%s) and o.ativo = 1 and (uo.dataValidade > current_date())
        '''
        ret = self.db.busca_um(query, (codUsuario,))
        if ret:
            if is_instance:
                ori = Orientadores(ret['codOrientador'], ret['nomeOrientador'], ret['raOrientador'], ret['email'], ret['currLattes'], db=self.db)
                return ori
            return ret
        return None

    def get_orientador_codUsuario(self, codUsuario):
        query = '''
            select o.codOrientador, o.nomeOrientador, o.raOrientador, o.currLattes, o.email 
            from orientadores as o 
            join usuarios as u 
            on u.codUsuario = o.codUsuario 
            where u.codUsuario = (%s)
        '''
        return self.db.busca_um(query, (codUsuario,))

    def get_orientador_codProjeto(self, codProjeto):
        query = '''
            select o.* from orientadores as o
            join usuario_orientado as uo on uo.codOrientador = o.codOrientador
            where uo.codProjeto = (%s)
        '''
        ret = self.db.busca_um(query, (codProjeto,))
        return ret

    def busca_orientadores_codProjeto(self, codProjeto):
        val = self.db.busca(
            '''
                select codOrientador, nomeOrientador, raOrientador, email, currLattes, tipoOrientador 
                from orientadores 
                natural join projeto_orientador as po
                where codProjeto = (%s)
                order by po.tipoOrientador
            ''',
            (codProjeto,)
        )

        return val

    def busca_todos_orientadores(self):
        val = self.db.busca(
            'select * from orientadores',
            None
        )

        return val

    def busca_orientadores(self):  
        val = self.db.busca(
            'select * from orientadores where ativo = 1',
            None
        )

        return val

    def busca_todos_orientadores_nome(self, nome):
        nome = '%{}%'.format(nome)
            
        val = self.db.busca(
            'select * from orientadores where nomeOrientador like (%s)',
            (nome,)
        )

        return val

    def busca_orientadores_nome(self, nome):
        nome = '%{}%'.format(nome)
            
        val = self.db.busca(
            'select * from orientadores where nomeOrientador like (%s) and ativo = 1',
            (nome,)
        )

        return val

    def buscar_revisoes(self):
        query = '''
            select * from solicitacoes_revisao
        '''
        ret = self.db.busca(query, None)

        for revisao in ret:
            revisao['projeto'] = self.projetosDao.get_projeto_codUsuarioOrientado(revisao['codUsuarioOrientado'])
        return ret

    def get_revisao(self, codSolicitacao):
        query = '''
            select * from solicitacoes_revisao 
            where codSolicitacao = (%s)
        '''
        ret = self.db.busca_um(query, (codSolicitacao,))
        if ret:
            ret['projeto'] = self.projetosDao.get_projeto_codUsuarioOrientado(ret['codUsuarioOrientado'])

        return ret

    def get_revisao_codUsuario_autor(self, codSolicitacao, codUsuario):
        query = '''
            select sr.* from solicitacoes_revisao as sr
            join usuario_orientado as uo
            on sr.codUsuarioOrientado = uo.codUsuarioOrientado
            join usuarios as u 
            on u.codUsuario = uo.codUsuario
            where uo.codUsuario = (%s) and ativo = 1 and codSolicitacao = (%s)
        '''
        ret = self.db.busca_um(query, (codUsuario, codSolicitacao))
        return ret

    def ativa_orientador(self, codOrientador):
        query = 'update orientadores set ativo = 1 where codOrientador = (%s)'

        self.db.gravar(query, (codOrientador,))

    def desativa_orientador(self, codOrientador):
        ori = self.get_orientador_codigo(codOrientador, False)
        if ori['codUsuario']:
            self.usuarioDao.deleta_usuario(ori['codUsuario'])

        query = 'update orientadores set ativo = 0, codUsuario = null where codOrientador = (%s)'
        self.db.gravar(query, (codOrientador,))
        self.usuarioDao.remove_responsabilidade_orientador(codOrientador)

    def deleta_orientador(self, codOrientador):
        query = '''
            delete from orientadores where codOrientador = (%s)
        '''
        self.db.gravar(query, (codOrientador,))

    def exists(self, codOrientador):
        query = 'select codOrientador from orientadores where codOrientador = (%s)'
        ret = self.db.busca_um(query, (codOrientador,))

        if ret:
            return True
        return False

    def get_count(self):
        query = 'select count(*) as orientadores from orientadores'
        ret = self.db.busca_um(query, None)
        return ret['orientadores']

    def get_relatorio_orientadores(self, data_i= None, data_f= None):
        base_query = '''
            select 
                o.nomeOrientador as nomeDoOrientador, 
                count(*) as quantidadeDeProjetos, 
                year(p.dataAvaliacao) as ano,
                sum(case when month(p.dataAvaliacao) between 1 and 7 then 1 else 0 end) AS 'semestre 1',
                sum(case when month(p.dataAvaliacao) between 8 and 12 then 1 else 0 end) AS 'semestre 2'
            from orientadores as o
            join projeto_orientador as po
            on po.codOrientador = o.codOrientador
            join projetos as p on p.codProjeto = po.codProjeto
            where (p.ativo = 1 and p.status = 1) {0}
            group by o.codOrientador, 3
            order by 1, 3
        '''
        
        if data_i and data_f:
            query = base_query.format('and dataAvaliacao between %s and %s')
            try:
                ret = self.db.busca(query, (data_i, data_f))
            except ProgrammingError:
                return None
        else:
            query = base_query.format('')
            try:
                ret = self.db.busca(query)
            except ProgrammingError:
                return None
        
        self.__remove_decimais(ret)

        return ret

    def __remove_decimais(self, obj):
        for item in obj:
            item['semestre 1'] = int(item['semestre 1'])
            item['semestre 2'] = int(item['semestre 2'])
