
def is_cod_valido(codUsuario):
    try:
        int(codUsuario)
        return True
    except ValueError:
        return False