from mysql.connector.errors import DatabaseError
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector.errors import IntegrityError
from datetime import datetime, timedelta
from biblioteca.db import Db
from biblioteca.orientador import orientadores_dao
from biblioteca import extensions

def verifica_usr(usuario, senha):
    
    senhaR = busca_senha_nome(usuario)
    
    if(senhaR):
        if(check_password_hash(senhaR, senha)):
            return busca_usuarios_nome(usuario)

    return None

def busca_usuarios():
    with Db() as db:
        val = db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where ativo = 1',
            None
        )
        if(not val):
            val = []

        return val

def busca_usuarios_nome_like(nomeUsuario):
    with Db() as db:
        nomeUsuario = '%{}%'.format(nomeUsuario)
        val = db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario like (%s) and ativo = 1',
            (nomeUsuario,)
        )
        if(not val):
            val = []

        return val

def busca_usuarios_inativos():
    with Db() as db:
        val = db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where ativo = 0',
            None
        )
        if(not val):
            val = []

        return val

def busca_usuarios_inativos_nome_like(nomeUsuario):
    with Db() as db:
        nomeUsuario = '%{}%'.format(nomeUsuario)
        val = db.busca(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario like (%s) and ativo = 0',
            (nomeUsuario,)
        )
        if(not val):
            val = []

        return val

def busca_usuarios_codAutor_not_codUsuario(codAutor, codUsuario):
    with Db() as db:
        query = '''
            select u.codUsuario, nomeUsuario, tipoUsuario, u.nome, u.email 
            from usuarios as u 
            join usuario_orientado as uo 
            on uo.codUsuario = u.codUsuario 
            join autores as a 
            on a.codAutor = uo.codAutor 
            where ativo = 1 and a.codAutor = (%s) and not u.codUsuario = (%s)
        '''
        return db.busca(query, (codAutor, codUsuario))

def busca_usuarios_nome(nomeUsuario):
    with Db() as db:
        val = db.busca_um(
            'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where nomeUsuario = (%s) and ativo = 1',
            (nomeUsuario,)
        )

        return val

def busca_usuarios_orientados_nome_like(nomeUsuario, codOrientador):
    with Db() as db:
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email 
            from usuarios as u 
            natural join usuario_orientado as uo 
            where uo.codOrientador = (%s) and nomeUsuario like (%s) and ativo = 1
        '''
        ret = db.busca(query,(codOrientador, nomeUsuario))
        return ret

def busca_usuarios_orientados(codOrientador):
    with Db() as db:
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email 
            from usuarios as u 
            natural join usuario_orientado as uo 
            where uo.codOrientador = (%s) and ativo = 1
        '''
        ret = db.busca(query,(codOrientador,))
        return ret

def busca_senha_nome(nomeUsuario):
    with Db() as db:
        val = db.busca_um(
            'select senha from usuarios where nomeUsuario = (%s) and ativo = 1',
            (nomeUsuario,)
        )
        if val:
            return val['senha']
        return None

def buscar_usuarios_secretaria(nomeUsuario=None):
    with Db() as db:
        if nomeUsuario == None:
            nomeUsuario = ''
        nomeUsuario = '%{}%'.format(nomeUsuario) 
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email, ativo from usuarios 
            where nomeUsuario like (%s) and tipoUsuario = {}
        '''.format(extensions.TiposUsuario.Secretaria.value)
        ret = db.busca(query, (nomeUsuario,))
        return ret

def buscar_usuarios_admin(nomeUsuario=None):
    with Db() as db:
        if nomeUsuario == None:
            nomeUsuario = ''
        nomeUsuario = '%{}%'.format(nomeUsuario)
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email, ativo from usuarios 
            where nomeUsuario like (%s) and tipoUsuario = {} or tipoUsuario = {}
        '''.format(extensions.TiposUsuario.Secretaria.value, extensions.TiposUsuario.Administrador.value)
        ret = db.busca(query, (nomeUsuario,))
        return ret

def add_usr(usuario, senha, tipoUsuario, nome, email):
    with Db() as db:
        try:
            query = '''
                insert into usuarios 
                (nomeUsuario, senha, tipoUsuario, ativo, nome, email) 
                values(%s, %s, %s, 1, %s, %s)
            '''
            db.gravar_autocommit(query,(usuario, generate_password_hash(senha),tipoUsuario, nome, email.lower()))
            return get_usuario_username(usuario)
        except IntegrityError:
            db.rollback()
            return None
        except Exception as ex:
            db.rollback()
            raise ex

def add_aluno(user, senha, nome, email, codAutor, codOrientador, codCurso):
    with Db() as db:
        user = add_usr(user, senha, 1, nome, email)
        if not user:
            return False
        
        now = datetime.now()
        dataValidade = now + timedelta(days=30)
        codUsuario = user['codUsuario']
        query = 'insert into usuario_orientado(codOrientador, codAutor, codUsuario, dataValidade, dataCriacao, codCurso) values (%s, %s, %s, %s, %s, %s)'
        db.gravar_autocommit(query, (codOrientador, codAutor, codUsuario, dataValidade.__str__(), now.__str__(), codCurso))

        desativa_anteriores(codAutor, codUsuario)

        return True

def desativa_anteriores(codAutor, codUsuario):
    aut = busca_usuarios_codAutor_not_codUsuario(codAutor, codUsuario)

    for item in aut:
        desativa_usuario(item['codUsuario'])

