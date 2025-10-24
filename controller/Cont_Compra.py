from model.Compra import Compra
from model.ItemCompra import ItemCompra
from model.Fornecedor import Fornecedor
from model.Produto import Produto
from conexion.oracle_queries import OracleQueries
# O uso de datetime é necessário para as datas
from datetime import datetime
# Se for usar pandas para manipulação de DataFrame:
# import pandas as pd 

# Dependência: Assumindo que você tem um Controller de Fornecedor para buscar o objeto
# from controller.cont_fornecedor import Cont_Fornecedor 

class Cont_Compra:
    def __init__(self):
        # self.cont_fornecedor = Cont_Fornecedor() # Exemplo de injeção de dependência
        pass
        
    def _get_next_id(self, oracle: OracleQueries) -> int:
        """ Método interno para obter o próximo ID de Compra (assumindo que o DB não faz isso automaticamente). """
        query = "SELECT MAX(id_compra) AS MAX_ID FROM compras"
        df = oracle.sqlToDataFrame(query)
        # O ID será o valor máximo + 1, ou 1 se o DB estiver vazio
        return int(df.max_id.values[0]) + 1 if df.max_id.notna().any() else 1

    def _recupera_estoque(self, oracle: OracleQueries, id_produto: int) -> dict:
        """ 
        Método interno para buscar os dados de estoque de um Produto.
        Retorna um dicionário com os campos 'custo_unitario', 'quantidade', 'total'.
        """
        # A tabela ESTOQUE deve ter uma linha por produto com os saldos atuais
        query = f"SELECT custo_unitario, quantidade, total FROM estoque WHERE id_produto = {id_produto}"
        df = oracle.sqlToDataFrame(query)
        
        if df.empty:
            # Produto não está no estoque (saldo inicial zero)
            return {"custo_unitario": 0.0, "quantidade": 0, "total": 0.0}
        else:
            data = df.iloc[0]
            return {
                "custo_unitario": float(data["custo_unitario"]), 
                "quantidade": int(data["quantidade"]), 
                "total": float(data["total"])
            }

    def _atualizar_estoque_cmp(self, oracle: OracleQueries, item_compra: ItemCompra):
        """
        Atualiza o estoque com a lógica do Custo Médio Ponderado (CMP) após uma compra.
        """
        produto = item_compra.produto
        qtd_compra = item_compra.quantidade
        total_compra = item_compra.subtotal
        
        # 1. Recupera o saldo atual do estoque
        estoque_atual = self._recupera_estoque(oracle, produto.id_produto)
        qtd_atual = estoque_atual["quantidade"]
        total_atual = estoque_atual["total"]
        
        # 2. Calcula os novos valores (CMP)
        nova_quantidade = qtd_atual + qtd_compra
        novo_total = total_atual + total_compra
        
        # Se a nova quantidade for zero (o que não deve ocorrer em uma compra), o custo é zero
        if nova_quantidade > 0:
            novo_custo_unitario = novo_total / nova_quantidade
        else:
            novo_custo_unitario = 0.0

        # 3. Prepara a query de atualização/inserção (MERGE ou UPDATE/INSERT)
        if qtd_atual == 0:
            # Se o produto não estava no estoque, insere
            sql_estoque = f"""
                INSERT INTO estoque (id_produto, custo_unitario, quantidade, total) 
                VALUES ({produto.id_produto}, {novo_custo_unitario}, {nova_quantidade}, {novo_total})
            """
        else:
            # Se o produto já estava no estoque, atualiza
            sql_estoque = f"""
                UPDATE estoque 
                SET custo_unitario = {novo_custo_unitario}, 
                    quantidade = {nova_quantidade}, 
                    total = {novo_total}
                WHERE id_produto = {produto.id_produto}
            """

        # 4. Persiste a atualização
        oracle.write(sql_estoque)
        print(f"-> Estoque atualizado para {produto.nome} (CMP: R$ {novo_custo_unitario:.2f})")

    # ---------------------------------------------------------------------------
    # MÉTODOS DE TRANSAÇÃO
    # ---------------------------------------------------------------------------

    def novaCompra(self) -> Compra:
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        
        # 1. Recupera Fornecedor (Você precisará de um Cont_Fornecedor real para isso)
        cnpj_fornecedor = input("CNPJ do Fornecedor para a Compra: ")
        
        # Busca o id_fornecedor baseado no CNPJ
        query_fornecedor = f"SELECT id_fornecedor, cnpj, razaoSocial, nomeFantasia, email, telefone FROM fornecedores WHERE cnpj = '{cnpj_fornecedor}'"
        df_fornecedor = oracle.sqlToDataFrame(query_fornecedor)

        if df_fornecedor.empty:
            print(f"Fornecedor de CNPJ {cnpj_fornecedor} não encontrado.")
            return None

        fornecedor_data = df_fornecedor.iloc[0]
        fornecedor_obj = Fornecedor(
            id_fornecedor=int(fornecedor_data["id_fornecedor"]),
            cnpj=fornecedor_data["cnpj"],
            razaoSocial=fornecedor_data["razaosocial"],
            nomeFantasia=fornecedor_data["nomefantasia"],
            email=fornecedor_data["email"],
            telefone=fornecedor_data["telefone"],
            endereco=None
        )

        # 2. Gera ID e Data
        id_compra = self._get_next_id(oracle)
        data_compra = datetime.now()
        
        # 3. Cria o objeto Compra inicial
        nova_compra = Compra(id_compra=id_compra, fornecedor=fornecedor_obj, data=data_compra, total=0.0)
        
        # 4. Adiciona Itens (loop)
        print("\n--- Adicionar Itens à Compra ---")
        nova_compra.itens = self.adicionarItemCompra(oracle, nova_compra)
        
        if not nova_compra.itens:
            print("Compra cancelada por não ter itens.")
            return None
            
        # 5. Finaliza (persiste e atualiza o total)
        total_compra = sum(item.subtotal for item in nova_compra.itens)
        nova_compra.total = total_compra
        
        self.finalizarCompra(oracle, nova_compra)
        
        print("\n--- Compra Registrada com Sucesso ---")
        print(nova_compra.to_string())
        
        return nova_compra

    def adicionarItemCompra(self, oracle: OracleQueries, compra: Compra) -> list:
        itens = []
        while True:
            id_produto = input("ID do Produto (0 para finalizar): ")
            if id_produto == '0':
                break

            # Valida se o ID é um número
            try:
                id_produto = int(id_produto)
            except ValueError:
                print("❌ ID do produto inválido. Digite um número.")
                continue

            # Busca o produto no banco de dados
            query_produto = f"SELECT id_produto, nome, preco_unitario FROM produtos WHERE id_produto = {id_produto}"
            df_produto = oracle.sqlToDataFrame(query_produto)

            if df_produto.empty:
                print(f"❌ Produto de ID {id_produto} não encontrado no banco de dados.")
                continue

            # Reconstrói o objeto Produto com dados reais do banco
            produto_data = df_produto.iloc[0]
            produto = Produto(
                id_produto=int(produto_data["id_produto"]),
                nome=produto_data["nome"],
                preco=float(produto_data["preco_unitario"]),
                descricao=""
            )

            try:
                quantidade = int(input(f"Quantidade comprada de {produto.nome}: "))
                preco_unitario = float(input(f"Custo Unitário de {produto.nome}: "))
            except ValueError:
                print("❌ Entrada inválida. Tente novamente.")
                continue

            subtotal = quantidade * preco_unitario

            item = ItemCompra(
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal,
                compra=compra
            )
            itens.append(item)
            print(f"✅ Item adicionado. Subtotal: R$ {subtotal:.2f}")

        return itens

    def finalizarCompra(self, oracle: OracleQueries, compra: Compra):
        """ Persiste a Compra e todos os seus Itens e atualiza o Estoque. """
        
        # 1. Persiste a Compra principal
        # Formata a data/hora no padrão Oracle: YYYY-MM-DD HH:MI:SS
        data_formatada = compra.data.strftime('%Y-%m-%d %H:%M:%S') if hasattr(compra.data, 'strftime') else str(compra.data)
        sql_compra = f"""
            INSERT INTO compras (id_compra, id_fornecedor, data_compra, valor_total)
            VALUES ({compra.id_compra}, {compra.fornecedor.id_fornecedor}, TO_TIMESTAMP('{data_formatada}', 'YYYY-MM-DD HH24:MI:SS'), {compra.total})
        """
        oracle.write(sql_compra)
        print("-> Compra persistida na tabela COMPRAS.")

        # 2. Persiste os Itens da Compra e Atualiza o Estoque (CMP)
        for item in compra.itens:
            sql_item = f"""
                INSERT INTO item_compra (id_item_compra, id_compra, id_produto, quantidade, preco_unitario_compra, subtotal)
                VALUES (item_compra_id_seq.NEXTVAL, {compra.id_compra}, {item.produto.id_produto}, {item.quantidade}, {item.preco_unitario}, {item.subtotal})
            """
            oracle.write(sql_item)
            
            # 3. ATUALIZAÇÃO DO ESTOQUE (Lógica CMP)
            self._atualizar_estoque_cmp(oracle, item)
            
        print("-> Itens de Compra persistidos na tabela ITEMCOMPRAS.")

    def pesquisarCompra(self) -> Compra:
        oracle = OracleQueries(can_write=False)
        oracle.connect()
        
        id_compra = input("Informe o ID da Compra que deseja pesquisar: ")
        
        try:
            id_compra = int(id_compra)
        except ValueError:
            print("ID de Compra inválido.")
            return None
            
        # Query para buscar a compra e todos os seus itens
        query_compra = f"""
            SELECT 
                c.id_compra, c.data_compra, c.valor_total, c.id_fornecedor, 
                ic.quantidade, ic.preco_unitario_compra, ic.subtotal, 
                p.id_produto, p.nome as nome_produto
            FROM compras c
            INNER JOIN item_compra ic ON c.id_compra = ic.id_compra
            INNER JOIN produtos p ON ic.id_produto = p.id_produto
            WHERE c.id_compra = {id_compra}
        """
        
        df_compra = oracle.sqlToDataFrame(query_compra)
        
        if df_compra.empty:
            print(f"Compra de ID {id_compra} não encontrada.")
            return None
        
        # Reconstroi o objeto Compra
        compra_data = df_compra.iloc[0]
        
        # Busca o Fornecedor completo para a Compra
        query_fornecedor = f"SELECT id_fornecedor, cnpj, razaoSocial, nomeFantasia, email, telefone FROM fornecedores WHERE id_fornecedor = {compra_data['id_fornecedor']}"
        df_fornecedor = oracle.sqlToDataFrame(query_fornecedor)
        fornecedor_data = df_fornecedor.iloc[0]
        fornecedor_obj = Fornecedor(
            id_fornecedor=int(fornecedor_data["id_fornecedor"]),
            cnpj=fornecedor_data["cnpj"],
            razaoSocial=fornecedor_data["razaosocial"],
            nomeFantasia=fornecedor_data["nomefantasia"],
            email=fornecedor_data["email"],
            telefone=fornecedor_data["telefone"],
            endereco=None
        )
        
        compra_recuperada = Compra(
            id_compra=int(compra_data["id_compra"]),
            fornecedor=fornecedor_obj,
            data=compra_data["data_compra"],
            total=float(compra_data["valor_total"])
        )
        
        itens = []
        for index, row in df_compra.iterrows():
            produto = Produto(id_produto=int(row["id_produto"]), nome=row["nome_produto"], preco=row["preco_unitario_compra"], descricao="N/A")
            item = ItemCompra(
                produto=produto,
                quantidade=int(row["quantidade"]),
                preco_unitario=float(row["preco_unitario_compra"]), 
                subtotal=float(row["subtotal"]), 
                compra=compra_recuperada
            )
            itens.append(item)
        
        compra_recuperada.itens = itens
        
        print("\n--- Compra Encontrada ---")
        print(compra_recuperada.to_string())
        print("Itens:")
        for item in itens:
            print(f"  - {item.to_string()}")
            
        return compra_recuperada

