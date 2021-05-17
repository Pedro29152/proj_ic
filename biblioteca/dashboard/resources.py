from biblioteca.orientador.orientadores_dao import get_orientador_codUsuario
from datetime import datetime
from flask_restful import Resource, request

from biblioteca import response_messages 
from biblioteca.dashboard import dashboard_dao
from biblioteca.extensions import admin_token_required, professor_token_required
from biblioteca.responses import (
    get_success,
    get_bad_request,
    get_no_content
)

class CountProjetosSemestre(Resource):
    def get(self):
        ano = request.args.get('ano')
        semestre = request.args.get('semestre')
        
        if not ano:
            ano = datetime.now().year
        if not semestre:
            semestre = 1
        
        count_semestre = dashboard_dao.get_count_projetos_semestre(ano, semestre)

        if count_semestre != None:
            return get_success(count_semestre)
        return get_bad_request(response_messages.DADOS_PARAMETRO_INVALIDOS('"ano" e "semestre"'))

class CountProjetosAnos(Resource):
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()
        
        count_ano = dashboard_dao.get_count_projetos_semestres(anoI, anoF)
        
        if count_ano != None:
            return get_success(count_ano)
        return get_no_content()

class CountProjetosCurso(Resource):
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()

        ret = dashboard_dao.get_count_projetos_curso(anoI, anoF)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountProjetosOrientador(Resource):
    @admin_token_required
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()

        o = request.args.get('orientadores')
        if not o:
            oris = tuple()
        else:
            oris = tuple()
            for ori in o.split(','):
                try:
                    oris = oris + (int(ori),)
                except:
                    oris = tuple()
                    break

        ret = dashboard_dao.get_count_projetos_orientador(anoI, anoF, orientadores= oris)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountProjetosOrientadorSelf(Resource):
    @professor_token_required
    def get(self, user_info):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()

        orientador = get_orientador_codUsuario(user_info['codUsuario'])
        if not orientador:
            return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

        oris = tuple([orientador['raOrientador']])
        ret = dashboard_dao.get_count_projetos_orientador(anoI, anoF, orientadores= oris)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountProjetosFormandos(Resource):
    @admin_token_required
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()

        ret = dashboard_dao.get_count_projetos_formandos_curso(anoI, anoF)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountProjetoStatus(Resource):
    @admin_token_required
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()

        ret = dashboard_dao.get_count_projetos_status(anoI, anoF)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountProjetoModalidade(Resource):
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()
        
        ret = dashboard_dao.get_count_projetos_modalidade(anoI, anoF)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountSolicitacoesRevisao(Resource):
    @admin_token_required
    def get(self):
        anoI, anoF = get_anoI_anoF()
        if anoF < anoI:
            return get_no_content()
        
        ret = dashboard_dao.get_count_solicitacoes_revisao(anoI, anoF)
        if ret == None:
            return get_no_content()
        return get_success(ret)

class CountUsuariosTipo(Resource):
    @admin_token_required
    def get(self):
        ret = dashboard_dao.get_count_usuarios_tipo()
        if ret == None:
            return get_no_content()
        return get_success(ret)

class GetAnos(Resource):
    def get(self):
        ret = dashboard_dao.get_anos()
        if ret == None:
            return get_no_content()
        return get_success(ret)

def get_anoI_anoF():
    try:
        anoI = int(request.args.get('anoInicial'))
    except:
        anoI = None
    try:
        anoF = int(request.args.get('anoFinal'))
    except:
        anoF = None

    anos = dashboard_dao.get_anos()
    if not anos:
        anos = [datetime.now().year]

    if not anoI:
        anoI = anos[0]
    if not anoF:
        anoF = anos[-1]

    return anoI, anoF