def add_orientador(user, senha, nome, email, codOrientador):
    with Db() as db:
        usr = add_usr(user, senha, 2, nome, email)
        if not usr:
            return False

        codUser = usr['codUsuario']
        query = 'update orientadores set codUsuario = (%s) where codOrientador = (%s)'
        db.gravar_autocommit(query, (codUser, codOrientador))
        return True

def get_count(codOrientador=None):
    with Db() as db:
        if codOrientador:
            query = 'select count(*) as usuarios from usuarios natural join usuario_orientado where codOrientador = (%s)'
            ret = db.busca_um(query, (codOrientador,))
            return ret['usuarios']

        query = 'select count(*) as usuarios from usuarios'
        ret = db.busca_um(query, None)
        return ret['usuarios']

def get_usuario(codUsuario):
    with Db() as db:
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where codUsuario = (%s) and ativo = 1'
        ret = db.busca_um(query,(codUsuario,))
        return ret

def get_usuario_inativo(codUsuario):
    with Db() as db:
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where codUsuario = (%s) and ativo = 0'
        ret = db.busca_um(query,(codUsuario,))
        return ret

def get_usuario_username(username):
    with Db() as db:
        query = '''
            select codUsuario, nomeUsuario, tipoUsuario, nome, email 
            from usuarios 
            where nomeUsuario = (%s)
        '''
        ret = db.busca_um(query,(username,))
        return ret

def get_usuario_email(email):
    with Db() as db:
        query = 'select codUsuario, nomeUsuario, tipoUsuario, nome, email from usuarios where email = (%s)'
        ret = db.busca_um(query,(email,))
        return ret

def get_usuario_codProjeto(codProjeto):
    with Db() as db:
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
        return db.busca_um(query, (codProjeto,))

def get_user_coordenador(codCurso):
    with Db() as db:
        query = '''
            select nome, email from usuarios as u
            natural join cursos as c 
            where codCurso = (%s)
        '''
        user = db.busca_um(query, (codCurso,))
        return user

def edita_usuario(usuario):
    with Db() as db:
        query = 'update usuarios set nomeUsuario = (%s), nome = (%s), email = (%s), tipoUsuario = (%s) where codUsuario = (%s)'
        db.gravar_autocommit(query,(usuario['nomeUsuario'], usuario['nome'], usuario['email'].lower(), usuario['tipoUsuario'], usuario['codUsuario']))

def deleta_usuario(codUsuario):
    with Db() as db:
        usr = get_usuario(codUsuario)

        query = 'delete from usuarios where codUsuario = (%s)'
        db.gravar_autocommit(query,(codUsuario,))
        
        if usr['tipoUsuario'] == extensions.TiposUsuario.Professor.value:
            orientador = orientadores_dao.get_orientador_orientando_codUsuario(codUsuario)
            if orientador:
                orientadores_dao.desativa_orientador(orientador['codOrientador'])

def desativar_aluno(codUsuario):
    with Db() as db:
        query = 'update usuarios set ativo = 0, email = null where codUsuario = (%s)'
        db.gravar_autocommit(query, (codUsuario,))

def desativa_usuario(codUsuario):
    with Db() as db:
        usr = get_usuario(codUsuario)

        query = 'update usuarios set ativo = 0 where codUsuario = (%s)'
        db.gravar_autocommit(query, (codUsuario,))

        if usr['tipoUsuario'] == extensions.TiposUsuario.Professor.value:
            orientador = orientadores_dao.get_orientador_codUsuario(codUsuario)
            if orientador:
                orientadores_dao.desativa_orientador(orientador['codOrientador'])

def ativa_usuario(codUsuario):
    with Db() as db:
        query = 'update usuarios set ativo = 1 where codUsuario = (%s)'
        db.gravar_autocommit(query, (codUsuario,))

def edita_senha(codUsuario, novaSenha):
    with Db() as db:
        query = 'update usuarios set senha = (%s) where codUsuario = (%s)'
        db.gravar_autocommit(query, (generate_password_hash(novaSenha), codUsuario))

def remove_responsabilidade_orientador(codOrientador):
    with Db() as db:
        query = '''
            select * from usuario_orientado
            where codOrientador = (%s)
        '''
        us_ori = db.busca(query, (codOrientador,))
        for item in us_ori:
            remove_responsabilidade_usuario(item)

def remove_responsabilidade_usuario(usuario_orientado):
    with Db() as db:
        query_upd = '''
            update usuario_orientado set codOrientador = null
            where codAutor = (%s) and codUsuario = (%s)
        '''
        
        db.gravar_autocommit(query_upd, (usuario_orientado['codAutor'], usuario_orientado['codUsuario']))

def gerar_solitacao(codUsuarioOrientado, mensagem):
    with Db() as db:
        query = '''
            insert into solicitacoes_revisao(codUsuarioOrientado, mensagem) values(%s,%s)
        '''
        db.gravar_autocommit(query, (codUsuarioOrientado, mensagem))

def verificar_revisao(codUsuarioOrientado):
    with Db() as db:
        query = '''
            select * from solicitacoes_revisao 
            where codUsuarioOrientado = (%s)
        '''
        ret = db.busca(query, (codUsuarioOrientado,))
        return ret
