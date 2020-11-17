from mysql import connector
from os import getenv

def __conecta():
    conn = connector.connect(
        user=getenv('MYSQL_USER'), 
        password=getenv('MYSQL_PASSWORD'),
        database=getenv('MYSQL_DATABASE')
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


def __conecta_information_schema():
    conn = connector.connect(
        user=getenv('MYSQL_USER'), 
        password=getenv('MYSQL_PASSWORD'),
        database='information_schema'
    )

    cursor = conn.cursor(dictionary=True)

    return conn, cursor

def bd_busca_information_schema(query, *args):
    conn, cursor = __conecta_information_schema()
    try:
        cursor.execute(query, *args)

        val = cursor.fetchall()
    finally:
        conn.close()

    return val

def bd_busca_um_information_schema(query, *args):
    conn, cursor = __conecta_information_schema()
    try:
        cursor.execute(query, *args)

        val = cursor.fetchone()

    finally:
        conn.close()

    return val
