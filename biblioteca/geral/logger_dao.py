from biblioteca.db import Db

def logger_gravar(url, request_datetime, method, status_code, codUsuario=None, ip_address=None, request_data=None, response_data=None, info=None, ):
    with Db() as db:
        query = '''
            insert into logger(rotaCompleta, requestDate, method, statusCode, ipAddress, info, requestData, responseData, codUsuario)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        db.gravar_autocommit(query, (url, request_datetime, method, status_code, ip_address, info, request_data, response_data, codUsuario))
