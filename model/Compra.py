from datetime import date
from model.Fornecedor import Fornecedor

class Compra:
    def __init__(self,
                 id_compra:int=None,
                 fornecedor:Fornecedor=None,
                 itens:list=None,
                 data:date=None,
                 total:float=None
                 ):
        self.id_compra = id_compra
        self.fornecedor = fornecedor
        self.itens = itens if itens is not None else []  # Lista de produtos comprados
        self.data = data
        self.total = total

    def to_string(self) -> str:
        nome_fornecedor = self.fornecedor.nome_fantasia if self.fornecedor is not None else "N/A"
        valor_total_str = f"R$ {self.total:.2f}" if self.total is not None else "N/A"
        qtd_itens = len(self.itens) if self.itens is not None else 0

        return f"ID: {self.id_compra} | Data: {self.data} | Fornecedor: {nome_fornecedor} | Itens: {qtd_itens} | Total: {valor_total_str}"