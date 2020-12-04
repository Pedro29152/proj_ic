import json

from json.decoder import JSONDecodeError
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill

from biblioteca.projeto import projetos_dao
from biblioteca.curso import cursos_dao
from biblioteca.orientador import orientadores_dao
from biblioteca.extensions import (
    LinguagemProjeto,
    ModalidadeProjeto,
    separate_camel_case, 
    get_enum_obj
)

DEFAULT_FILL = PatternFill(
        fill_type= "solid",
        fgColor='b3605d'
    )
DEFAULT_FONT = Font(
        size=18,
        bold=True,
        color='ffffff'
    )


def get_projs_workbook(proj_attr= [], proj_attr_esp=[], data_i= None, data_f= None):
    projs = projetos_dao.busca_projeto(proj_attr=proj_attr, proj_attr_esp=proj_attr_esp, data_i=data_i, data_f=data_f)
    if not projs:
        return None
    
    atributos = list(projs[0].keys())
    atributos.remove('codProjeto')
    atributos.remove('codCurso')

    wb = __generate_workbook(
        title='Relatorio Trabalhos',
        header= __generate_header(atributos)
    )
    ws = wb.active
    
    column_widths = __get_base_column_widths(atributos)
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
            elif atributo == 'localPublicacao':
                try:
                    pub = json.loads(val)

                    if isinstance(pub, list):
                        texto = ''
                        for item in pub:
                            c = list(item.keys())
                            if not texto:
                                texto = item[c[0]]
                            else:
                                texto += f', {item[c[0]]}'
                        linha.append(texto)
                    elif isinstance(pub, dict):
                        c = list(pub.keys())
                        linha.append(pub[c[0]])
                    else:
                        linha.append('')
                except JSONDecodeError:
                    linha.append(val)   
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

def get_cursos_workbook(data_i= None, data_f= None):
    cursos = cursos_dao.get_relatorio_cursos(data_i=data_i, data_f=data_f)
    if not cursos:
        return None

    atributos = list(cursos[0].keys())

    wb = __generate_workbook(
        title='Relatorio Cursos',
        header= __generate_header(atributos)
    )
    ws = wb.active

    column_widths = __get_base_column_widths(atributos)
    for i, curso in enumerate(cursos):
        linha = []
        
        for j, atributo in enumerate(atributos):
            val = curso[atributo]
            
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

def get_orientadores_workbook(data_i= None, data_f= None):
    orientadores = orientadores_dao.get_relatorio_orientadores(data_i=data_i, data_f=data_f)
    if not orientadores:
        return None

    atributos = list(orientadores[0].keys())

    wb = __generate_workbook(
        title='Relatorio Orientadores',
        header= __generate_header(atributos)
    )
    ws = wb.active

    column_widths = __get_base_column_widths(atributos)

    for i, orientador in enumerate(orientadores):
        linha = []

        for j, atributo in enumerate(atributos):
            val = orientador[atributo]
            
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

def __generate_workbook(title='', header='', header_font=DEFAULT_FONT, header_fill=DEFAULT_FILL):
    wb = Workbook()
    ws = wb.active
    if title != '':
        ws.title = title
    ws.append(header)

    for cell in ws['1:1']:
        cell.font = header_font
        cell.fill = header_fill

    return wb

def __get_base_column_widths(attrs):
    return [(len(separate_camel_case(att)) + 3) * 1.6 for att in attrs]
