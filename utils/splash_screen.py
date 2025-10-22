from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_produtos = config.QUERY_COUNT.format(tabela="produtos")
        self.qry_total_clientes = config.QUERY_COUNT.format(tabela="clientes")
        self.qry_total_fornecedores = config.QUERY_COUNT.format(tabela="fornecedores")
        self.qry_total_vendas = config.QUERY_COUNT.format(tabela="vendas")
        self.qry_total_itens_venda = config.QUERY_COUNT.format(tabela="item_venda")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = "GABRIELY, GUILHERME, LUIZ, RICARDO E RODRIGO"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2022/2"

    def get_total_produtos(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_produtos)["total_produtos"].values[0]

    def get_total_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_clientes)["total_clientes"].values[0]

    def get_total_fornecedores(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_fornecedores)["total_fornecedores"].values[0]

    def get_total_vendas(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_vendas)["total_vendas"].values[0]

    def get_total_itens_venda(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_itens_venda)["total_item_venda"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE VENDAS                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - PRODUTOS:         {str(self.get_total_produtos()).rjust(5)}
        #      2 - CLIENTES:         {str(self.get_total_clientes()).rjust(5)}
        #      3 - FORNECEDORES:     {str(self.get_total_fornecedores()).rjust(5)}
        #      4 - VENDAS:           {str(self.get_total_vendas()).rjust(5)}
        #      5 - ITENS DE VENDA:   {str(self.get_total_itens_venda()).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  ALTERADO POR: GABRIELY, GUILHERME, LUIZ, RICARDO E RODRIGO
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """