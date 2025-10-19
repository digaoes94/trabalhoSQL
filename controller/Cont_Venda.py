from model.Venda import Venda
from model.ItemVenda import ItemVenda
from model.Cliente import Cliente
from model.Produto import Produto
from conexion.oracle_queries import OracleQueries
from datetime import date
import pandas as pd # Necessário para o método de estoque

class Cont_Venda:
    def __init__(self):
        # self.cont_cliente = Cont_Cliente() # Exemplo de injeção de dependência
        pass
        
    def _get_next_id(self, oracle: OracleQueries) -> int:
        """ Método interno para obter o próximo ID de Venda. """
        query = "SELECT MAX(id_venda) AS MAX_ID FROM vendas"
        df = oracle.sqlToDataFrame(query)
        return int(df.max_id.values[0]) + 1 if df.max_id.notna().any() else 1

    def _recupera_estoque(self, oracle: OracleQueries, id_produto: int) -> dict:
        """ 
        Método interno para buscar os dados de estoque de um Produto.
        Retorna um dicionário com os campos 'custo_unitario', 'quantidade', 'total'.
        """
        query = f"SELECT custo_unitario, quantidade, total FROM estoque WHERE id_produto = {id_produto}"
        df = oracle.sqlToDataFrame(query)
        
        if df.empty:
            return {"custo_unitario": 0.0, "quantidade": 0, "total": 0.0}
        else:
            data = df.iloc[0]
            return {
                "custo_unitario": float(data["custo_unitario"]), 
                "quantidade": int(data["quantidade"]), 
                "total": float(data["total"])
            }

    def _atualizar_estoque_venda(self, oracle: OracleQueries, item_venda: ItemVenda, custo_unitario_cmp: float):
        """
        Atualiza o estoque e registra o CMV após uma venda.
        """
        produto = item_venda.produto
        qtd_saida = item_venda.quantidade
        
        # 1. Recupera o saldo atual do estoque
        estoque_atual = self._recupera_estoque(oracle, produto.id_produto)
        qtd_atual = estoque_atual["quantidade"]
        total_atual = estoque_atual["total"]
        
        # 2. Calcula a nova situação do estoque
        nova_quantidade = qtd_atual - qtd_saida
        
        # O custo total de saída (CMV) é calculado com base no CUSTO UNITÁRIO MÉDIO ATUAL
        cmv_saida = qtd_saida * custo_unitario_cmp 
        
        # O novo TOTAL do estoque é reduzido pelo CMV, mantendo o novo custo unitário
        novo_total = total_atual - cmv_saida
        
        # 3. Prepara a query de atualização
        if nova_quantidade < 0:
             raise Exception("Erro de Estoque: Tentativa de vender mais do que o saldo. Operação Cancelada.")
        
        if nova_quantidade == 0:
            # Se o estoque zera, o registro pode ser mantido com 0 ou deletado. Mantendo o registro zerado.
            sql_estoque = f"""
                UPDATE estoque 
                SET custo_unitario = 0.0, quantidade = 0, total = 0.0
                WHERE id_produto = {produto.id_produto}
            """
        else:
            # Se ainda resta estoque, o Custo Unitário não muda, apenas a Qtd e Total.
            sql_estoque = f"""
                UPDATE estoque 
                SET quantidade = {nova_quantidade}, 
                    total = {novo_total}
                WHERE id_produto = {produto.id_produto}
            """

        # 4. Persiste a atualização
        oracle.write(sql_estoque)
        print(f"-> Estoque atualizado para {produto.nome} (Saída CMV: R$ {cmv_saida:.2f})")
        
    # ---------------------------------------------------------------------------
    # MÉTODOS DE TRANSAÇÃO
    # ---------------------------------------------------------------------------

    def novaVenda(self) -> Venda:
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        
        # 1. Recupera Cliente
        cpf_cliente = input("CPF do Cliente para a Venda: ")
        # Simulação de busca do Cliente
        cliente_placeholder = Cliente(cpf=cpf_cliente, nome="Cliente Teste", endereco=None, email=None, telefone=None)
        
        if cliente_placeholder.cpf != cpf_cliente:
            print(f"Cliente de CPF {cpf_cliente} não encontrado.")
            return None

        # 2. Gera ID e Data
        id_venda = self._get_next_id(oracle)
        data_venda = date.today()
        
        # 3. Cria o objeto Venda inicial
        nova_venda = Venda(id_venda=id_venda, cliente=cliente_placeholder, data=data_venda, total=0.0)
        
        # 4. Adiciona Itens (loop)
        print("\n--- Adicionar Itens à Venda ---")
        nova_venda.itens = self.adicionarItemVenda(oracle, nova_venda)
        
        if not nova_venda.itens:
            print("Venda cancelada por não ter itens.")
            return None
            
        # 5. Finaliza (persiste e atualiza o total)
        total_venda = sum(item.subtotal for item in nova_venda.itens)
        nova_venda.total = total_venda
        
        self.finalizarVenda(oracle, nova_venda)
        
        print("\n--- Venda Registrada com Sucesso ---")
        print(nova_venda.to_string())
        
        return nova_venda

    def adicionarItemVenda(self, oracle: OracleQueries, venda: Venda) -> list:
        itens = []
        while True:
            id_produto = input("ID do Produto (0 para finalizar): ")
            if id_produto == '0':
                break
                
            try:
                id_produto = int(id_produto)
            except ValueError:
                print("ID do Produto inválido.")
                continue

            # 1. Verifica Estoque e Custo CMP
            estoque_atual = self._recupera_estoque(oracle, id_produto)
            qtd_estoque = estoque_atual["quantidade"]
            custo_unitario_cmp = estoque_atual["custo_unitario"]
            
            if qtd_estoque <= 0:
                print(f"Produto {id_produto} sem estoque.")
                continue

            # Simulação de busca do Produto
            produto_placeholder = Produto(id_produto=id_produto, nome=f"Produto {id_produto}", preco=10.0, descricao="")
            
            try:
                quantidade = int(input(f"Quantidade vendida de {produto_placeholder.nome} (Max: {qtd_estoque}): "))
                
                if quantidade > qtd_estoque:
                    print(f"Quantidade indisponível. Máximo: {qtd_estoque}.")
                    continue
                    
                preco_unitario_venda = float(input(f"Preço Unitário de Venda de {produto_placeholder.nome}: "))
            except ValueError:
                print("Entrada inválida. Tente novamente.")
                continue
                
            subtotal = quantidade * preco_unitario_venda
            
            item = ItemVenda(
                produto=produto_placeholder, 
                quantidade=quantidade, 
                preco_unitario=preco_unitario_venda, # Este é o preço de VENDA, não o CUSTO!
                subtotal=subtotal, 
                venda=venda
            )
            # Adiciona o custo CMP do momento ao objeto para uso posterior no método finalizarVenda
            item.custo_unitario_cmp = custo_unitario_cmp 
            itens.append(item)
            print(f"Item adicionado. Subtotal: R$ {subtotal:.2f}")
            
        return itens

    def finalizarVenda(self, oracle: OracleQueries, venda: Venda):
        """ Persiste a Venda e todos os seus Itens e atualiza o Estoque (CMV). """
        
        # 1. Persiste a Venda principal
        sql_venda = f"""
            INSERT INTO vendas (id_venda, cpf_cliente, data, total) 
            VALUES ({venda.id_venda}, '{venda.cliente.cpf}', DATE '{venda.data}', {venda.total})
        """
        oracle.write(sql_venda)
        print("-> Venda persistida na tabela VENDAS.")

        # 2. Persiste os Itens da Venda e Atualiza o Estoque (CMV)
        for item in venda.itens:
            # Presume-se que ItemVenda tem um campo 'preco_custo' ou 'custo_cmv' para registrar o CMV
            # Se a tabela ItemVendas só tem o preço de venda, vamos registrar o CMV do momento separadamente 
            # na tabela de Estoque/Relatório
            
            sql_item = f"""
                INSERT INTO itemvendas (id_venda, id_produto, quantidade, preco_unitario, subtotal)
                VALUES ({venda.id_venda}, {item.produto.id_produto}, {item.quantidade}, {item.preco_unitario}, {item.subtotal})
            """
            oracle.write(sql_item)
            
            # 3. ATUALIZAÇÃO DO ESTOQUE (Lógica de Baixa CMV/CMP)
            # Usa o custo CMP que foi anexado temporariamente ao objeto ItemVenda
            self._atualizar_estoque_venda(oracle, item, item.custo_unitario_cmp)
            
        print("-> Itens de Venda persistidos na tabela ITEMVENDAS.")

    def pesquisarVenda(self) -> Venda:
        oracle = OracleQueries(can_write=False)
        oracle.connect()
        
        id_venda = input("Informe o ID da Venda que deseja pesquisar: ")
        
        try:
            id_venda = int(id_venda)
        except ValueError:
            print("ID de Venda inválido.")
            return None
            
        # Query para buscar a venda e todos os seus itens
        query_venda = f"""
            SELECT 
                v.id_venda, v.data, v.total, v.cpf_cliente, 
                iv.quantidade, iv.preco_unitario, iv.subtotal, 
                p.id_produto, p.nome as nome_produto
            FROM vendas v
            INNER JOIN itemvendas iv ON v.id_venda = iv.id_venda
            INNER JOIN produtos p ON iv.id_produto = p.id_produto
            WHERE v.id_venda = {id_venda}
        """
        
        df_venda = oracle.sqlToDataFrame(query_venda)
        
        if df_venda.empty:
            print(f"Venda de ID {id_venda} não encontrada.")
            return None
        
        # Reconstroi o objeto Venda
        venda_data = df_venda.iloc[0]
        
        # Necessita de um Cont_Cliente para buscar o Cliente completo, mas vamos simplificar
        cliente_placeholder = Cliente(cpf=venda_data["cpf_cliente"], nome="N/A", endereco=None, email=None, telefone=None)
        
        venda_recuperada = Venda(
            id_venda=int(venda_data["id_venda"]),
            cliente=cliente_placeholder,
            data=venda_data["data"],
            total=float(venda_data["total"])
        )
        
        itens = []
        for index, row in df_venda.iterrows():
            produto = Produto(id_produto=int(row["id_produto"]), nome=row["nome_produto"], preco=row["preco_unitario"], descricao="N/A")
            item = ItemVenda(
                produto=produto, 
                quantidade=int(row["quantidade"]), 
                preco_unitario=float(row["preco_unitario"]), # Preço de Venda
                subtotal=float(row["subtotal"]), 
                venda=venda_recuperada
            )
            itens.append(item)
        
        venda_recuperada.itens = itens
        
        print("\n--- Venda Encontrada ---")
        print(venda_recuperada.to_string())
        print("Itens:")
        for item in itens:
            print(f"  - {item.to_string()}")
            
        return venda_recuperada