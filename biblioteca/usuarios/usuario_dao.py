from mysql.connector.errors import DatabaseError
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector.errors import IntegrityError
from datetime import datetime, timedelta
from biblioteca.orientador import orientadores_dao
from biblioteca import extensions, response_messages

class UsuarioDAO:
    def __init__(self, db, orientadoresDaoArg=None):
        self.db = db
        self.orientadoresDao = orientadoresDaoArg if orientadoresDaoArg else orientadores_dao.OrientadoresDAO(self.db, usuariosDaoArg=self)

    def verifica_usr(self, usuario, senha):
        senhaR = self.busca_senha_nome(usuario)
        
        if(senhaR):
            if(check_password_hash(senhaR, senha)):
                return self.busca_usuarios_nome(usuario)

        return None

    def busca_usuarios(self):
        val = self.db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where ativo = 1',
            None
        )
        if(not val):
            val = []

        return val

    def busca_usuarios_nome_like(self, nomeUsuario):
        nomeUsuario = '%{}%'.format(nomeUsuario)
        val = self.db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario like (%s) and ativo = 1',
            (nomeUsuario,)
        )
        if(not val):
            val = []

        return val

    def busca_usuarios_inativos(self):
        val = self.db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where ativo = 0',
            None
        )
        if(not val):
            val = []

        return val

    def busca_usuarios_inativos_nome_like(self, nomeUsuario):
        nomeUsuario = '%{}%'.format(nomeUsuario)
        val = self.db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario like (%s) and ativo = 0',
            (nomeUsuario,)
        )
        if(not val):
            val = []

        return val

    def busca_usuarios_codAutor_not_codUsuario(self, codAutor, codUsuario):
        query = '''
            select u.codUsuario, nomeUsuario, tipoUsuario, u.nome, u.email 
            from usuarios as u 
            join usuario_orientado as uo 
            on uo.codUsuario = u.codUsuario 
            join autores as a 
            on a.codAutor = uo.codAutor 
            where ativo = 1 and a.codAutor = (%s) and not u.codUsuario = (%s)
        '''
        return self.db.busca(query, (codAutor, codUsuario))

    def busca_usuarios_nome(self, nomeUsuario):
        val = self.db.busca_um(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario = (%s) and ativo = 1',
            (nomeUsuario,)
        )

        return val

    def busca_usuarios_orientados_nome_like(self, nomeUsuario, codOrientador):
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email 
            from usuarios as u 
            natural join usuario_orientado as uo 
            where uo.codOrientador = (%s) and nomeUsuario like (%s) and ativo = 1
        '''
        ret = self.db.busca(query,(codOrientador, nomeUsuario))
        return ret

    def busca_usuarios_orientados(self, codOrientador):
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email 
            from usuarios as u 
            natural join usuario_orientado as uo 
            where uo.codOrientador = (%s) and ativo = 1
        '''
        ret = self.db.busca(query,(codOrientador,))
        return ret

    def busca_senha_nome(self, nomeUsuario):
        val = self.db.busca_um(
            'select senha from usuarios where nomeUsuario = (%s) and ativo = 1',
            (nomeUsuario,)
        )
        if val:
            return val['senha']
        return None

    def buscar_usuarios_secretaria(self, nomeUsuario=None):
        if nomeUsuario == None:
            nomeUsuario = ''
        nomeUsuario = '%{}%'.format(nomeUsuario) 
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email, ativo from usuarios 
            where nomeUsuario like (%s) and tipoUsuario = {}
        '''.format(extensions.TiposUsuario.Secretaria.value)
        ret = self.db.busca(query, (nomeUsuario,))
        return ret

    def buscar_usuarios_admin(self, nomeUsuario=None):
        if nomeUsuario == None:
            nomeUsuario = ''
        nomeUsuario = '%{}%'.format(nomeUsuario)
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email, ativo from usuarios 
            where nomeUsuario like (%s) and tipoUsuario = {} or tipoUsuario = {}
        '''.format(extensions.TiposUsuario.Secretaria.value, extensions.TiposUsuario.Administrador.value)
        ret = self.db.busca(query, (nomeUsuario,))
        return ret

    def add_usr(self, usuario, senha, tipoUsuario, nome, email):
        try:
            query = '''
                insert into usuarios 
                (nomeUsuario, senha, tipoUsuario, ativo, nome, email) 
                values(%s, %s, %s, 1, %s, %s)
            '''
            self.db.gravar(query,(usuario, generate_password_hash(senha),tipoUsuario, nome, email.lower()))
            return self.get_usuario_username(usuario)
        except IntegrityError as ie:
            raise IntegrityError(response_messages.ERRO_INTEGRIDADE('Email ou nome de usuario'))

    def add_aluno(self, user, senha, nome, email, codAutor, codOrientador, codCurso):
        user = self.add_usr(user, senha, extensions.TiposUsuario.Aluno.value, nome, email)
        if not user:
            raise Exception(response_messages.ERRO_INESPERADO())

        now = datetime.now()
        dataValidade = now + timedelta(days=30)
        codUsuario = user['codUsuario']
        query = 'insert into usuario_orientado(codOrientador, codAutor, codUsuario, dataValidade, dataCriacao, codCurso) values (%s, %s, %s, %s, %s, %s)'
        self.db.gravar(query, (codOrientador, codAutor, codUsuario, dataValidade.__str__(), now.__str__(), codCurso))

        self.desativa_usuarios_autor_anteriores(codAutor, codUsuario)

    def desativa_usuarios_autor_anteriores(self, codAutor, codUsuario):
        aut = self.busca_usuarios_codAutor_not_codUsuario(codAutor, codUsuario)

        for item in aut:
            self.desativa_usuario(item['codUsuario'])

    def add_orientador(self, user, senha, nome, email, codOrientador):
        usr = self.add_usr(user, senha, extensions.TiposUsuario.Professor.value, nome, email)
        if not usr:
            raise Exception(response_messages.ERRO_INESPERADO())
    
        codUser = usr['codUsuario']
        query = 'update orientadores set codUsuario = (%s) where codOrientador = (%s)'
        self.db.gravar(query, (codUser, codOrientador))

    def get_count(self, codOrientador=None):
        if codOrientador:
            query = 'select count(*) as usuarios from usuarios natural join usuario_orientado where codOrientador = (%s)'
            ret = self.db.busca_um(query, (codOrientador,))
            return ret['usuarios']

        query = 'select count(*) as usuarios from usuarios'
        ret = self.db.busca_um(query, None)
        return ret['usuarios']

    def get_usuario(self, codUsuario):
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where codUsuario = (%s)'
        ret = self.db.busca_um(query,(codUsuario,))
        return ret

    def get_usuario_ativo(self, codUsuario):
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where codUsuario = (%s) and ativo = 1'
        ret = self.db.busca_um(query,(codUsuario,))
        return ret

    def get_usuario_inativo(self, codUsuario):
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where codUsuario = (%s) and ativo = 0'
        ret = self.db.busca_um(query,(codUsuario,))
        return ret

    def get_usuario_username(self, username):
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email 
            from usuarios 
            where nomeUsuario = (%s)
        '''
        ret = self.db.busca_um(query,(username,))
        return ret

    def get_usuario_email(self, email):
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where email = (%s)'
        ret = self.db.busca_um(query,(email,))
        return ret

    def get_usuario_codProjeto(self, codProjeto):
        query = '''
            select u.codUsuario
            from usuarios as u
            join usuario_orientado as uo
            on uo.codUsuario = u.codUsuario
            join autores as a
            on uo.codAutor = a.codAutor
            join projeto_autor as pa
            on pa.codAutor = a.codAutor
            join projetos as p
            on pa.codProjeto = p.codProjeto
            where p.codProjeto = (%s) and u.ativo = 1
            order by p.dataEnvio
        '''
        return self.db.busca_um(query, (codProjeto,))

    def get_user_coordenador(self, codCurso):
        query = '''
            select nome, email from usuarios as u
            natural join cursos as c 
            where codCurso = (%s)
        '''
        user = self.db.busca_um(query, (codCurso,))
        return user

    def edita_usuario(self, usuario):
        query = 'update usuarios set nomeUsuario = (%s), nome = (%s), email = (%s), tipoUsuario = (%s) where codUsuario = (%s)'
        self.db.gravar(query,(usuario['nomeUsuario'], usuario['nome'], usuario['email'].lower(), usuario['tipoUsuario'], usuario['codUsuario']))

    def deleta_usuario(self, codUsuario):
        usr = self.get_usuario_ativo(codUsuario)

        query = 'delete from usuarios where codUsuario = (%s)'
        self.db.gravar(query,(codUsuario,))
        
        if usr['tipoUsuario'] == extensions.TiposUsuario.Professor.value:
            orientador = self.orientadoresDao.get_orientador_orientando_codUsuario(codUsuario)
            if orientador:
                self.orientadoresDao.desativa_orientador(orientador['codOrientador'])

    def desativar_aluno(self, codUsuario):
        query = 'update usuarios set ativo = 0, email = null where codUsuario = (%s)'
        self.db.gravar(query, (codUsuario,))

    def desativa_usuario(self, codUsuario):
        
        usr = self.get_usuario_ativo(codUsuario)

        query = 'update usuarios set ativo = 0 where codUsuario = (%s)'
        self.db.gravar(query, (codUsuario,))

        if usr['tipoUsuario'] == extensions.TiposUsuario.Professor.value:
            orientador = self.orientadoresDao.get_orientador_codUsuario(codUsuario)
            if orientador:
                self.orientadoresDao.desativa_orientador(orientador['codOrientador'])

    def ativa_usuario(self, codUsuario):
        query = 'update usuarios set ativo = 1 where codUsuario = (%s)'
        self.db.gravar(query, (codUsuario,))

    def edita_senha(self, codUsuario, novaSenha):
        query = 'update usuarios set senha = (%s) where codUsuario = (%s)'
        self.db.gravar(query, (generate_password_hash(novaSenha), codUsuario))

    def remove_responsabilidade_orientador(self, codOrientador):
        query = '''
            select * from usuario_orientado
            where codOrientador = (%s)
        '''
        us_ori = self.db.busca(query, (codOrientador,))
        for item in us_ori:
            self.remove_responsabilidade_usuario(item)

    def remove_responsabilidade_usuario(self, usuario_orientado):
        query_upd = '''
            update usuario_orientado set codOrientador = null
            where codAutor = (%s) and codUsuario = (%s)
        '''
        
        self.db.gravar(query_upd, (usuario_orientado['codAutor'], usuario_orientado['codUsuario']))

    def gerar_solitacao(self, codUsuarioOrientado, mensagem):
        query = '''
            insert into solicitacoes_revisao(codUsuarioOrientado, mensagem) values(%s,%s)
        '''
        self.db.gravar(query, (codUsuarioOrientado, mensagem))

    def verificar_revisao(self, codUsuarioOrientado):
        query = '''
            select * from solicitacoes_revisao 
            where codUsuarioOrientado = (%s)
        '''
        ret = self.db.busca(query, (codUsuarioOrientado,))
        return ret
