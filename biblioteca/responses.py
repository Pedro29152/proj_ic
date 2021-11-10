from flask import jsonify

from biblioteca import response_messages

def get_ok(message='OK'):
    return {
        'status':'OK',
        'message': message
    }

def get_erro(message='erro'):
    return {
        'status':'erro',
        'message': message
    }
    
def get_falha(message='falha'):
    return {
        'status':'falha',
        'message': message
    }

def get_negado(message='negado'):
    return {
        'status':'acesso negado',
        'message': message
    }

def get_data(data):
    return {
        'status': 'OK',
        'data': data
    }

def get_page(data, size, complete_size, page):
    return {
        'status': 'OK',
        'data': data,
        'size': size,
        'complete_size': complete_size,
        'page': page
    }

def get_count(count):
    return {
        'status': 'OK',
        'count': count
    }

def get_success(data):
    res = jsonify(get_data(data))
    res.status_code = 200
    return res

def get_unauthorized(data):
    res = jsonify(get_erro(data))
    res.status_code = 401
    return res

def get_bad_request(data):
    res = jsonify(get_falha(data))
    res.status_code = 400
    return res

def get_not_found(data=None):
    if not data:
        data=response_messages.PAGINA_NAO_ENCONTRADA()
    res = jsonify(get_erro(data))
    res.status_code = 404
    return res

def get_no_content():
    res = jsonify(None)
    res.status_code = 204
    return res

def get_method_not_allowed():
    res = jsonify(get_falha(response_messages.METODO_NAO_PERMITIDO()))
    res.status_code = 405
    return res

def get_response_code(data, cod):
    res = jsonify(data)
    res.status_code = cod
    return res