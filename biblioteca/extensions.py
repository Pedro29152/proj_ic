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
        except Exception as ex:
            return jsonify(responses.get_erro(ex.__str__()))

        try:
            ext = parser.parse(data['ext'])
            if(ext < datetime.now()):
                return jsonify(responses.get_erro('Token enviado expirou'))
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not current_user):
                raise Exception()
        except:
            return jsonify(responses.get_erro('Token enviado não é valido ou esta expirado'))
        return f(*args, **kwargs)
    return decorated

def secretaria_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        try:
            data = get_token_data(auth_str)
        except Exception as ex:
            return jsonify(responses.get_erro(ex.__str__()))
        
        try:
            ext = parser.parse(data['ext'])
            if(ext < datetime.now()):
                return jsonify(responses.get_erro('O Token enviado expirou'))
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not (current_user['tipoUsuario'] == TiposUsuario.Administrador.value or current_user['tipoUsuario'] == TiposUsuario.Secretaria.value)):
                return jsonify(responses.get_falha('Seu nível de acesso não lhe permite esta ação'))
            if(not current_user):
                raise Exception()
        except:
            return jsonify(responses.get_erro('O Token enviado não é valido ou esta expirado'))
        return f(*args, **kwargs)
    return decorated

def professor_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        try:
            data = get_token_data(auth_str)
        except Exception as ex:
            return jsonify(responses.get_erro(ex.__str__()))
        
        try:
            ext = parser.parse(data['ext'])
            if(ext < datetime.now()):
                return jsonify(responses.get_erro('O Token enviado expirou'))
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not (current_user['tipoUsuario'] == TiposUsuario.Administrador.value or current_user['tipoUsuario'] == TiposUsuario.Professor.value)):
                return jsonify(responses.get_falha('Seu nível de acesso não lhe permite esta ação'))
            if(not current_user):
                raise Exception()
        except:
            return jsonify(responses.get_erro('O Token enviado não é valido ou esta expirado'))
        return f(*args, **kwargs)
    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        try:
            data = get_token_data(auth_str)
        except Exception as ex:
            return jsonify(responses.get_erro(ex.__str__()))
        
        try:
            ext = parser.parse(data['ext'])
            if(ext < datetime.now()):
                return jsonify(responses.get_erro('O Token enviado expirou'))
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            if(not current_user['tipoUsuario'] == TiposUsuario.Administrador.value):
                return jsonify(responses.get_falha('Seu nível de acesso não lhe permite esta ação'))
            if(not current_user):
                raise Exception()
        except:
            return jsonify(responses.get_erro('O Token enviado não é valido ou esta expirado'))
        return f(*args, **kwargs)
    return decorated

def user_admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_str = request.headers.get('AUTHORIZATION')
        try:
            data = get_token_data(auth_str)
        except Exception as ex:
            return jsonify(responses.get_erro(ex.__str__()))

        try:
            ext = parser.parse(data['ext'])
            if(ext < datetime.now()):
                return jsonify(responses.get_erro('O Token enviado expirou'))
            current_user = usuario_dao.busca_usuarios_nome(data['username'])
            kwargs['is_user'] = False
            if(kwargs['id'] != str(current_user['codUsuario'])):
                if(not current_user['tipoUsuario'] == TiposUsuario.Administrador.value):
                    return jsonify(responses.get_falha('Seu nível de acesso não lhe permite esta ação'))
            else:
                kwargs['is_user'] = True
            if(not current_user):
                raise Exception()
        except:
            return jsonify(responses.get_erro('O Token enviado não é valido ou esta expirado'))
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
        return jwt.decode(token, app.config['SECRET_KEY'])
    except IndexError:
        raise Exception('Nenhum token enviado')
