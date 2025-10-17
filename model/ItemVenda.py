from model.Produto import Produto
from model.Venda import Venda

class ItemVenda: 
    def __init__(self,
                 produto: Produto=None,
                 quantidade: int=None,
                 preco_unitario: float=None,
                 subtotal: float=None,
                 venda: Venda=None
                 ):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal
        self.venda = venda

    def to_string(self) -> str:
       nome_produto = self.produto.nome if self.produto is not None else "N/A"
       preco_unitario_str = f"R$ {self.preco_unitario:.2f}" if self.preco_unitario is not None else "N/A"
       subtotal_str = f"R$ {self.subtotal:.2f}" if self.subtotal is not None else "N/A"

       return f"Produto: {nome_produto} | Qtd: {self.quantidade} | Preço Unit: {preco_unitario_str} | Subtotal: {subtotal_str}"