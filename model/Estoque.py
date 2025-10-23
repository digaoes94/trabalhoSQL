class Estoque:
    def __init__(self,
                 id_produto:int=None,
                 custo_unitario:float=None,
                 quantidade:int=None,
                 total:float=None
                 ):
        self.id_produto = id_produto
        self.custo_unitario = custo_unitario
        self.quantidade = quantidade
        self.total = total

    def to_string(self) -> str:
        return f"ID Produto: {self.id_produto} | Custo Unitário: {self.custo_unitario} | Quantidade: {self.quantidade} | Total: {self.total}"
