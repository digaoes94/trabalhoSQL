from model.Produto import Produto
from conexion.oracle_queries import OracleQueries

# O uso de pandas é implícito no ambiente do professor
# para manipulação dos DataFrames retornados por sqlToDataFrame.
class Cont_Produto:
    def __init__(self):
        pass
        
    def _recupera_produto(self, oracle: OracleQueries, id_produto: int = None) -> Produto:
        """ 
        Método interno para buscar os dados de Produto no BD e instanciar o objeto Produto completo.
        Retorna o objeto Produto ou None se não encontrado.
        """
        if id_produto is None:
            return None
            
        query = f"SELECT id_produto, nome, preco_unitario, descricao FROM produtos WHERE id_produto = {id_produto}"
        
        df_produto = oracle.sqlToDataFrame(query)

        if df_produto.empty:
            return None
        else:
            produto_data = df_produto.iloc[0]
            
            # Cria o objeto Produto
            produto = Produto(
                id_produto=int(produto_data["id_produto"]),
                nome=produto_data["nome"],
                # Garante que preco é float
                preco=float(produto_data["preco_unitario"]),
                descricao=produto_data["descricao"]
            )
            return produto
            
    def verifica_existencia_produto(self, oracle:OracleQueries, id_produto:int=None) -> bool:
        """
        Verifica se o Produto *NÃO* existe no BD (DataFrame vazio).
        (Retorna True se o produto *pode* ser inserido)
        """
        query = f"SELECT id_produto FROM produtos WHERE id_produto = {id_produto}"
        df_produto = oracle.sqlToDataFrame(query)
        return df_produto.empty

    # ---------------------------------------------------------------------------
    # MÉTODOS CRUD SOLICITADOS
    # ---------------------------------------------------------------------------
    
    def pesquisarProduto(self) -> Produto:
        oracle = OracleQueries(can_write=False)
        oracle.connect()

        id_produto = input("Informe o ID do Produto que deseja pesquisar: ")
        
        # Tenta converter para int para usar na query SQL
        try:
            id_produto = int(id_produto)
        except ValueError:
            print("ID do produto inválido.")
            return None
            
        produto = self._recupera_produto(oracle, id_produto)

        if produto is None:
            print(f"O Produto de ID {id_produto} não existe.")
        else:
            print("\nProduto Encontrado:")
            print(produto.to_string())
            
        return produto

    def novoProduto(self) -> Produto:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita o ID (Assumindo que o usuário insere, ou o DB gera)
        id_produto = input("ID do Produto (Novo): ")

        # Tenta converter para int
        try:
            id_produto = int(id_produto)
        except ValueError:
            print("ID do produto inválido.")
            return None

        # verifica_existencia_produto retorna True se o produto *NÃO* existe
        if self.verifica_existencia_produto(oracle, id_produto):
            
            # Coleta dados do Produto
            print("--- Dados do Produto ---")
            nome = input("Nome do Produto: ")
            
            # Tratamento para preço (Double/Float)
            preco = input("Preço Unitário: ")
            try:
                preco_float = float(preco)
            except ValueError:
                print("Preço inválido. Cancelando operação.")
                return None
                
            descricao = input("Descrição: ")
            
            # Insere e persiste o novo Produto
            sql_produto = f"""
                INSERT INTO produtos (id_produto, nome, preco_unitario, descricao) 
                VALUES ({id_produto}, '{nome}', {preco_float}, '{descricao}')
            """
            oracle.write(sql_produto)

            # Recupera o objeto Produto completo para retorno
            novo_produto = self._recupera_produto(oracle, id_produto)
            
            # Exibe os atributos do novo produto
            print("\nProduto cadastrado com sucesso!")
            print(novo_produto.to_string())
            return novo_produto
        else:
            print(f"O Produto de ID {id_produto} já está cadastrado.")
            return None

    def atualizarProduto(self) -> Produto:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID do Produto a ser alterado
        id_produto = input("ID do Produto que deseja alterar: ")

        # Tenta converter para int
        try:
            id_produto = int(id_produto)
        except ValueError:
            print("ID do produto inválido.")
            return None

        # Verifica se o produto existe na base de dados (se retorna True, NÃO existe)
        if self.verifica_existencia_produto(oracle, id_produto):
            print(f"O Produto de ID {id_produto} não existe.")
            return None
        else:
            # Recupera o produto existente para preencher os valores antigos
            produto_existente = self._recupera_produto(oracle, id_produto)
            print(f"\nDados atuais do Produto: {produto_existente.to_string()}")
            
            # Coleta novos dados do Produto
            novo_nome = input(f"Novo nome (Atual: {produto_existente.nome}): ") or produto_existente.nome
            
            novo_preco_str = input(f"Novo Preço Unitário (Atual: {produto_existente.preco}): ")
            novo_preco = float(novo_preco_str) if novo_preco_str else produto_existente.preco
            
            nova_descricao = input(f"Nova Descrição (Atual: {produto_existente.descricao}): ") or produto_existente.descricao
            
            # Atualiza no BD (PRODUTOS)
            sql_update_produto = f"""
                UPDATE produtos 
                SET nome = '{novo_nome}', preco_unitario = {novo_preco}, descricao = '{nova_descricao}' 
                WHERE id_produto = {id_produto}
            """
            oracle.write(sql_update_produto)
            
            # Recupera o produto atualizado
            produto_atualizado = self._recupera_produto(oracle, id_produto)
            
            print("\nProduto atualizado com sucesso!")
            print(produto_atualizado.to_string())
            return produto_atualizado

    def deletarProduto(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID do Produto a ser excluído
        id_produto = input("ID do Produto que irá excluir: ")        

        # Tenta converter para int
        try:
            id_produto = int(id_produto)
        except ValueError:
            print("ID do produto inválido.")
            return

        # Verifica se o produto existe na base de dados
        if self.verifica_existencia_produto(oracle, id_produto):            
            print(f"O Produto de ID {id_produto} não existe.")
        else:
            # Recupera os dados do produto antes de excluir para exibição
            produto_excluido = self._recupera_produto(oracle, id_produto)
            
            # Deleta Produto
            sql_del_produto = f"DELETE FROM produtos WHERE id_produto = {id_produto}"
            oracle.write(sql_del_produto)
            
            # Exibe os atributos do produto excluído
            print("Produto Removido com Sucesso!")
            print(produto_excluido.to_string())

