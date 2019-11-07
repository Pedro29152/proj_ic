def get_ok(message='OK'):
    return {
        'cod_s': 1,
        'status':'OK',
        'message': message
    }

def get_erro(message='erro'):
    return {
        'cod_s': 0,
        'status':'erro',
        'message': message
    }
    
def get_falha(message='falha'):
    return {
        'cod_s': 0,
        'status':'falha',
        'message': message
    }

def get_negado(message='negado'):
    return {
        'cod_s': 0,
        'status':'negado',
        'message': message
    }


def get_data(data):
    return {
        'cod_s': 1,
        'status': 'OK',
        'data': data
    }

def get_count(count):
    return {
        'cod_s': 1,
        'status': 'OK',
        'count': count
    }