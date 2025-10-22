from model.Endereco import Endereco

class Cliente:
    def __init__(self, 
                 id_cliente:int=None,
                 cpf:str=None,
                 nome:str=None,
                 endereco:Endereco=None, 
                 email:str=None,
                 telefone:list=None
                ):
        self.id_cliente = id_cliente
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.email = email
        self.telefone = telefone if telefone is not None else []

    def getIDCliente(self) -> int: return self.id_cliente
    def getCPF(self) -> str: return self.cpf
    def getNome(self) -> str: return self.nome
    def getEndereco(self) -> Endereco: return self.endereco
    def getEmail(self) -> str: return self.email
    def getTelefone(self) -> list: return self.telefone

    def setIDCliente(self, id_cliente:int): self.id_cliente = id_cliente
    def setCPF(self, cpf:str): self.cpf = cpf
    def setNome(self, nome:str): self.nome = nome
    def setEndereco(self, endereco:Endereco): self.endereco = endereco
    def setEmail(self, email:str): self.email = email
    def setTelefone(self, telefone:list): self.telefone = telefone

    def to_string(self) -> str:
        return f"ID: {self.id_cliente} | Nome: {self.nome} | CPF: {self.cpf} | Email: {self.email} | Telefone: {', '.join(self.telefone)}"