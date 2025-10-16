class Produto:
    def __init__(self,
                 id_produto:int=None,
                 nome:str=None,
                 preco:float=None,
                 descricao:str=None
                 ):
        self.id_produto = id_produto
        self.nome = nome        
        self.preco = preco
        self.descricao = descricao

    def to_string(self) -> str:
        return f"ID: {self.id_produto} | Nome: {self.nome} | Preço: {self.preco} | Descrição: {self.descricao}"