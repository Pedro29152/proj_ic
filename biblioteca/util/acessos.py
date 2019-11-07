from flask                      import jsonify, session
from functools                  import wraps
from biblioteca.controllers     import usuario_control
import util, json_res

def login_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado(session):
            return f(*args, **kwargs)
        else:
            return util.response_ext(
                jsonify(
                    json_res.get_negado('Voce precisa estar logado antes de acessar esta página')
                )
            )

    return wrap

def admin_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado(session):
            if session['nivel_acesso'] > 1:
                return f(*args, **kwargs)
            else:
                return util.response_ext(
                    jsonify(
                        json_res.get_negado('Seu nivel de acesso nao permite acesso a esta pagina')
                    )
                )
        else:
            return util.response_ext(
                jsonify(
                    json_res.get_negado('Voce precisa estar logado antes de acessar esta página')
                )
            )

    return wrap

def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            return util.response_ext(
                jsonify(
                    json_res.get_negado('Voce ja esta logado em uma conta, deslogue-se para poder acessar esta pagina')
                )
            )
    
    return wrap
