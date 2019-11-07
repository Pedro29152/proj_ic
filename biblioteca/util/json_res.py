def get_ok(message='OK'):
    return {
        'status':'OK',
        'message': message
    }

def get_erro(message='erro'):
    return {
        'status':'OK',
        'message': message
    }
    
def get_falha(message='falha'):
    return {
        'status':'falha',
        'message': message
    }

def get_negado(message='negado'):
    return {
        'status':'negado',
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