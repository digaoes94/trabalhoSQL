from model.Endereco import Endereco

class Fornecedor:
    def __init__(self, 
                 id_fornecedor:int=None,
                 cnpj:str=None,
                 razaoSocial:str=None,
                 nomeFantasia:str=None,
                 endereco:Endereco=None, 
                 email:str=None,
                 telefone:list=None
                ):
        self.id_fornecedor = id_fornecedor
        self.cnpj = cnpj
        self.razaoSocial = razaoSocial
        self.nomeFantasia = nomeFantasia
        self.endereco = endereco
        self.email = email
        self.telefone = telefone if telefone is not None else []

    def getIDFornecedor(self) -> int: return self.id_fornecedor
    def getCNPJ(self) -> str: return self.cnpj
    def getRazaoSocial(self) -> str: return self.razaoSocial
    def getNomeFantasia(self) -> str: return self.nomeFantasia
    def getEndereco(self) -> Endereco: return self.endereco
    def getEmail(self) -> str: return self.email
    def getTelefone(self) -> list: return self.telefone

    def setIDFornecedor(self, id_fornecedor:int): self.id_fornecedor = id_fornecedor
    def setCNPJ(self, cnpj:str): self.cnpj = cnpj
    def setRazaoSocial(self, razaoSocial:str): self.razaoSocial = razaoSocial
    def setNomeFantasia(self, nomeFantasia:str): self.nomeFantasia = nomeFantasia
    def setEndereco(self, endereco:Endereco): self.endereco = endereco
    def setEmail(self, email:str): self.email = email
    def setTelefone(self, telefone:list): self.telefone = telefone

    def to_string(self) -> str:
        return f"ID: {self.id_fornecedor} | Nome Fantasia: {self.nomeFantasia} | CNPJ: {self.cnpj} | Email: {self.email} | Telefone: {', '.join(self.telefone)}"