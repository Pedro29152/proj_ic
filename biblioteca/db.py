from mysql import connector
from os import getenv
from . import response_messages

class Db:
    def __init__(self, host=None, user=None, password=None, database=None, commit_on_exit=True):
        host = host if host else getenv('MYSQL_HOST')
        user = user if user else getenv('MYSQL_USER')
        password = password if password else getenv('MYSQL_PASSWORD')
        database = database if database else getenv('MYSQL_DATABASE')

        self.__commit_on_exit = commit_on_exit

        self.__conn, self.__cursor = self.__conecta(host, user, password, database)
        self.__closed = False

    def __conecta(self, host, user, password, database):
        conn = connector.connect(
            host=host,
            user=user, 
            password=password,
            database=database
        )

        cursor = conn.cursor(dictionary=True, buffered=True)

        return conn, cursor

    def busca(self, query, *args):
        if self.__closed:
            raise ValueError(response_messages.CONEXAO_FECHADA)

        self.__cursor.execute(query, *args)

        val = self.__cursor.fetchall()

        return val

    def busca_um(self, query, *args):
        if self.__closed:
            raise ValueError(response_messages.CONEXAO_FECHADA)

        self.__cursor.execute(query, *args)

        val = self.__cursor.fetchone()

        return val

    def commit(self):
        if self.__closed:
            raise ValueError(response_messages.CONEXAO_FECHADA)
        
        self.__conn.commit()

    def gravar(self, query, *args):
        self.__cursor.execute(query, *args)

    def rollback(self):
        if self.__closed:
            raise ValueError(response_messages.CONEXAO_FECHADA)
        
        self.__conn.rollback()        

    def close(self):
        if self.__commit_on_exit:
            self.commit()
        self.__conn.close()
        self.__closed = True

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

def get_db():
    from flask import g

    if 'db' not in g:
        g.db = Db()

    return g.db
