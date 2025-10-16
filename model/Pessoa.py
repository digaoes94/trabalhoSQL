from model.Endereco import Endereco

class Pessoa:
    def __init__(self, 
                 endereco:Endereco=None, 
                 email:str=None,
                 telefones:list=None
                ):
        self.endereco = endereco
        self.email = email
        self.telefones = telefones if telefones is not None else []

    def to_string(self) -> str:
        telefones_str = ", ".join(self.telefones)
       
        return f"Email: {self.email} | Telefones: {telefones_str} | Endereço: {self.endereco.to_string()}" 