from mysql import connector
from flask import flash

def __conecta():
    conn = connector.connect(
        user='root', 
        password= '1234',
        database='proj_ic'
    )

    cursor = conn.cursor(dictionary=True)

    return conn, cursor

def bd_busca(query, *args):
    conn, cursor = __conecta()
    try:
        cursor.execute(query, *args)

        val = cursor.fetchall()
    finally:
        conn.close()

    return val

def bd_busca_um(query, *args):
    conn, cursor = __conecta()
    try:
        cursor.execute(query, *args)

        val = cursor.fetchone()

    finally:
        conn.close()

    return val

def bd_gravar(query, *args):
    conn, cursor = __conecta()
    try:
        cursor.execute(query, *args)
        conn.commit()
    
    finally:
        conn.close()
