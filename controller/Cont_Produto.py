from model.Produto import Produto
from conexion.oracle_queries import OracleQueries

class Cont_Produto: 
    def __init__(self):
        pass

    def pesqProduto(self, oracle:OracleQueries, id_produto:int=None) -> bool:
        #df = DataFrame
        df_produto = oracle.sqlToDataFrame(f"SELECT id_produto, nome FROM produtos WHERE id_produto = {id_produto}")
        return df_produto.empty
    
    def novoProduto(self) -> Produto:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        id_produto = int(input("Informe ID do Produto: "))

        if not self.pesqProduto(oracle, id_produto):
            print(f"Produto de ID {id_produto} já existe.")
        else:
            nome = input("Nome do Produto: ")
            preco = float(input("Preço do Produto: "))
            descricao = input("Descrição do Produto: ")

            produto = Produto(
                id_produto=id_produto,
                nome=nome,
                preco=preco,
                descricao=descricao
            )

            oracle.executeSQL(
                f"INSERT INTO produtos (id_produto, nome, preco, descricao) VALUES ({produto.getIdProduto()}, '{produto.getNome()}', {produto.getPreco()}, '{produto.getDescricao()}')"
            )

            print(f"Produto {produto.getNome()} cadastrado com sucesso!")

            return produto
        
    def atualizarProduto(self, id_produto:int) -> None: 
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        if self.pesqProduto(oracle, id_produto):
            print(f"Produto de ID {id_produto} não existe.")
        else:
            nome = input("Novo Nome do Produto: ")
            preco = float(input("Novo Preço do Produto: "))
            descricao = input("Nova Descrição do Produto: ")

            oracle.executeSQL(
                f"UPDATE produtos SET nome = '{nome}', preco = {preco}, descricao = '{descricao}' WHERE id_produto = {id_produto}"
            )

            print(f"Produto de ID {id_produto} atualizado com sucesso!")
        