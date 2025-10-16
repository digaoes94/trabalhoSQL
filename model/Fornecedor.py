from model.Pessoa import Pessoa
from model.Endereco import Endereco

class Fornecedor(Pessoa):
    def __init__(self, 
                 id_fornecedor:int=None,
                 cnpj:str=None,
                 razao_social:str=None,
                 nome_fantasia:str=None,
                 # Parâmetros herdados de Pessoa
                 endereco:Endereco=None, 
                 email:str=None,
                 telefones:list=None
                ):
        # Chama o construtor da classe mãe (Pessoa)
        super().__init__(endereco, email, telephones)
        
        # Inicializa os atributos específicos de Fornecedor
        self.id_fornecedor = id_fornecedor
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia

    def to_string(self) -> str:
        return f"ID: {self.id_fornecedor} | Nome Fantasia: {self.nome_fantasia} | CNPJ: {self.cnpj}"