from conexion.oracle_queries import OracleQueries
import pandas as pd
import os

class Relatorio:
    def __init__(self):
        # Usa __file__ para obter o caminho correto dos arquivos SQL
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            with open(os.path.join(base_path, "sql/relatorioClientes.sql")) as f:
                self.query_relatorioClientes = f.read()

            with open(os.path.join(base_path, "sql/relatorioCompras.sql")) as f:
                self.query_relatorioCompras = f.read()

            with open(os.path.join(base_path, "sql/relatorioEstoque.sql")) as f:
                self.query_relatorioEstoque = f.read()

            with open(os.path.join(base_path, "sql/relatorioFornecedores.sql")) as f:
                self.query_relatorioFornecedores = f.read()

            with open(os.path.join(base_path, "sql/relatorioProdutos.sql")) as f:
                self.query_relatorioProdutos = f.read()

            with open(os.path.join(base_path, "sql/relatorioVendas.sql")) as f:
                self.query_relatorioVendas = f.read()
        except FileNotFoundError as e:
            print(f"❌ Erro: Arquivo SQL não encontrado: {e}")
            raise
    
    def get_relatorioClientes(self):
        oracle = OracleQueries()
        oracle.connect()
        
        print("=" * 80)
        print("📋 RELATÓRIO DE CLIENTES")
        print("=" * 80)
        
        df = oracle.sqlToDataFrame(self.query_relatorioClientes)
        
        if df.empty:
            print("❌ Nenhum cliente encontrado!")
        else:
            print(f"📊 Total de clientes: {len(df)}")
            print("-" * 80)
            
            for index, row in df.iterrows():
                print(f"👤 CLIENTE {index + 1}")
                print(f"   CPF: {row['cpf']}")
                print(f"   Nome: {row['nome']}")
                print(f"   Email: {row['email']}")
                print(f"   Telefone: {row['telefone']}")
                
                if pd.notna(row['cep']):
                    print(f"   📍 ENDEREÇO:")
                    print(f"      CEP: {row['cep']}")
                    print(f"      {row['logradouro']}, {row['numero']}")
                    if pd.notna(row['complemento']):
                        print(f"      {row['complemento']}")
                    print(f"      {row['bairro']} - {row['cidade']}/{row['estado']}")
                else:
                    print(f"   📍 ENDEREÇO: Não cadastrado")
                
                print("-" * 80)
        
        oracle.close()
        input("\n⏎ Pressione Enter para voltar ao menu...")

    def get_relatorioCompras(self):
        oracle = OracleQueries()
        oracle.connect()
        
        print("=" * 80)
        print("🛒 RELATÓRIO DE COMPRAS")
        print("=" * 80)
        
        df = oracle.sqlToDataFrame(self.query_relatorioCompras)
        
        if df.empty:
            print("❌ Nenhuma compra encontrada!")
        else:
            print(f"📊 Total de fornecedores com compras: {len(df)}")
            print("-" * 80)
            
            for index, row in df.iterrows():
                print(f"🛒 FORNECEDOR {index + 1}")
                print(f"   CNPJ: {row['cnpj']}")
                print(f"   Razão Social: {row['nome_fornecedor']}")
                print(f"   Nome Fantasia: {row['nomeFantasia']}")
                print(f"   Email: {row['email_fornecedor']}")
                print(f"   Telefone: {row['telefone_fornecedor']}")
                print(f"   📊 ESTATÍSTICAS:")
                print(f"      Total de compras: {row['total_de_compras']}")
                print(f"      💵 Valor total gasto: R$ {row['valor_total_gasto']:.2f}")
                print(f"      💰 Valor médio por compra: R$ {row['valor_medio_compra']:.2f}")
                print(f"      📅 Última compra: {row['ultima_compra']}")
                print("-" * 80)
        
        oracle.close()
        input("\n⏎ Pressione Enter para voltar ao menu...")

    def get_relatorioEstoque(self):
        oracle = OracleQueries()
        oracle.connect()
        
        print("=" * 80)
        print("📦 RELATÓRIO DE ESTOQUE")
        print("=" * 80)
        
        df = oracle.sqlToDataFrame(self.query_relatorioEstoque)
        
        if df.empty:
            print("❌ Nenhum produto no estoque!")
        else:
            print(f"📊 Total de produtos: {len(df)}")
            print("-" * 80)
            
            # Contadores por status
            sem_estoque = len(df[df['status_estoque'] == 'Sem Estoque'])
            estoque_baixo = len(df[df['status_estoque'] == 'Estoque Baixo'])
            estoque_ok = len(df[df['status_estoque'] == 'OK'])
            
            print(f"🔴 Sem Estoque: {sem_estoque}")
            print(f"🟡 Estoque Baixo: {estoque_baixo}")
            print(f"🟢 Estoque OK: {estoque_ok}")
            print("-" * 80)
            
            for index, row in df.iterrows():
                status_icon = "🔴" if row['status_estoque'] == 'Sem Estoque' else "🟡" if row['status_estoque'] == 'Estoque Baixo' else "🟢"
                print(f"📦 {status_icon} {row['nome_produto']}")
                print(f"   ID: {row['id_produto']}")
                print(f"   Quantidade: {row['qtde_estoque']} unidades")
                print(f"   Status: {row['status_estoque']}")
                print("-" * 80)
        
        oracle.close()
        input("\n⏎ Pressione Enter para voltar ao menu...")

    def get_relatorioFornecedores(self):
        oracle = OracleQueries()
        oracle.connect()
        
        print("=" * 80)
        print("🏢 RELATÓRIO DE FORNECEDORES")
        print("=" * 80)
        
        df = oracle.sqlToDataFrame(self.query_relatorioFornecedores)
        
        if df.empty:
            print("❌ Nenhum fornecedor encontrado!")
        else:
            print(f"📊 Total de fornecedores: {len(df)}")
            print("-" * 80)
            
            for index, row in df.iterrows():
                print(f"🏢 FORNECEDOR {index + 1}")
                print(f"   CNPJ: {row['cnpj']}")
                print(f"   Razão Social: {row['razaoSocial']}")
                print(f"   Nome Fantasia: {row['nomeFantasia']}")
                print(f"   Email: {row['email']}")
                print(f"   Telefone: {row['telefone']}")
                
                if pd.notna(row['cep']):
                    print(f"   📍 ENDEREÇO:")
                    print(f"      CEP: {row['cep']}")
                    print(f"      {row['logradouro']}, {row['numero']}")
                    if pd.notna(row['complemento']):
                        print(f"      {row['complemento']}")
                    print(f"      {row['bairro']} - {row['cidade']}/{row['estado']}")
                else:
                    print(f"   📍 ENDEREÇO: Não cadastrado")
                
                print("-" * 80)
        
        oracle.close()
        input("\n⏎ Pressione Enter para voltar ao menu...")

    def get_relatorioProdutos(self):
        oracle = OracleQueries()
        oracle.connect()
        
        print("=" * 80)
        print("📦 RELATÓRIO DE PRODUTOS")
        print("=" * 80)
        
        df = oracle.sqlToDataFrame(self.query_relatorioProdutos)
        
        if df.empty:
            print("❌ Nenhum produto encontrado!")
        else:
            print(f"📊 Total de produtos: {len(df)}")
            print("-" * 80)
            
            for index, row in df.iterrows():
                print(f"📦 PRODUTO {index + 1}")
                print(f"   ID: {row['id_produto']}")
                print(f"   Nome: {row['nome_produto']}")
                print(f"   Descrição: {row['descricao']}")
                print(f"   Preço: R$ {row['preco_unitario']:.2f}")
                print(f"   Estoque: {row['qtde_estoque']} unidades")
                
                status_icon = "🔴" if row['status_estoque'] == 'Sem Estoque' else "🟡" if row['status_estoque'] == 'Estoque Baixo' else "🟢"
                print(f"   Status: {status_icon} {row['status_estoque']}")
                
                print("-" * 80)
        
        oracle.close()
        input("\n⏎ Pressione Enter para voltar ao menu...")

    def get_relatorioVendas(self):
        oracle = OracleQueries()
        oracle.connect()
        
        print("=" * 80)
        print("💰 RELATÓRIO DE VENDAS")
        print("=" * 80)
        
        df = oracle.sqlToDataFrame(self.query_relatorioVendas)
        
        if df.empty:
            print("❌ Nenhuma venda encontrada!")
        else:
            print(f"📊 Total de vendas: {len(df)}")
            print("-" * 80)
            
            for index, row in df.iterrows():
                print(f"💰 VENDA {index + 1}")
                print(f"   ID: {row['id_venda']}")
                print(f"   Data: {row['data_venda']}")
                print(f"   Cliente: {row['nome_cliente']}")
                print(f"   CPF: {row['cpf_cliente']}")
                print(f"   Email: {row['email_cliente']}")
                print(f"   Telefone: {row['telefone_cliente']}")
                print(f"   Total de itens: {row['total_itens']}")
                print(f"   💵 Valor Total: R$ {row['valor_total']:.2f}")
                print("-" * 80)
        
        oracle.close()
        input("\n⏎ Pressione Enter para voltar ao menu...")