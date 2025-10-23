###########################################################################
# Author: Howard Roatti
# Adapted: Gabriely, Guilherme, Luiz, Ricardo, Rodrigo
# Created: 02/09/2022
# Last Update: 22/10/2025
#
# Essa classe auxilia na conexão com o Banco de Dados Oracle
# Documentação base: https://python-oracledb.readthedocs.io/
###########################################################################
import json
import oracledb
from pandas import DataFrame

class OracleQueries:

    def __init__(self, can_write:bool=False):
        self.can_write = can_write
        self.host = "host.docker.internal"
        self.port = 1521
        self.service_name = 'FREEPBD1'

        with open("conexion/passphrase/authentication.oracle", "r") as f:
            self.user, self.passwd = f.read().split(',')

    def __del__(self):
        if hasattr(self, 'cur') and self.cur:
            self.close()

    def connect(self):
        '''
        Esse método realiza a conexão com o banco de dados Oracle
        '''
        try:
            dsn = f"{self.host}:{self.port}/{self.service_name}"
            self.conn = oracledb.connect(user=self.user,
                                         password=self.passwd,
                                         dsn=dsn
                                        )
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as e:
            print(f"Erro ao conectar no Oracle: {e}")
            # Exit the program if connection fails
            exit()


    def sqlToDataFrame(self, query:str) -> DataFrame:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: um DataFrame da biblioteca Pandas
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])

    def sqlToMatrix(self, query:str) -> tuple:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: uma matriz (lista de listas), uma lista com os nomes das colunas(atributos) da(s) tabela(s)
        '''
        self.cur.execute(query)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query:str):
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        return: um objeto json
        '''
        self.cur.execute(query)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query:str):
        if not self.can_write:
            raise Exception('Can\'t write using this connection')

        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()

    def executeDDL(self, query:str):
        '''
        Esse método irá executar o comando DDL enviado no atributo query
        Parameters:
        - query: consulta utilizada para comandos DDL
        '''
        self.cur.execute(query)
