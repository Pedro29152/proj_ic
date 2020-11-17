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
    get_bad_request
)

class ReltorioProjetosResource(Resource):
    @admin_token_required
    def get(self):
        atributos = request.args.get('atributos')
        if not atributos:
            atributos = []
        else:
            try:
                atributos = [int(i) for i in atributos.split(',')]
            except ValueError:
                atributos = []

        projs_wb = get_projs_workbook(proj_attr=atributos)
        if not projs_wb:
            return get_bad_request(response_messages.ERRO_INESPERADO())

        xlsx = BytesIO(save_virtual_workbook(projs_wb))

        return send_file(xlsx, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            attachment_filename='Relatorio-Projetos.xlsx',
            as_attachment=True)




        