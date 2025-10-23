import json
import cx_Oracle
from pandas import DataFrame
import os

class OracleQueries:

    def __init__(self, can_write:bool=False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1' # Service Name correto para Oracle 21c XE (gvenzl)
        self.sid = 'XE'              # SID (provavelmente não será usado, mas mantido)

        # --- MODIFICAÇÃO ---
        # Define o usuário e a senha diretamente para o container
        #self.user = "SYSTEM"
        #self.passwd = "oracle"
        
        # O código original que lia de um arquivo foi comentado/removido:
        auth_path = os.path.join(os.path.dirname(__file__), "passphrase", "authentication.oracle")
        with open(auth_path, "r") as f:
            self.user, self.passwd = f.read().split(',')            
        # --- FIM DA MODIFICAÇÃO ---

    def __del__(self):
        # Adicionado verificação se 'self.cur' existe antes de fechar
        if hasattr(self, 'cur') and self.cur:
            self.close()

    def connectionString(self, in_container:bool=True):
        '''
        Cria uma string de conexão utilizando os parâmetros necessários
        '''
        if not in_container:
            # Conexão via SID (comum em instalações locais antigas)
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                port=self.port,
                                                sid=self.sid
                                                )
        elif in_container:
            # Conexão via Service Name (padrão para containers Docker/Oracle 21c)
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                port=self.port,
                                                service_name=self.service_name
                                                )
        return string_connection

    def connect(self):
        '''
        Realiza a conexão com o banco de dados Oracle
        '''

        # Usa in_container=True por padrão, que usará o self.service_name ('XEPDB1')
        self.conn = cx_Oracle.connect(user=self.user,
                                      password=self.passwd,
                                      dsn=self.connectionString() 
                                     )
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query:str, params:dict=None) -> DataFrame:
        '''
        Executa uma query e retorna os resultados como DataFrame
        '''
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            rows = self.cur.fetchall()
            if not self.cur.description:
                return DataFrame()
            return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])
        except Exception as e:
            print(f"❌ Erro ao executar query: {e}")
            raise

    def sqlToMatrix(self, query:str, params:dict=None) -> tuple:
        '''
        Executa uma query e retorna matriz e nomes das colunas
        '''
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            rows = self.cur.fetchall()
            matrix = [list(row) for row in rows]
            columns = [col[0].lower() for col in self.cur.description] if self.cur.description else []
            return matrix, columns
        except Exception as e:
            print(f"❌ Erro ao executar query: {e}")
            raise

    def sqlToJson(self, query:str, params:dict=None):
        '''
        Executa uma query e retorna os resultados como JSON
        '''
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            columns = [col[0].lower() for col in self.cur.description] if self.cur.description else []
            self.cur.rowfactory = lambda *args: dict(zip(columns, args))
            rows = self.cur.fetchall()
            return json.dumps(rows, default=str)
        except Exception as e:
            print(f"❌ Erro ao executar query: {e}")
            raise

    def write(self, query:str, params:dict=None):
        '''
        Executa uma query de escrita (INSERT, UPDATE, DELETE)
        '''
        if not self.can_write:
            raise Exception('Can\'t write using this connection')

        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Erro ao executar write: {e}")
            raise

    def close(self):
        if self.cur:
            self.cur.close()

    def executeDDL(self, query:str, params:dict=None):
        '''
        Executa um comando DDL (CREATE, DROP, ALTER)
        '''
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
        except Exception as e:
            print(f"❌ Erro ao executar DDL: {e}")
            raise