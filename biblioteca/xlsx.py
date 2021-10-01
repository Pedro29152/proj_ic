import json

from json.decoder import JSONDecodeError
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill

from biblioteca.db import Db
from biblioteca.projeto.projetos_dao import ProjetosDAO
from biblioteca.orientador.orientadores_dao import OrientadoresDAO
from biblioteca.curso.cursos_dao import CursosDAO
from biblioteca.autor import autores_dao
from biblioteca.extensions import (
    LinguagemProjeto,
    ModalidadeProjeto,
    separate_camel_case, 
    get_enum_obj,
    get_maior
)

HEADER_FILL = PatternFill(
        fill_type= "solid",
        fgColor='b3605d'
    )
HEADER_FONT = Font(
        size=18,
        bold=True,
        color='ffffff'
    )

INFO_FILL = PatternFill(
        fill_type= "solid",
        fgColor='c3706d'
    )
INFO_FONT = Font(
        size=22,
        bold=True,
        color='ffffff'
    )


def get_projs_workbook(proj_attr= [], proj_attr_esp=[], data_i= None, data_f= None, has_filtro_orientador=False, codOrientador=None, user=None):
    with Db() as db:
        projetosDao = ProjetosDAO(db)

        if has_filtro_orientador:
            if not codOrientador:
                return None
            projs = projetosDao.busca_reltorio_projeto_orientador(codOrientador, proj_attr=proj_attr, proj_attr_esp=proj_attr_esp, data_i=data_i, data_f=data_f)
        else:
            projs = projetosDao.busca_projeto(proj_attr=proj_attr, proj_attr_esp=proj_attr_esp, data_i=data_i, data_f=data_f)
        if not projs:
            return None
        
        atributos = list(projs[0].keys())
        atributos.remove('codProjeto')
        atributos.remove('codCurso')
        
        
        info = [
            'FATEC de Carapicuíba',
            'Gerado por: {}'.format(user['nome']),
            'Data: {}'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
        ]

        header = __generate_header(atributos)

        column_widths = __format_column_widths( 
            __get_base_column_widths_info(info), 
            __get_base_column_widths_header(header),
            __get_base_column_widths(atributos)
        )

        dif = len(header) - len(info)
        for i in range(dif if dif > 0 else 0):
            info.append('')

        wb = __generate_workbook(
            title='Relatorio Trabalhos',
            info=info,
            header=header
        )
        ws = wb.active

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

def get_cursos_workbook(data_i= None, data_f= None, user=None):
    with Db() as db:
        cursosDao = CursosDAO(db)
        
        cursos = cursosDao.get_relatorio_cursos(data_i=data_i, data_f=data_f)
        if not cursos:
            return None

        atributos = list(cursos[0].keys())

        info = [
            'FATEC de Carapicuíba',
            'Gerado por: {}'.format(user['nome']),
            'Data: {}'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
        ]
        
        header = __generate_header(atributos)

        column_widths = __format_column_widths( 
            __get_base_column_widths_info(info), 
            __get_base_column_widths_header(header),
            __get_base_column_widths(atributos)
        )

        dif = len(header) - len(info)
        for i in range(dif if dif > 0 else 0):
            info.append('')

        wb = __generate_workbook(
            title='Relatorio Cursos',
            info=info,
            header= __generate_header(atributos)
        )
        ws = wb.active

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

def get_orientadores_workbook(data_i= None, data_f= None, user=None):
    with Db() as db:
        orientadoresDao = OrientadoresDAO(db)

        orientadores = orientadoresDao.get_relatorio_orientadores(data_i=data_i, data_f=data_f)
        if not orientadores:
            return None

        atributos = list(orientadores[0].keys())

        info = [
            'FATEC de Carapicuíba',
            'Gerado por: {}'.format(user['nome']),
            'Data: {}'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
        ]
        
        header = __generate_header(atributos)

        column_widths = __format_column_widths( 
            __get_base_column_widths_info(info), 
            __get_base_column_widths_header(header),
            __get_base_column_widths(atributos)
        )

        dif = len(header) - len(info)
        for i in range(dif if dif > 0 else 0):
            info.append('')

        wb = __generate_workbook(
            title='Relatorio Orientadores',
            info=info,
            header= __generate_header(atributos)
        )
        ws = wb.active

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

def get_autores_workbook(data_i=None, data_f=None, user=None):
    autores = autores_dao.get_relatorio_autores(data_i=data_i, data_f=data_f)
    if not autores:
        return None

    atributos = list(autores[0].keys())

    info = [
        'FATEC de Carapicuíba',
        'Gerado por: {}'.format(user['nome']),
        'Data: {}'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
    ]
    
    header = __generate_header(atributos)

    column_widths = __format_column_widths( 
        __get_base_column_widths_info(info), 
        __get_base_column_widths_header(header),
        __get_base_column_widths(atributos)
    )

    dif = len(header) - len(info)
    for i in range(dif if dif > 0 else 0):
        info.append('')

    wb = __generate_workbook(
        title='Relatorio de Autores',
        info=info,
        header= __generate_header(atributos)
    )
    ws = wb.active

    for i, autor in enumerate(autores):
        linha = []

        for j, atributo in enumerate(atributos):
            val = autor[atributo]
            
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

def __generate_workbook(title=None, header=None, info=None, header_font=HEADER_FONT, header_fill=HEADER_FILL, info_font=INFO_FONT, info_fill=INFO_FILL):
    wb = Workbook()
    ws = wb.active

    if title != None:
        ws.title = title
    linha = 1

    if info:
        ws.append(info)

        for cell in ws['{0}:{0}'.format(linha)]:
            cell.font = info_font
            cell.fill = info_fill
        
        linha += 1

    if header:
        ws.append(header)

        for cell in ws['{0}:{0}'.format(linha)]:
            cell.font = header_font
            cell.fill = header_fill

        linha += 1

    return wb

def __get_base_column_widths(attrs):
    return [(len(separate_camel_case(att)) + 3) * 1.6 for att in attrs]

def __get_base_column_widths_header(attrs):
    return [(len(separate_camel_case(att)) + 3) * 1.7 for att in attrs]

def __get_base_column_widths_info(attrs):
    return [(len(separate_camel_case(att)) + 3) * 1.9 for att in attrs]

def __format_column_widths(arr1, arr2, arr3):
    tam = get_maior(len(arr1), len(arr2), len(arr3))
    ret = list()

    for i in range(tam):
        try:
            i1 = arr1[i]
        except:
            i1 = 0
        try:
            i2 = arr2[i]
        except:
            i2 = 0
        try:
            i3 = arr3[i]
        except:
            i3 = 0

        ret.append(get_maior(i1, i2, i3))
    return ret
