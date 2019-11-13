from flask                      import jsonify, session
from functools                  import wraps
from biblioteca.controllers     import usuario_control
from biblioteca.util            import util, json_res

def login_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado():
            return f(*args, **kwargs)
        return util.response_ext(
            jsonify(
                json_res.get_negado('Voce precisa estar logado antes de acessar esta página')
            )
        )

    return wrap

def admin_reqired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado():
            if session['nivel_acesso'] > 2:
                return f(*args, **kwargs)
                
            return util.response_ext(
                jsonify(
                    json_res.get_negado('Seu nivel de acesso nao permite acesso a esta pagina')
                )
            )
        return util.response_ext(
            jsonify(
                json_res.get_negado('Voce precisa estar logado antes de acessar esta página')
            )
        )

    return wrap

def user_admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if usuario_control.logado():
            if usuario_control.is_user(kwargs['codUsuario']) or session['nivel_acesso'] > 2:
                return f(*args, **kwargs)
            return util.response_ext(
                jsonify(
                     json_res.get_negado('Voce nao tem permissao para efetuar esta operacao')
                )
            )
        return util.response_ext(
            jsonify(
                json_res.get_negado('Voce precisa estar logado antes de acessar esta página')
            )
        )
        
        

    return wrap

def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not usuario_control.logado():
            return f(*args, **kwargs)
        return util.response_ext(
            jsonify(
                json_res.get_negado('Voce ja esta logado em uma conta, deslogue-se para poder acessar esta pagina')
            )
        )
    
    return wrap