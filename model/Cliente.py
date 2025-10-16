from model.Pessoa import Pessoa
from model.Endereco import Endereco

class Cliente(Pessoa): # Sintaxe da Herança
    def __init__(self, 
                 id_cliente:int=None,
                 cpf:str=None,
                 nome:str=None,
                 # Parâmetros que serão passados para a classe mãe (Pessoa)
                 endereco:Endereco=None, 
                 email:str=None,
                 telefones:list=None
                ):
        
        # Chama o construtor da classe mãe (Pessoa) para inicializar os atributos herdados
        super().__init__(endereco, email, telefones)
    
        # Inicializa os atributos específicos de Cliente
        self.id_cliente = id_cliente
        self.cpf = cpf
        self.nome = nome

    def to_string(self) -> str:
        pessoa_str = super().to_string()
        return f"ID: {self.id_cliente} | Nome: {self.nome} | CPF: {self.cpf} | {pessoa_str}"