import tempfile, os

from io import BytesIO
from datetime import datetime

from flask import send_file
from flask_restful import Resource, request

from biblioteca.db import get_db
from biblioteca import response_messages
from biblioteca.orientador.orientadores_dao import OrientadoresDAO
from biblioteca.xlsx import (
    get_projs_workbook,
    get_cursos_workbook,
    get_orientadores_workbook,
    get_autores_workbook
)
from biblioteca.extensions import (
    admin_token_required_user_info,
    professor_token_required,
    get_enum_values,
    AtributosEspeciaisProjeto
)
from biblioteca.responses import (
    get_bad_request,
    get_no_content
)

class RelatorioProjetosResource(Resource):
    @admin_token_required_user_info
    def get(self, user_info):
        dataInicial = (request.args.get('dataInicial'))
        dataFinal = (request.args.get('dataFinal'))

        if (dataInicial and not dataFinal) or (not dataInicial and dataFinal):
            return get_no_content()
        
        atributos = request.args.get('atributos')
        if not atributos:
            atributos = []
        else:
            try:
                atributos = [int(i) for i in atributos.split(',')]
            except ValueError:
                atributos = []

        atributosEsp = request.args.get('atributosEspeciais')
        default = get_enum_values(AtributosEspeciaisProjeto)
        if not atributosEsp:
            atributosEsp = default
        else:
            try:
                atributosEsp = [int(i) for i in atributosEsp.split(',')]
                if not atributosEsp:
                    atributosEsp = default
            except ValueError:
                atributosEsp = default

        projs_wb = get_projs_workbook(
            proj_attr=atributos, 
            proj_attr_esp=atributosEsp, 
            data_i=dataInicial,
            data_f=dataFinal,
            user=user_info
        )
        if not projs_wb:
            return get_bad_request(response_messages.NAO_FOI_POSSIVEL('gerar um relatorio com os parametros enviados'))

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        return get_excel(projs_wb, 'Relatorio-Trabalhos-{0}'.format(data_str))

class RelatorioCursosResource(Resource):
    @admin_token_required_user_info
    def get(self, user_info):
        dataInicial = (request.args.get('dataInicial'))
        dataFinal = (request.args.get('dataFinal'))

        if (dataInicial and not dataFinal) or (not dataInicial and dataFinal):
            return get_no_content()
        
        cursos_wb = get_cursos_workbook(
            data_i=dataInicial, 
            data_f=dataFinal,
            user=user_info
        )
        if not cursos_wb:
            return get_bad_request(response_messages.NAO_FOI_POSSIVEL('gerar um relatorio com os parametros enviados'))

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        return get_excel(cursos_wb, title='Relatorio-Cursos-{0}'.format(data_str))

class RelatorioOrientadoresResource(Resource):
    @admin_token_required_user_info
    def get(self, user_info):
        dataInicial = (request.args.get('dataInicial'))
        dataFinal = (request.args.get('dataFinal'))

        if (dataInicial and not dataFinal) or (not dataInicial and dataFinal):
            return get_no_content()

        orientadores_wb = get_orientadores_workbook(
            data_i=dataInicial, 
            data_f=dataFinal,
            user=user_info
        )
        if not orientadores_wb:
            return get_bad_request(response_messages.NAO_FOI_POSSIVEL('gerar um relatorio com os parametros enviados'))

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        return get_excel(orientadores_wb, title='Relatorio-Orientadores-{0}'.format(data_str))

class RelatorioOrientadoresSelfResource(Resource):
    @professor_token_required
    def get(self, user_info):
        db = get_db()
        orientadoresDao = OrientadoresDAO(db)
            
        orientador = orientadoresDao.get_orientador_codUsuario(user_info['codUsuario'])
        if not orientador:
            return get_bad_request(response_messages.USUARIO_NAO_RELACIONADO())

        dataInicial = (request.args.get('dataInicial'))
        dataFinal = (request.args.get('dataFinal'))

        if (dataInicial and not dataFinal) or (not dataInicial and dataFinal):
            return get_no_content()
        
        atributos = request.args.get('atributos')
        if not atributos:
            atributos = []
        else:
            try:
                atributos = [int(i) for i in atributos.split(',')]
            except ValueError:
                atributos = []

        atributosEsp = request.args.get('atributosEspeciais')
        default = get_enum_values(AtributosEspeciaisProjeto)
        if not atributosEsp:
            atributosEsp = default
        else:
            try:
                atributosEsp = [int(i) for i in atributosEsp.split(',')]
                if not atributosEsp:
                    atributosEsp = default
            except ValueError:
                atributosEsp = default

        projs_wb = get_projs_workbook(
            proj_attr=atributos, 
            proj_attr_esp=atributosEsp, 
            data_i=dataInicial, 
            data_f=dataFinal, 
            has_filtro_orientador=True, 
            codOrientador=orientador['codOrientador'],
            user=user_info
        )
        if not projs_wb:
            return get_no_content()

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        nome = orientador['nomeOrientador'].split(' ')[0]

        return get_excel(projs_wb, 'Relatorio-Orientador-{0}-{1}'.format(nome, data_str))

class RelatorioAutoresResource(Resource):
    @admin_token_required_user_info
    def get(self, user_info):
        dataInicial = (request.args.get('dataInicial'))
        dataFinal = (request.args.get('dataFinal'))

        if (dataInicial and not dataFinal) or (not dataInicial and dataFinal):
            return get_no_content()

        autores_wb = get_autores_workbook(
            data_i=dataInicial, 
            data_f=dataFinal,
            user=user_info
        )
        if not autores_wb:
            return get_bad_request(response_messages.NAO_FOI_POSSIVEL('gerar um relatorio com os parametros enviados'))

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        return get_excel(autores_wb, title='Relatorio-Autores-{0}'.format(data_str))


def get_excel(xlsx_wb, title='arquivo'):
    with open(os.path.join(tempfile.gettempdir(), title), 'wb+') as tmp_file:
        xlsx_wb.save(tmp_file.name)
        file = BytesIO(tmp_file.read())

        title += '.xlsx'

        return send_file(file, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            download_name=title,
            as_attachment=True)
