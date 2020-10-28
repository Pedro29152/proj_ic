from datetime import datetime
from flask_restful import Resource, request

from biblioteca import response_messages 
from biblioteca.dashboard import dashboard_dao
from biblioteca.responses import (
    get_success,
    get_bad_request
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
        anoI = request.args.get('anoI')
        anoF = request.args.get('anoF')
        
        if not anoI:
            anoI = datetime.now().year
        if not anoF:
            anoF = datetime.now().year
        
        count_ano = dashboard_dao.get_count_projetos_semestres(anoI, anoF)
        
        if count_ano != None:
            return get_success(count_ano)
        return get_bad_request(response_messages.DADOS_PARAMETRO_INVALIDOS('"anoI" e "anoF"'))
