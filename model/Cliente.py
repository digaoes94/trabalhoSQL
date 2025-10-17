from model.Endereco import Endereco

class Cliente:
    def __init__(self, 
                 cpf:str,
                 nome:str,
                 endereco:Endereco, 
                 email:str,
                 telefone:list
                ):
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.email = email
        self.telefone = telefone

    def getCPF(self) -> str: return self.cpf
    def getNome(self) -> str: return self.nome
    def getEndereco(self) -> Endereco: return self.endereco
    def getEmail(self) -> str: return self.email
    def getTelefone(self) -> str: return self.telefone

    def setCPF(self, cpf:str): self.cpf = cpf
    def setNome(self, nome:str): self.nome = nome
    def setEndereco(self, endereco:Endereco): self.endereco = endereco
    def setEmail(self, email:str): self.email = email
    def setTelefone(self, telefone:str): self.telefone = telefone

    def to_string(self) -> str:
        pessoa_str = super().to_string()
        return f"ID: {self.id_cliente} | Nome: {self.nome} | CPF: {self.cpf} | {pessoa_str}"