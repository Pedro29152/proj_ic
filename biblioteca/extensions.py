import jwt, re, string, random, os
from werkzeug.exceptions import BadRequestKeyError
from enum import IntEnum
from functools import wraps
from flask import request, jsonify, current_app as app
from datetime import datetime
from dateutil import parser 

from biblioteca.db import get_db
from biblioteca import response_messages
from biblioteca.autor import autores_dao
from biblioteca.responses import (
    get_response_code,
    get_erro,
    get_unauthorized
)
from biblioteca.usuarios import usuario_dao

class AtributosEspeciaisProjeto(IntEnum):
    Autores = 1
    PalavrasChave = 2
    Curso = 3
    Orientadores = 4

class TiposUsuario(IntEnum):
    Aluno = 1
    Professor = 2
    Secretaria = 3
    Coordenador = 5
    Administrador = 4

class TiposOrientador(IntEnum):
    Principal = 0
    CoOrientador = 1

class StatusProjeto(IntEnum):
    Novo = 0
    Aceito = 1
    Recusado = 2

class LinguagemProjeto(IntEnum):
    Portugues = 0
    Ingles = 1
    Espanhol = 2

class ModalidadeProjeto(IntEnum):
    ArtigoCientifico = 0,
    RelatorioTecnico = 1,
    Monografia = 2,
    RelatorioTecnicoDeAtividadesDePorfolio = 3,
    Resumo = 4,
    GDD = 5

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Aluno.value,
            TiposUsuario.Professor.value,
            TiposUsuario.Secretaria.value,
            TiposUsuario.Coordenador.value,
            TiposUsuario.Administrador.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def secretaria_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value,
            TiposUsuario.Secretaria.value
        ])

        if(success):
            return f(*args, **kwargs)
        return data
    return decorated

def secretaria_aluno_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value,
            TiposUsuario.Secretaria.value,
            TiposUsuario.Aluno.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def secretaria_token_required_user_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value,
            TiposUsuario.Secretaria.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def secretaria_token_required_is_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value,
            TiposUsuario.Secretaria.value
        ], has_is_user=True, has_is_admin=True, id=kwargs['id'])

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def professor_admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value,
            TiposUsuario.Professor.value
        ])

        if(success):
            return f(*args, **kwargs)
        return data
    return decorated
    
def professor_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Professor.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def professor_coordenador_secretaria_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value,
            TiposUsuario.Professor.value,
            TiposUsuario.Secretaria.value,
            TiposUsuario.Coordenador.value
        ], has_user_info=True, has_is_admin=True, has_is_secretaria=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def aluno_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        db = get_db()
        autoresDao = autores_dao.AutoresDAO(db)

        success, data = check_tipo_usuario([
            TiposUsuario.Aluno.value
        ], has_user_info=True)

        if(success):
            is_valid = autoresDao.is_aluno_valido(data['user_info']['codUsuario'])
            if not is_valid:
                return get_unauthorized(response_messages.ACESSO_EXPIRADO())
            kwargs.update(data)
            return f(*args, **kwargs)            
        return data
    
    return decorated

def aluno_professor_coordenador_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        db = get_db()
        autoresDao = autores_dao.AutoresDAO(db)

        success, data = check_tipo_usuario([
            TiposUsuario.Aluno.value,
            TiposUsuario.Professor.value,
            TiposUsuario.Coordenador
        ], has_user_info=True)

        if(success):
            if data['user_info']['tipoUsuario'] == TiposUsuario.Aluno.value:
                is_valid = autoresDao.is_aluno_valido(data['user_info']['codUsuario'])
            else:
                is_valid = True
            
            if not is_valid:
                return get_unauthorized(response_messages.ACESSO_EXPIRADO())
            kwargs.update(data)
            return f(*args, **kwargs)            
        return data
    
    return decorated

def coordenador_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Coordenador.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def coordenador_secretaria_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Coordenador.value,
            TiposUsuario.Secretaria.value,
            TiposUsuario.Administrador.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def coordenador_professor_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Professor.value,
            TiposUsuario.Coordenador.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value
        ])

        if(success):
            return f(*args, **kwargs)
        return data
    return decorated

def admin_token_required_user_info(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value
        ], has_user_info=True)

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def admin_is_user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value
        ], has_is_user=True, id=kwargs['id'])

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated

def user_admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        success, data = check_tipo_usuario([
            TiposUsuario.Administrador.value
        ], has_is_user=True, has_is_admin=True, id=kwargs['id'])

        if(success):
            kwargs.update(data)
            return f(*args, **kwargs)
        return data
    return decorated


