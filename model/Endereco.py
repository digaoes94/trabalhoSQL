class Endereco:
    def __init__(self, 
                 cep:str=None,
                 logradouro:str=None,
                 numero:int=None,
                 complemento:str=None, 
                 bairro:str=None,
                 cidade:str=None,
                 estado:str=None
                ):
      
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

    def to_string(self) -> str:
        
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado} - CEP: {self.cep}"