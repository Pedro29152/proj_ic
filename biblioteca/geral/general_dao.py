
from biblioteca.extensions import (
    separate_camel_case as scc
)

def get_enum_obj(intenum, separate_camel_case=True):
    obj = {}
    for i, tipo in enumerate(intenum):
        if separate_camel_case:
            obj[tipo.value] = scc(tipo.name)
        else:
            obj[tipo.value] = tipo.name
    return obj
    