def check_tipo_usuario(tipos_usuario, has_is_user=False, has_is_admin=False, has_user_info=False, id=None, has_is_secretaria=False):
    is_user = False
    is_admin = False
    is_secretaria = False

    try:
        db = get_db()
        usuarioDao = usuario_dao.UsuarioDAO(db)

        authorized = False
        data = get_token_data()
        current_user = usuarioDao.busca_usuarios_nome(data['username'])

        if not current_user:
            raise Exception(response_messages.SEM_AUTORIZACAO())

        if has_is_user:
            if not id:
                raise AttributeError(response_messages.PARAMETRO_NAO_ENVIADO('"id"'))
            if id == current_user['codUsuario']:
                authorized = True 
                is_user = True

        if has_is_admin:
            if current_user['tipoUsuario'] == TiposUsuario.Administrador.value:
                authorized = True
                is_admin = True
        if has_is_secretaria:
            if current_user['tipoUsuario'] == TiposUsuario.Secretaria.value:
                authorized = True
                is_secretaria = True

        if not authorized:
            for item in tipos_usuario:
                if item == current_user['tipoUsuario']:
                    authorized = True

        if not authorized:
            raise Exception(response_messages.SEM_AUTORIZACAO())
    except Exception as ex:
        return False, get_unauthorized(ex.__str__())

    res_data = {}
    if has_is_user:
        res_data.update({ 'is_user': is_user })
    if has_is_admin:
        res_data.update({ 'is_admin': is_admin })
    if has_is_secretaria:
        res_data.update({ 'is_secretaria': is_secretaria })
    if has_user_info:
        res_data.update({ 'user_info': current_user })

    return True, res_data   

def get_token_data():
    auth_header = request.headers.get('AUTHORIZATION')

    if not auth_header:
        raise Exception(response_messages.TOKEN_NAO_ENVIADO())
    token_arr = auth_header.split(' ')
    if(not token_arr[0] == 'Bearer'):
        raise Exception(response_messages.TOKEN_TIPO_INVALIDO())

    try:
        token = token_arr[1]
    except IndexError:
        raise Exception(response_messages.TOKEN_NAO_ENVIADO())

    data = jwt.decode(
        token, 
        app.config['SECRET_KEY'], 
        algorithms=['HS256']
    )
    if(not is_valid(data)):
        raise Exception(response_messages.TOKEN_EXPIRADO())
    return data

def is_valid(token_data):
    ext = parser.parse(token_data['ext'])
    if(ext < datetime.now()):
        return False
    return True

def is_valid_email(email):
    email_regex = '(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
    return re.search(email_regex, email)

def is_valid_username(username):
    username_regex = '^(?=[a-zA-Z0-9._]{5,50}$)(?!.*[_.]{2})[^_.].*[^_.]$'
    return re.search(username_regex, username)

def is_valid_http_link(link):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, link)

def generate_random_password():
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    pwd = '' 
    for i in range(length):
        pwd = pwd + pwd.join(random.choice(chars))
    return str(pwd)

def separate_camel_case(string):
    if string == string.upper():
        return string
        
    string = string[0].upper() + string[1:]
    frase = ''
    arr = []
    for i, char in enumerate(string):
        if char.isalpha() and char.isupper():
            arr += [i]
    for i in range(len(arr)):
        if not i + 1 == len(arr):
            frase += string[arr[i]:arr[i+1]] + ' '
        else: 
            frase += string[arr[-1]:len(string)]
    return frase

def get_enum_obj(intenum, separate=True):
    obj = {}
    for i, tipo in enumerate(intenum):
        if separate:
            obj[tipo.value] = separate_camel_case(tipo.name)
        else:
            obj[tipo.value] = tipo.name
    return obj

def get_enum_values(intenum):
    arr = []

    for i, tipo in enumerate(intenum):
        arr.append(tipo.value)

    return arr

def get_maior(*args):
        maior = 0
        
        for arg in args:
            if arg > maior:
                maior = arg
        
        return maior

def get_request_form_data_attributes(atributos: list):
    ret = {}

    try:
        for campo in atributos:
            ret[campo] = request.form[campo]
        return ret
    except BadRequestKeyError:
        attr_str = ', '.join(list(map((lambda attr: '"{0}"'.format(attr)), atributos)))
        raise Exception(response_messages.CAMPOS_OBRIGATORIOS(attr_str))
