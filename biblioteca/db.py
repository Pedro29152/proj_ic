from mysql import connector
from os import getenv
from . import response_messages

class Db:
    def __init__(self, host=None, user=None, password=None, database=None):
        self.host = host if host else getenv('MYSQL_HOST')
        self.user = user if user else getenv('MYSQL_USER')
        self.password = password if password else getenv('MYSQL_PASSWORD')
        self.database = database if database else getenv('MYSQL_DATABASE')

        self.__conn, self.__cursor = self.__conecta()
        self.__closed = False

    def __conecta(self):
        conn = connector.connect(
            host=self.host,
            user=self.user, 
            password=self.password,
            database=self.database
        )

        cursor = conn.cursor(dictionary=True)

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

    def gravar_autocommit(self, query, *args):
        self.gravar(query, *args)
        self.__conn.commit()

    def rollback(self):
        if self.__closed:
            raise ValueError(response_messages.CONEXAO_FECHADA)
        
        self.__conn.rollback()        

    def close(self):
        self.__conn.commit()
        self.__conn.close()
        self.__closed = True

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
