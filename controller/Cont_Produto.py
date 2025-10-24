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

        # Pergunta se quer gerar ID automaticamente ou inserir manualmente
        print("\n--- ID do Produto ---")
        print("1 - Gerar ID automaticamente")
        print("2 - Inserir ID manualmente")
        opcao_id = input("Escolha (1 ou 2): ")

        id_produto = None
        usar_sequence = False

        if opcao_id == '1':
            # Usar sequence automática
            usar_sequence = True
        elif opcao_id == '2':
            # Inserir ID manualmente
            id_entrada = input("ID do Produto: ")
            try:
                id_produto = int(id_entrada)
            except ValueError:
                print("❌ ID do produto inválido.")
                return None

            # Verifica se o ID já existe
            if not self.verifica_existencia_produto(oracle, id_produto):
                print(f"❌ O Produto de ID {id_produto} já está cadastrado.")
                return None
        else:
            print("❌ Opção inválida.")
            return None

        # Coleta dados do Produto
        print("--- Dados do Produto ---")
        nome = input("Nome do Produto: ")

        # Tratamento para preço (Double/Float)
        preco = input("Preço Unitário: ")
        try:
            preco_float = float(preco)
        except ValueError:
            print("❌ Preço inválido. Cancelando operação.")
            return None

        descricao = input("Descrição: ")

        # Insere o novo Produto
        if usar_sequence:
            # Gera ID automaticamente
            sql_produto = f"""
                INSERT INTO produtos (id_produto, nome, preco_unitario, descricao)
                VALUES (produtos_id_seq.NEXTVAL, '{nome}', {preco_float}, '{descricao}')
            """
            oracle.write(sql_produto)

            # Recupera o ID gerado automaticamente
            query_id_produto = "SELECT produtos_id_seq.CURRVAL AS id_produto FROM DUAL"
            df_id_produto = oracle.sqlToDataFrame(query_id_produto)
            id_produto_gerado = int(df_id_produto.id_produto.values[0])
        else:
            # Usa o ID informado manualmente
            sql_produto = f"""
                INSERT INTO produtos (id_produto, nome, preco_unitario, descricao)
                VALUES ({id_produto}, '{nome}', {preco_float}, '{descricao}')
            """
            oracle.write(sql_produto)
            id_produto_gerado = id_produto

        # Recupera o objeto Produto completo para retorno
        novo_produto = self._recupera_produto(oracle, id_produto_gerado)

        # Exibe os atributos do novo produto
        print("\n✅ Produto cadastrado com sucesso!")
        print(novo_produto.to_string())
        return novo_produto

    def atualizarProduto(self) -> Produto:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Loop para atualizar múltiplos produtos
        while True:
            # Lista produtos cadastrados
            query_produtos = "SELECT id_produto, nome FROM produtos ORDER BY nome"
            df_produtos = oracle.sqlToDataFrame(query_produtos)

            if df_produtos.empty:
                print("Nenhum produto cadastrado.")
                return None

            print("\n--- Produtos Cadastrados ---")
            for idx, row in df_produtos.iterrows():
                print(f"{idx + 1}. ID: {int(row['id_produto'])} | Nome: {row['nome']}")

            # Solicita ao usuário qual produto deseja alterar
            selecao = input("\nDigite o número do produto para atualizar (ou 0 para voltar): ")

            if selecao == '0':
                break

            try:
                idx_selecionado = int(selecao) - 1
                if idx_selecionado < 0 or idx_selecionado >= len(df_produtos):
                    print("❌ Opção inválida!")
                    continue
            except ValueError:
                print("❌ Entrada inválida!")
                continue

            produto_selecionado = df_produtos.iloc[idx_selecionado]
            id_produto = int(produto_selecionado['id_produto'])

            # Verifica se o produto existe na base de dados (se retorna True, NÃO existe)
            if self.verifica_existencia_produto(oracle, id_produto):
                print(f"O Produto de ID {id_produto} não existe.")
                continue
            else:
                # Recupera o produto existente para preencher os valores antigos
                produto_existente = self._recupera_produto(oracle, id_produto)

                if produto_existente is None:
                    print(f"Erro ao recuperar dados do produto com ID {id_produto}.")
                    continue

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

                print("\n✅ Produto atualizado com sucesso!")
                if produto_atualizado:
                    print(produto_atualizado.to_string())
                else:
                    # Mostra informações básicas se algo der errado
                    print(f"ID: {id_produto} | Nome: {novo_nome} | Preço: R$ {novo_preco:.2f}")

                # Pergunta se deseja atualizar outro produto
                continuar = input("\nDeseja atualizar outro produto? (s/n): ").lower()
                if continuar != 's':
                    return produto_atualizado

    def deletarProduto(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Loop para deletar múltiplos produtos
        while True:
            # Lista produtos cadastrados
            query_produtos = "SELECT id_produto, nome FROM produtos ORDER BY nome"
            df_produtos = oracle.sqlToDataFrame(query_produtos)

            if df_produtos.empty:
                print("Nenhum produto cadastrado.")
                return

            print("\n--- Produtos Cadastrados ---")
            for idx, row in df_produtos.iterrows():
                print(f"{idx + 1}. ID: {int(row['id_produto'])} | Nome: {row['nome']}")

            # Solicita ao usuário qual produto deseja excluir
            selecao = input("\nDigite o número do produto para excluir (ou 0 para voltar): ")

            if selecao == '0':
                break

            try:
                idx_selecionado = int(selecao) - 1
                if idx_selecionado < 0 or idx_selecionado >= len(df_produtos):
                    print("❌ Opção inválida!")
                    continue
            except ValueError:
                print("❌ Entrada inválida!")
                continue

            produto_selecionado = df_produtos.iloc[idx_selecionado]
            id_produto = int(produto_selecionado['id_produto'])

            # Recupera os dados do produto antes de excluir para exibição
            produto_excluido = self._recupera_produto(oracle, id_produto)

            # Verifica se existem itens de compra associados
            query_item_compra = f"SELECT COUNT(*) as qtde FROM item_compra WHERE id_produto = {id_produto}"
            df_item_compra = oracle.sqlToDataFrame(query_item_compra)
            qtde_item_compra = int(df_item_compra.iloc[0]["qtde"])

            # Verifica se existem itens de venda associados
            query_item_venda = f"SELECT COUNT(*) as qtde FROM item_venda WHERE id_produto = {id_produto}"
            df_item_venda = oracle.sqlToDataFrame(query_item_venda)
            qtde_item_venda = int(df_item_venda.iloc[0]["qtde"])

            if qtde_item_compra > 0 or qtde_item_venda > 0:
                print(f"\n⚠️  Não é possível excluir o produto '{produto_selecionado['nome']}'")
                print(f"Motivo: Existem registros associados:")
                if qtde_item_compra > 0:
                    print(f"  - {qtde_item_compra} item(ns) em compras")
                if qtde_item_venda > 0:
                    print(f"  - {qtde_item_venda} item(ns) em vendas")
                print("💡 Dica: Remova os registros de compra/venda associados antes de deletar o produto.")
                continuar = input("\nDeseja tentar outro produto? (s/n): ").lower()
                if continuar != 's':
                    break
                continue

            # Pede confirmação
            confirmacao = input(f"\nDeseja realmente excluir o produto '{produto_selecionado['nome']}'? (s/n): ").lower()
            if confirmacao != 's':
                print("Exclusão cancelada.")
                continuar = input("Deseja excluir outro produto? (s/n): ").lower()
                if continuar != 's':
                    break
                continue

            # Verifica se existe estoque associado
            query_estoque = f"SELECT COUNT(*) as qtde FROM estoque WHERE id_produto = {id_produto}"
            df_estoque = oracle.sqlToDataFrame(query_estoque)
            qtde_estoque = int(df_estoque.iloc[0]["qtde"])

            # Deleta estoque se existir (devido ao ON DELETE CASCADE, pode ser automático)
            if qtde_estoque > 0:
                sql_del_estoque = f"DELETE FROM estoque WHERE id_produto = {id_produto}"
                oracle.write(sql_del_estoque)

            # Deleta Produto
            sql_del_produto = f"DELETE FROM produtos WHERE id_produto = {id_produto}"
            oracle.write(sql_del_produto)

            # Exibe os atributos do produto excluído
            print("\n✅ Produto Removido com Sucesso!")
            if produto_excluido:
                print(produto_excluido.to_string())
            else:
                print(f"ID: {id_produto} | Nome: {produto_selecionado['nome']}")

            # Pergunta se deseja deletar outro produto
            continuar = input("\nDeseja excluir outro produto? (s/n): ").lower()
            if continuar != 's':
                break

