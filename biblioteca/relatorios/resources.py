from io import BytesIO
from datetime import datetime

from flask import send_file
from flask_restful import Resource, request
from openpyxl.writer.excel import save_virtual_workbook

from biblioteca import response_messages
from biblioteca.xlsx import (
    get_projs_workbook,
    get_cursos_workbook
)
from biblioteca.extensions import (
    admin_token_required
)
from biblioteca.responses import (
    get_bad_request,
    get_no_content
)

class RelatorioProjetosResource(Resource):
    def get(self):
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
        if not atributosEsp:
            atributosEsp = []
        else:
            try:
                atributosEsp = [int(i) for i in atributosEsp.split(',')]
            except ValueError:
                atributosEsp = []

        projs_wb = get_projs_workbook(proj_attr=atributos, proj_attr_esp=atributosEsp, data_i=dataInicial, data_f=dataFinal)
        if not projs_wb:
            return get_bad_request(response_messages.NAO_FOI_POSSIVEL('gerar um relatorio com os parametros enviados'))

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        return get_excel(projs_wb, 'Relatorio-Trabalhos-{0}'.format(data_str))

class RelatorioCursosResource(Resource):
    def get(self):
        dataInicial = (request.args.get('dataInicial'))
        dataFinal = (request.args.get('dataFinal'))

        if (dataInicial and not dataFinal) or (not dataInicial and dataFinal):
            return get_no_content()
        
        cursos_wb = get_cursos_workbook(data_i=dataInicial, data_f=dataFinal)
        if not cursos_wb:
            return get_bad_request(response_messages.NAO_FOI_POSSIVEL('gerar um relatorio com os parametros enviados'))

        data = datetime.now()
        data_str = f'{data.day}-{data.month}-{data.year}'

        return get_excel(cursos_wb, title='Relatorio-Cursos-{0}'.format(data_str))


def get_excel(xlsx_wb, title='arquivo'):
    file = BytesIO(save_virtual_workbook(xlsx_wb))

    title += '.xlsx'

    return send_file(file, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        attachment_filename=title,
        as_attachment=True)
