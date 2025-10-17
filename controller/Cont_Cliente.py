from model.Cliente import Cliente
from conexion.oracle_queries import OracleQueries

class Cont_Cliente:
    def __init__(self):
        pass

    def pesqCliente(self, oracle:OracleQueries, cpf:str=None) -> bool:
        #df = DataFrame
        df_cliente = oracle.sqlToDataFrame(f"SELECT cpf, nome FROM clientes WHERE cpf = {cpf}")
        return df_cliente.empty
    
    def novoCliente(self) -> Cliente:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = input("Informe CPF do Cliente: ")

        if not self.pesqCliente(oracle, cpf):
            print(f"Cliente de CPF {cpf} já existe.")
        else:
            nome = input("Nome do CLiente: ")
            