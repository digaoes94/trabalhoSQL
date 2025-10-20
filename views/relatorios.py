from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        with open("sql/relatorioClientes.sql") as f:
            self.query_relatorioClientes = f.read()

        with open("sql/relatorioCompras.sql") as f:
            self.query_relatorioCompras = f.read()

        with open("sql/relatorioEstoque.sql") as f:
            self.query_relatorioEstoque = f.read()

        with open("sql/relatorioFornecedores.sql") as f:
            self.query_relatorioFornecedores = f.read()

        with open("sql/relatorioProdutos.sql") as f:
            self.query_relatorioProdutos = f.read()

        with open("sql/relatorioVendas.sql") as f:
            self.query_relatorioVendas = f.read()
    
    def get_relatorioClientes(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorioClientes))
        input("Pressione Enter para sair do relatório de CLientes")

    def get_relatorioCompras(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorioCompras))
        input("Pressione Enter para sair do relatório de Compras")

    def get_relatorioEstoque(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorioEstoque))
        input("Pressione Enter para sair do relatório do Estoque")

    def get_relatorioFornecedores(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorioFornecedores))
        input("Pressione Enter para sair do relatório de Fornecedores")

    def get_relatorioProdutos(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorioProdutos))
        input("Pressione Enter para sair do relatório de Produtos")

    def get_relatorioVendas(self):
        oracle = OracleQueries()
        oracle.connect()
        print(oracle.sqlToDataFrame(self.query_relatorioVendas))
        input("Pressione Enter para sair do relatório de Vendas")