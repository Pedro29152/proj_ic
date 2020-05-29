import jwt
from enum import IntEnum
from functools import wraps
from flask import request, jsonify, current_app as app
from datetime import datetime
from dateutil import parser 

from biblioteca import responses
from .usuarios import usuario_dao

class TiposUsuario(IntEnum):
    Aluno = 1
    Professor = 2
    Secretaria = 3
    Administrador = 4

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        
        try:
            data = get_token_data(auth_str)
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not current_user):
                raise Exception('Sem autorização para esta ação')
        except Exception as ex:
            res = jsonify(responses.get_erro('Erro: ' + ex.__str__()))
            res.status_code = 401
            return res
        return f(*args, **kwargs)
    return decorated

def secretaria_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        
        try:
            data = get_token_data(auth_str)
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not (current_user['tipoUsuario'] == TiposUsuario.Administrador.value or 
                    current_user['tipoUsuario'] == TiposUsuario.Secretaria.value)):
                raise Exception('Seu nível de acesso não lhe permite esta ação')
            if(not current_user):
                raise Exception('Sem autorização para esta ação')
        except Exception as ex:
            res = jsonify(responses.get_erro('Erro: ' + ex.__str__()))
            res.status_code = 401
            return res
        return f(*args, **kwargs)
    return decorated

def professor_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        
        try:
            data = get_token_data(auth_str)
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not (current_user['tipoUsuario'] == TiposUsuario.Administrador.value or 
                    current_user['tipoUsuario'] == TiposUsuario.Professor.value)):
                raise Exception('Seu nível de acesso não lhe permite esta ação')
            if(not current_user):
                raise Exception('Sem autorização para esta ação')
        except Exception as ex:
            res = jsonify(responses.get_erro('Erro: ' + ex.__str__()))
            res.status_code = 401
            return res
        return f(*args, **kwargs)
    return decorated

def aluno_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        
        try:
            data = get_token_data(auth_str)
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not (current_user['tipoUsuario'] == TiposUsuario.Administrador.value or 
                    current_user['tipoUsuario'] == TiposUsuario.Aluno.value)):
                raise Exception('Seu nível de acesso não lhe permite esta ação')
            if(not current_user):
                raise Exception('Sem autorização para esta ação')
        except Exception as ex:
            res = jsonify(responses.get_erro('Erro: ' + ex.__str__()))
            res.status_code = 401
            return res
        return f(*args, **kwargs)
    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')

        try:
            data = get_token_data(auth_str)
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not current_user['tipoUsuario'] == TiposUsuario.Administrador.value):
                raise Exception('Seu nível de acesso não lhe permite esta ação')
            if(not current_user):
                raise Exception('Sem autorização para esta ação')
        except Exception as ex:
            res = jsonify(responses.get_erro('Erro: ' + ex.__str__()))
            res.status_code = 401
            return res
        return f(*args, **kwargs)
    return decorated

def user_admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')

        try:
            data = get_token_data(auth_str)
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not current_user):
                raise Exception('Usuario invalido')
            kwargs['is_user'] = False
            if(kwargs['id'] != str(current_user['codUsuario'])):
                if(not current_user['tipoUsuario'] == TiposUsuario.Administrador.value):
                    raise Exception('Sem autorização para esta ação')
            else:
                kwargs['is_user'] = True

        except Exception as ex:
            res = jsonify(responses.get_erro('Erro: ' + ex.__str__()))
            res.status_code = 401
            return res
        return f(*args, **kwargs)
    return decorated

def get_token_data(auth_header):
    if not auth_header:
        raise Exception('Token não foi enviado')
    token_arr = auth_header.split(' ')
    if(not token_arr[0] == 'Bearer'):
        raise Exception('O Token enviado deve ser do tipo Bearer')

    try:
        token = token_arr[1]
    except IndexError:
        raise Exception('Nenhum token enviado')

    data = jwt.decode(token, app.config['SECRET_KEY'])
    if(not is_valid(data)):
        raise Exception('Token expirado')
    return data

def is_valid(token_data):
    ext = parser.parse(token_data['ext'])
    if(ext < datetime.now()):
        return False
    return True
