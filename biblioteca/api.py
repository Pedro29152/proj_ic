# -*- coding: utf-8 -*-

# Importamos as classes API e Resource
from flask import jsonify
from flask_restful import Api, Resource
from biblioteca.curso.resources import (
    CursoResource, 
    AtivaCursoResource, 
    DesativaCursoResource, 
    CountCursosResource, 
    TodosCursosResource,
    CursoIdResource
)
from biblioteca.orientador.resources import (
    OrientadorResource,
    CountOrientadoresResource,
    AtivaOrientadorResource,
    DesativaOrientadorResource,
    TodosOrientadoresResource, 
    OrientadorIdResource
)
from biblioteca.projeto.resources import (
    BuscaProjetoResource,
    BuscaRankingResource,
    GetProjetoResource,
    UploadProjetoResource,
    DownloadArquivoProjetoResource,
    DesativaProjetoResource,
    AtivaProjetoResource,
    AlteraProjetoResource,
    CountProjetosResource,
    UploadProjetoAlunoResource
)
from biblioteca.usuarios.resources import (
    LoginResource,
    CadastroUsuarioResource,
    CadastroAlunoResource,
    CountUsuariosResource,
    BuscaUsuariosResource,
    UsuarioIdResource,
    MudarSenhaUsuarioResource
)
from biblioteca.geral.resources import (
    AllCountsResource
)
from .db import bd_busca   

# Criamos uma classe que extende de Resource
class Index(Resource):
    def get(self):
        return {
            'name': 'Biblioteca de Trabalhos Científicos',
            'versao':'0.1.0'
        }

# Instânciamos a API do FlaskRestful
api = Api()

def configure_api(app):

    # adicionamos na rota '/' a sua classe correspondente Index
    api.add_resource(Index, '/api')
    api.add_resource(AllCountsResource, '/api/allcounts')

    #Rotas de curso
    api.add_resource(CursoResource, '/api/cursos')
    api.add_resource(TodosCursosResource, '/api/cursos/todos')
    api.add_resource(CountCursosResource, '/api/cursos/count')
    api.add_resource(CursoIdResource, '/api/cursos/<int:id>')
    api.add_resource(AtivaCursoResource, '/api/cursos/ativar/<int:id>')
    api.add_resource(DesativaCursoResource, '/api/cursos/desativar/<int:id>')

    #Rotas de orientador
    api.add_resource(OrientadorResource, '/api/orientadores')
    api.add_resource(OrientadorIdResource, '/api/orientadores/<int:id>')
    api.add_resource(TodosOrientadoresResource, '/api/orientadores/todos')
    api.add_resource(AtivaOrientadorResource, '/api/orientadores/ativar/<int:id>')
    api.add_resource(DesativaOrientadorResource, '/api/orientadores/desativar/<int:id>')
    api.add_resource(CountOrientadoresResource, '/api/orientadores/count')

    #Rotas de projetos
    api.add_resource(BuscaProjetoResource, '/api/projetos/<string:id>', '/api/projetos') #id: titulo, curso, descricao, orientador, autor e palavrasChave
    api.add_resource(BuscaRankingResource, '/api/projetos/ranking')
    api.add_resource(GetProjetoResource, '/api/projetos/get/<int:id>') #id: codigo do projeto a ser buscado
    api.add_resource(UploadProjetoResource, '/api/projetos/cadastrar')
    api.add_resource(UploadProjetoAlunoResource, '/api/projetos/cadastrar/aluno')
    api.add_resource(DownloadArquivoProjetoResource, '/api/projetos/download/<path:filename>') #filename: nome do arquivo a ser baixado
    api.add_resource(DesativaProjetoResource, '/api/projetos/desativar/<int:id>') #id: codigo do projeto a ser desativado
    api.add_resource(AtivaProjetoResource, '/api/projetos/ativar/<int:id>') #id: codigo do projeto a ser ativado
    api.add_resource(AlteraProjetoResource, '/api/projetos/editar/<int:id>')  #id: codigo do projeto a ser editado
    api.add_resource(CountProjetosResource, '/api/projetos/count')

    #Rotas de autorizacao
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(BuscaUsuariosResource, '/api/usuarios/buscar')
    api.add_resource(UsuarioIdResource, '/api/usuarios/<int:id>')
    api.add_resource(CadastroUsuarioResource, '/api/usuarios/cadastro')
    api.add_resource(CadastroAlunoResource, '/api/usuarios/cadastro/aluno')
    api.add_resource(CountUsuariosResource, '/api/usuarios/count')
    api.add_resource(MudarSenhaUsuarioResource, '/api/usuarios/mudarsenha/<int:id>')

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)