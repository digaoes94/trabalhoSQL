from model.Endereco import Endereco

class Fornecedor:
    def __init__(self, 
                 cnpj:str,
                 razaoSocial:str,
                 nomeFantasia:str,
                 endereco:Endereco, 
                 email:str,
                 telefone:list
                ):
        self.cnpj = cnpj
        self.razaoSocial = razaoSocial
        self.nomeFantasia = nomeFantasia
        self.endereco = endereco
        self.email = email
        self.telefone = telefone

    def getCNPJ(self) -> str: return self.cnpj
    def getRazaoSocial(self) -> str: return self.razaoSocial
    def getNomeFantasia(self) -> str: return self.nomeFantasia
    def getEndereco(self) -> Endereco: return self.endereco
    def getEmail(self) -> str: return self.email
    def getTelefone(self) -> str: return self.telefone

    def setCNPJ(self, cnpj:str): self.cnpj = cnpj
    def setRazaoSocial(self, razaoSocial:str): self.razaoSocial = razaoSocial
    def setNomeFantasia(self, nomeFantasia:str): self.nomeFantasia = nomeFantasia
    def setEndereco(self, endereco:Endereco): self.endereco = endereco
    def setEmail(self, email:str): self.email = email
    def setTelefone(self, telefone:str): self.telefone = telefone

    def to_string(self) -> str:
        return f"ID: {self.id_fornecedor} | Nome Fantasia: {self.nomeFantasia} | CNPJ: {self.cnpj}"