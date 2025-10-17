from datetime import date
from model.Cliente import Cliente

class Venda:
    def __init__(self,
                 id_venda:int=None,
                 cliente:Cliente=None,
                 itens:list=None,
                 data:date=None,
                 total:float=None
                 ):
        self.id_venda = id_venda
        self.cliente = cliente  
        self.itens = itens if itens is not None else []  # Lista de produtos vendidos
        self.data = data
        self.total = total


    def to_string(self) -> str:
        nome_cliente = self.cliente.nome if self.cliente is not None else "N/A"
        valor_total_str = f"R$ {self.total:.2f}" if self.total is not None else "N/A"
        
        return f"ID: {self.id_venda} | Data: {self.data} | Cliente: {nome_cliente} | Total: {valor_total_str}"