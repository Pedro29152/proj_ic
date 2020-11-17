from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill

from biblioteca.projeto import projetos_dao
from biblioteca.extensions import (
    LinguagemProjeto,
    ModalidadeProjeto,
    separate_camel_case, 
    get_enum_obj
)

def get_projs_workbook(proj_attr=[]):
    projs = projetos_dao.busca_projeto(proj_attr=proj_attr)
    if not projs:
        return None
    
    atributos = list(projs[0].keys())
    atributos.remove('codProjeto')
    atributos.remove('codCurso')

    wb = __generate_workbook(
        title='Relatorio Projetos',
        header= __generate_header(atributos),
        header_font=Font(size=18, bold=True, color='ffffff'),
        header_fill=PatternFill(fill_type= "solid", fgColor='b3605d')
    )
    ws = wb.active
    
    column_widths = [(len(separate_camel_case(att)) + 3) * 1.6 for att in atributos]
    for i, projeto in enumerate(projs):
        linha = []

        for j, atributo in enumerate(atributos):
            val = projeto[atributo]
            if atributo == 'autores':
                texto = ''
                for item in val:
                    if not texto:
                        texto = item['nomeAutor']
                    else:
                        texto += f', {item["nomeAutor"]}'
                linha.append(texto)
            elif atributo == 'orientadores':
                texto = ''
                for item in val:
                    if not texto:
                        texto = item['nomeOrientador']
                    else:
                        texto += f', {item["nomeOrientador"]}'
                linha.append(texto)
            elif atributo == 'palavrasChave':
                texto = ''
                for item in val:
                    if not texto:
                        texto = item['palavraChave']
                    else:
                        texto += f', {item["palavraChave"]}'
                linha.append(texto)
            elif atributo == 'curso':
                linha.append(val['abreviacao'])
            elif atributo == 'linguagem':
                linha.append(get_enum_obj(LinguagemProjeto)[val])
            elif atributo == 'modalidade':
                linha.append(get_enum_obj(ModalidadeProjeto)[val])
            else:
                linha.append(val)
            
            tam_cell = (len(str(linha[j])) + 3)
            if tam_cell > 80:
                tam_cell = 80
            
            if len(column_widths) > j:
                if tam_cell > column_widths[j]:
                    column_widths[j] = tam_cell
            else:
                column_widths += [tam_cell]

        ws.append(linha)

    for i, column_width in enumerate(column_widths):
        ws.column_dimensions[get_column_letter(i+1)].width = column_width
    
    return wb

def __generate_header(attr):
    ret = [separate_camel_case(key) for key in attr]
    return ret

def __generate_workbook(title='', header='', header_font=None, header_fill=None):
    wb = Workbook()
    ws = wb.active
    if title != '':
        ws.title = title
    ws.append(header)

    for cell in ws['1:1']:
        cell.font = header_font
        cell.fill = header_fill

    return wb
