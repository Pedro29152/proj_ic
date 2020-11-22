from io import BytesIO

from flask import send_file
from flask_restful import Resource, request
from openpyxl.writer.excel import save_virtual_workbook

from biblioteca import response_messages
from biblioteca.xlsx import get_projs_workbook
from biblioteca.extensions import (
    admin_token_required
)
from biblioteca.responses import (
    get_bad_request,
    get_no_content
)

class ReltorioProjetosResource(Resource):
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

        projs_wb = get_projs_workbook(proj_attr=atributos, data_i=dataInicial, data_f=dataFinal)
        if not projs_wb:
            return get_bad_request(response_messages.NAO_ENCONTRADO('"trablho"'))

        xlsx = BytesIO(save_virtual_workbook(projs_wb))

        return send_file(xlsx, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            attachment_filename='Relatorio-Projetos.xlsx',
            as_attachment=True)
