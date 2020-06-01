from flask import jsonify

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

def get_count(count):
    return {
        'status': 'OK',
        'count': count
    }


def get_unauthorized(data):
    res = jsonify(get_erro(data))
    res.status_code = 401
    return res

def get_bad_request(data):
    res = jsonify(get_negado(data))
    res.status_code = 400
    return res

def get_response_code(data, cod):
    res = jsonify(data)
    res.status_code = cod
    return res