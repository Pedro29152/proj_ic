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
    OrientadorIdResource,
    SolicitarRevisaoResource,
    VerificarRevisoesResource
)
from biblioteca.projeto.resources import (
    BuscaProjetoResource,
    BuscaRankingResource,
    BuscarProjetosOrientador,
    BuscarProjetosOrientadorId,
    BuscarProjetosCoordenador,
    GetProjetoResource,
    GetProjetoOrientador,
    GetProjetoAutorResource,
    UploadProjetoResource,
    DownloadArquivoProjetoResource,
    DownloadArquivoProjetoNovoResource,
    DesativaProjetoResource,
    AtivaProjetoResource,
    AlteraProjetoResource,
    AlteraProjetoAlunoResource,
    CountProjetosResource,
    UploadProjetoAlunoResource,
    AprovarProjetoResource,
    RecusarProjetoResource
)
from biblioteca.usuarios.resources import (
    LoginResource,
    CadastroUsuarioResource,
    CadastroAlunoResource,
    CadastroProfessorExistenteResource,
    CadastroProfessorNovoResource,
    CadastroCoordenadorResource,
    CountUsuariosResource,
    UsuarioIdResource,
    MudarSenhaUsuarioResource,
    DesativaUsuarioResource,
    AtivaUsuarioResource,
    BuscaUsuariosResource,
    BuscaUsuariosInativosResource,
    BuscaUsuariosOrientadosResource,
    AlterarOrientadorDoAlunoResource,
    RecuperaraSenha
)
from biblioteca.geral.resources import (
    AllCountsResource
)
from biblioteca.autor.resources import (
    BuscaAlunosResource,
    GetAlunoResource
)
from biblioteca.coordenador.resources import (
    CoordenadorResource,
    GetCoordenadorResource,
    CountCoordenadoresResource
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

    #Rotas de revisao
    api.add_resource(SolicitarRevisaoResource, '/api/orientadores/solicitarrevisao/<int:id>')
    api.add_resource(VerificarRevisoesResource, '/api/orientadores/verificarrevisao')

    #Rotas de projetos
    api.add_resource(BuscaProjetoResource, '/api/projetos/<string:id>', 
                                           '/api/projetos') #id: titulo, curso, descricao, orientador, autor e palavrasChave
    api.add_resource(BuscaRankingResource, '/api/projetos/ranking')
    api.add_resource(BuscarProjetosOrientador, '/api/projetos/orientador')
    api.add_resource(BuscarProjetosCoordenador, '/api/projetos/coordenador')
    api.add_resource(GetProjetoOrientador, '/api/projetos/orientador/get/<int:id>')
    api.add_resource(GetProjetoAutorResource, '/api/projetos/aluno/get')
    api.add_resource(BuscarProjetosOrientadorId, '/api/projetos/orientador/<int:id>')#publico
    api.add_resource(AprovarProjetoResource, '/api/projetos/aprovar/<int:id>')
    api.add_resource(RecusarProjetoResource, '/api/projetos/recusar/<int:id>')
    api.add_resource(GetProjetoResource, '/api/projetos/get/<int:id>') #id: codigo do projeto a ser buscado
    api.add_resource(UploadProjetoResource, '/api/projetos/cadastrar')
    api.add_resource(UploadProjetoAlunoResource, '/api/projetos/cadastrar/aluno')
    api.add_resource(DownloadArquivoProjetoResource, '/api/projetos/download/<path:filename>') #filename: nome do arquivo a ser baixado
    api.add_resource(DownloadArquivoProjetoNovoResource, '/api/projetos/download/novo/<path:filename>')
    api.add_resource(DesativaProjetoResource, '/api/projetos/desativar/<int:id>') #id: codigo do projeto a ser desativado
    api.add_resource(AtivaProjetoResource, '/api/projetos/ativar/<int:id>') #id: codigo do projeto a ser ativado
    api.add_resource(AlteraProjetoResource, '/api/projetos/editar/<int:id>')  #id: codigo do projeto a ser editado
    api.add_resource(AlteraProjetoAlunoResource, '/api/projetos/editar/aluno/<int:id>')
    api.add_resource(CountProjetosResource, '/api/projetos/count')

    #Rotas de autorizacao
    api.add_resource(LoginResource, '/api/auth/login')
    #Rotas de usuario
    api.add_resource(BuscaUsuariosResource, '/api/usuarios/buscar')
    api.add_resource(BuscaUsuariosInativosResource, '/api/usuarios/buscar/inativos')
    api.add_resource(BuscaUsuariosOrientadosResource, '/api/usuarios/buscar/orientador')
    api.add_resource(UsuarioIdResource, '/api/usuarios/<int:id>')
    api.add_resource(DesativaUsuarioResource, '/api/usuarios/desativar/<int:id>')
    api.add_resource(AtivaUsuarioResource, '/api/usuarios/ativar/<int:id>')
    api.add_resource(CadastroUsuarioResource, '/api/usuarios/cadastro')
    api.add_resource(CadastroAlunoResource, '/api/usuarios/cadastro/aluno')
    api.add_resource(CadastroProfessorExistenteResource, '/api/usuarios/cadastro/orientador/existente')
    api.add_resource(CadastroProfessorNovoResource, '/api/usuarios/cadastro/orientador/novo')
    api.add_resource(CadastroCoordenadorResource, '/api/usuarios/cadastro/coordenador')
    api.add_resource(CountUsuariosResource, '/api/usuarios/count')
    api.add_resource(AlterarOrientadorDoAlunoResource, '/api/usuarios/editaorientadoraluno/<int:id>')
    api.add_resource(MudarSenhaUsuarioResource, '/api/usuarios/mudarsenha/<int:id>')
    api.add_resource(RecuperaraSenha, '/api/usuarios/recuperarsenha')

    #Rotas de autor
    api.add_resource(BuscaAlunosResource, '/api/autores')
    api.add_resource(GetAlunoResource, '/api/autores/<int:id>')

    #Rotas de coordenador
    api.add_resource(CoordenadorResource, '/api/coordenadores')
    api.add_resource(GetCoordenadorResource, '/api/coordenadores/<int:id>')
    api.add_resource(CountCoordenadoresResource, '/api/coordenadores/count')

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)