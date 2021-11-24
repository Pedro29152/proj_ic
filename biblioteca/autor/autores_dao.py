from mysql.connector.errors import IntegrityError, ProgrammingError, DataError
from biblioteca import response_messages

class AutoresDAO:
    def __init__(self, db):
        self.db = db

    def busca_autores(self, nomeAutor=''):
        if not nomeAutor:
            nomeAutor = ''
        nomeAutor = '%{}%'.format(nomeAutor)
        query = '''
            SELECT *
            FROM autores
            WHERE nomeAutor like (%s)
            '''
        ret = self.db.busca(
            query,
            (nomeAutor,)
        )
        return ret

    def get_autor(self, codAluno):
        query = 'select * from autores where codAutor = (%s)'
        ret = self.db.busca_um(query, (codAluno,))
        return ret

    def busca_autores_proj(self, codProjeto):
        query = '''
            SELECT autores.nomeAutor, autores.raAutor, autores.email
            FROM autores 
            NATURAL JOIN projeto_autor pa 
            WHERE pa.codProjeto = (%s)
        '''
        ret = self.db.busca(query, (codProjeto,))
        return ret

    def get_autor_ra(self, ra):
        query = 'select * from autores where raAutor = (%s)'
        ret = self.db.busca_um(query, (ra,))
        return ret

    def get_autor_codUsuario(self, codUsuario):
        query = '''
            select distinct a.*
            from autores as a 
            join usuario_orientado as uo 
            on uo.codAutor = a.codAutor 
            join usuarios as u 
            on u.codUsuario = uo.codUsuario 
            where u.codUsuario = (%s) and u.ativo = 1
        '''
        return self.db.busca_um(query, (codUsuario,))

    def get_orientador_codAutor(self, codAutor):
        query = '''
            select o.* from usuario_orientado as uo
            join orientadores as o 
            on uo.codOrientador = o.codOrientador 
            where uo.codAutor = (%s)
        '''
        return self.db.busca_um(query, (codAutor,))

    def get_relatorio_autores(self, data_i=None, data_f=None):
        base_query = '''
            select 
                a.nomeAutor as nomeDoAutor,
                a.raAutor as raDoAutor,
                a.email as emailDoAutor,
                p.tituloProjeto as projeto, 
                p.dataAvaliacao as dataDeAvaliacaoDoProjeto,
                year(p.dataAvaliacao) as ano, 
                c.abreviacao as curso,
                o.nomeOrientador as orientador
            from autores as a
            join projeto_autor as pa
            on a.codAutor = pa.codAutor
            join projetos as p
            on pa.codProjeto = p.codProjeto
            join cursos as c
            on c.codCurso = p.codCurso
            join projeto_orientador as po
            on po.codProjeto = p.codProjeto
            join orientadores as o
            on o.codOrientador = po.codOrientador
            where (p.ativo = 1 and p.status = 1) and (po.tipoOrientador = 0) {0}
            order by p.dataAvaliacao, p.tituloProjeto, a.nomeAutor, a.raAutor, c.descricaoCurso
        '''

        if data_i and data_f:
            query = base_query.format(
                'and (p.dataAvaliacao between %s and %s)')
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

        return ret

    def cadastra_autor(self, nome, email, ra):
        query = 'insert into autores(nomeAutor, email, raAutor) values (%s, %s, %s)'
        try:
            self.db.gravar(query, (nome, email.lower(), ra))
            return self.get_autor_ra(ra)
        except IntegrityError:
            raise IntegrityError(response_messages.ERRO_INTEGRIDADE('"raAutor" ou "email"'))
        except DataError:
            raise DataError(response_messages.VALIDACAO_DEVE('ra', 'ter no maximo 13 caracteres'))

    def is_aluno_valido(self, codUsuario):
        query = '''
            select distinct u.codUsuario
            from usuarios as u 
            join usuario_orientado as uo 
            on u.codUsuario = uo.codUsuario 
            join autores as a 
            on a.codAutor = uo.codAutor 
            where uo.dataValidade > now() and u.codUsuario = (%s) 
        '''
        ret = self.db.busca_um(query, (codUsuario,))
        return ret
