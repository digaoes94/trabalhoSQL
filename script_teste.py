"""
Script de teste para popular o banco de dados com dados iniciais.
Cadastra: 1 Cliente, 1 Fornecedor e 3 Produtos.
"""

import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from conexion.oracle_queries import OracleQueries

def cadastrar_dados_teste():
    """Cadastra dados de teste no banco"""

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    print("\n" + "="*60)
    print("  SCRIPT DE TESTE - POPULAÇÃO DE DADOS")
    print("="*60 + "\n")

    # ========== CLIENTE ==========
    print("1️⃣  Cadastrando Cliente...")
    try:
        # Verifica se o cliente já existe
        query_verifica = "SELECT id_cliente FROM clientes WHERE cpf = '12345678901'"
        df_existe = oracle.sqlToDataFrame(query_verifica)

        if not df_existe.empty:
            id_cliente = int(df_existe.id_cliente.values[0])
            print(f"   ℹ️  Cliente já existe com ID: {id_cliente}")
            print(f"      - Nome: João Silva\n")
        else:
            sql_cliente = """
                INSERT INTO clientes (cpf, nome, email, telefone)
                VALUES ('12345678901', 'João Silva', 'joao@email.com', '(27) 99999-1234')
            """
            oracle.write(sql_cliente)

            # Recupera o ID gerado
            query_id_cliente = "SELECT clientes_id_seq.CURRVAL AS id_cliente FROM DUAL"
            df_id = oracle.sqlToDataFrame(query_id_cliente)
            id_cliente = int(df_id.id_cliente.values[0])

            # Cadastra o endereço
            sql_endereco = f"""
                INSERT INTO enderecos (cep, logradouro, numero, complemento, bairro, cidade, estado, id_cliente)
                VALUES ('29000-000', 'Rua das Flores', 123, 'Apto 101', 'Centro', 'Vitória', 'ES', {id_cliente})
            """
            oracle.write(sql_endereco)

            print(f"   ✅ Cliente cadastrado com ID: {id_cliente}")
            print(f"      - Nome: João Silva")
            print(f"      - CPF: 12345678901\n")

    except Exception as e:
        print(f"   ❌ Erro ao cadastrar cliente: {e}\n")
        return False

    # ========== FORNECEDOR ==========
    print("2️⃣  Cadastrando Fornecedor...")
    try:
        # Verifica se o fornecedor já existe
        query_verifica = "SELECT id_fornecedor FROM fornecedores WHERE cnpj = '12345678000195'"
        df_existe = oracle.sqlToDataFrame(query_verifica)

        if not df_existe.empty:
            id_fornecedor = int(df_existe.id_fornecedor.values[0])
            print(f"   ℹ️  Fornecedor já existe com ID: {id_fornecedor}")
            print(f"      - Razão Social: Tech Produtos LTDA\n")
        else:
            sql_fornecedor = """
                INSERT INTO fornecedores (cnpj, razaoSocial, nomeFantasia, email, telefone)
                VALUES ('12345678000195', 'Tech Produtos LTDA', 'TechProd', 'contato@techprod.com', '(27) 3333-4444')
            """
            oracle.write(sql_fornecedor)

            # Recupera o ID gerado
            query_id_fornecedor = "SELECT fornecedores_id_seq.CURRVAL AS id_fornecedor FROM DUAL"
            df_id = oracle.sqlToDataFrame(query_id_fornecedor)
            id_fornecedor = int(df_id.id_fornecedor.values[0])

            # Cadastra o endereço
            sql_endereco = f"""
                INSERT INTO enderecos (cep, logradouro, numero, complemento, bairro, cidade, estado, id_fornecedor)
                VALUES ('29000-100', 'Av. Comercial', 456, 'Sala 501', 'Praia do Canto', 'Vitória', 'ES', {id_fornecedor})
            """
            oracle.write(sql_endereco)

            print(f"   ✅ Fornecedor cadastrado com ID: {id_fornecedor}")
            print(f"      - Razão Social: Tech Produtos LTDA")
            print(f"      - CNPJ: 12345678000195\n")

    except Exception as e:
        print(f"   ❌ Erro ao cadastrar fornecedor: {e}\n")
        return False

    # ========== PRODUTOS ==========
    print("3️⃣  Cadastrando Produtos...")

    produtos = [
        {
            'nome': 'Notebook Dell',
            'descricao': 'Notebook 15.6 polegadas, processador i5',
            'preco': 3500.00
        },
        {
            'nome': 'Mouse Logitech',
            'descricao': 'Mouse sem fio com bateria de 12 meses',
            'preco': 150.00
        },
        {
            'nome': 'Teclado Mecânico',
            'descricao': 'Teclado mecânico RGB com switches Cherry MX',
            'preco': 450.00
        }
    ]

    try:
        for i, produto in enumerate(produtos, 1):
            # Verifica se o produto já existe
            query_verifica = f"SELECT id_produto FROM produtos WHERE nome = '{produto['nome']}'"
            df_existe = oracle.sqlToDataFrame(query_verifica)

            if not df_existe.empty:
                id_produto = int(df_existe.id_produto.values[0])
                print(f"   ℹ️  Produto {i} já existe com ID: {id_produto}")
                print(f"      - Nome: {produto['nome']}")
                print(f"      - Preço: R$ {produto['preco']:.2f}\n")
            else:
                sql_produto = f"""
                    INSERT INTO produtos (nome, preco_unitario, descricao)
                    VALUES ('{produto['nome']}', {produto['preco']}, '{produto['descricao']}')
                """
                oracle.write(sql_produto)

                # Recupera o ID gerado
                query_id_produto = "SELECT produtos_id_seq.CURRVAL AS id_produto FROM DUAL"
                df_id = oracle.sqlToDataFrame(query_id_produto)
                id_produto = int(df_id.id_produto.values[0])

                print(f"   ✅ Produto {i} cadastrado com ID: {id_produto}")
                print(f"      - Nome: {produto['nome']}")
                print(f"      - Preço: R$ {produto['preco']:.2f}\n")

    except Exception as e:
        print(f"   ❌ Erro ao cadastrar produtos: {e}\n")
        return False

    print("="*60)
    print("  ✅ TODOS OS DADOS DE TESTE FORAM CADASTRADOS!")
    print("="*60)
    print("\n📋 RESUMO:")
    print("   • 1 Cliente: João Silva (ID: 1)")
    print("   • 1 Fornecedor: Tech Produtos LTDA (ID: 1)")
    print("   • 3 Produtos: Notebook Dell, Mouse Logitech, Teclado Mecânico")
    print("\n   Agora você pode fazer vendas e compras usando esses dados!\n")

    return True

if __name__ == '__main__':
    try:
        sucesso = cadastrar_dados_teste()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\n❌ Erro geral: {e}\n")
        sys.exit(1)
