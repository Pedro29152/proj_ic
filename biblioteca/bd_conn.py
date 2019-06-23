from mysql import connector
from flask import flash

def conecta():
    conn = connector.connect(
        user='root', 
        password='LabRobotica123#@',
        host='127.0.0.1',
        port='3306',
        database='proj_ic')

    cursor = conn.cursor(dictionary=True)

    return conn, cursor

def bd_busca(query, busca):
    try:
        conn, cursor = conecta()
        cursor.execute(
            query,
            [busca,]
        )

        val = cursor.fetchall()

    finally:
        conn.close()

    return val

def bd_gravar(query, *args):
    try:
        conn, cursor = conecta()
        cursor.execute(query, *args)
        conn.commit()
    finally:
        conn.close()
