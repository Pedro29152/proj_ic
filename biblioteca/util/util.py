from flask import make_response

def response_ext(val):
    res = make_response(val)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res