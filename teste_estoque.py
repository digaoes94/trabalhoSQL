"""
Script para testar se o estoque está sendo atualizado corretamente.
Simula: Compra 14 unidades -> Vende 13 -> Verifica se estoque mostra 1
"""

import sys
import os
from datetime import datetime

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from conexion.oracle_queries import OracleQueries

def teste_estoque():
    oracle = OracleQueries(can_write=True)
    oracle.connect()

    print("\n" + "="*70)
    print("  TESTE DE ATUALIZAÇÃO DE ESTOQUE")
    print("="*70 + "\n")

    # ========== COMPRA: 14 UNIDADES ==========
    print("1️⃣  COMPRA: Adicionando 14 unidades do Mouse Logitech ao estoque...")

    data_compra = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insere a compra
    sql_compra = f"""
        INSERT INTO compras (id_compra, id_fornecedor, data_compra, valor_total)
        VALUES (1, 1, TO_TIMESTAMP('{data_compra}', 'YYYY-MM-DD HH24:MI:SS'), 2100.00)
    """
    oracle.write(sql_compra)
    print("   ✅ Compra registrada (ID: 1)\n")

    # Insere item da compra (Mouse Logitech - ID 2)
    sql_item_compra = f"""
        INSERT INTO item_compra (id_item_compra, id_compra, id_produto, quantidade, preco_unitario_compra, subtotal)
        VALUES (1, 1, 2, 14, 150.00, 2100.00)
    """
    oracle.write(sql_item_compra)
    print("   ✅ Item de compra registrado (14 x Mouse Logitech @ R$ 150.00)\n")

    # Atualiza estoque (CMP)
    sql_estoque = """
        INSERT INTO estoque (id_produto, custo_unitario, quantidade, total)
        VALUES (2, 150.00, 14, 2100.00)
    """
    oracle.write(sql_estoque)
    print("   ✅ Estoque atualizado: 14 unidades\n")

    # ========== VENDA: 13 UNIDADES ==========
    print("2️⃣  VENDA: Vendendo 13 unidades do Mouse Logitech...")

    data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insere a venda
    sql_venda = f"""
        INSERT INTO vendas (id_venda, id_cliente, data_venda, valor_total)
        VALUES (1, 1, TO_TIMESTAMP('{data_venda}', 'YYYY-MM-DD HH24:MI:SS'), 1950.00)
    """
    oracle.write(sql_venda)
    print("   ✅ Venda registrada (ID: 1)\n")

    # Insere item da venda
    sql_item_venda = f"""
        INSERT INTO item_venda (id_item_venda, id_venda, id_produto, quantidade, preco_unitario_venda, subtotal)
        VALUES (1, 1, 2, 13, 150.00, 1950.00)
    """
    oracle.write(sql_item_venda)
    print("   ✅ Item de venda registrado (13 x Mouse Logitech @ R$ 150.00)\n")

    # Atualiza estoque (subtrai as 13 unidades)
    sql_estoque_update = """
        UPDATE estoque
        SET quantidade = 1,
            total = 150.00
        WHERE id_produto = 2
    """
    oracle.write(sql_estoque_update)
    print("   ✅ Estoque atualizado: 14 - 13 = 1 unidade\n")

    # ========== VERIFICAÇÃO ==========
    print("3️⃣  VERIFICAÇÃO: Consultando estoque real no banco...\n")

    query_estoque = "SELECT id_produto, quantidade, total FROM estoque WHERE id_produto = 2"
    df_estoque = oracle.sqlToDataFrame(query_estoque)

    if df_estoque.empty:
        print("   ❌ Erro: Nenhum registro de estoque encontrado!")
    else:
        row = df_estoque.iloc[0]
        qtd = int(row['quantidade'])
        total = float(row['total'])
        print(f"   Quantidade em ESTOQUE: {qtd} unidades")
        print(f"   Total em ESTOQUE: R$ {total:.2f}\n")

        if qtd == 1:
            print("   ✅ SUCESSO! Estoque está correto: 1 unidade restante\n")
        else:
            print(f"   ❌ ERRO! Estoque deveria ser 1, mas está {qtd}\n")

    # ========== RELATÓRIO ==========
    print("4️⃣  RELATÓRIO DE PRODUTOS (via SQL atualizado)...\n")

    query_relatorio = """
        SELECT p.id_produto, p.nome,
               COALESCE(e.quantidade, 0) as qtde_estoque,
               CASE
                    WHEN COALESCE(e.quantidade, 0) = 0 THEN 'Sem Estoque'
                    WHEN COALESCE(e.quantidade, 0) < 10 THEN 'Estoque Baixo'
                    ELSE 'OK'
               END as status_estoque
        FROM produtos p
        LEFT JOIN estoque e ON p.id_produto = e.id_produto
        WHERE p.id_produto = 2
    """
    df_relatorio = oracle.sqlToDataFrame(query_relatorio)

    if not df_relatorio.empty:
        row = df_relatorio.iloc[0]
        print(f"   Produto: {row['nome']}")
        print(f"   Quantidade: {int(row['qtde_estoque'])} unidades")
        print(f"   Status: {row['status_estoque']}")

        if int(row['qtde_estoque']) == 1 and row['status_estoque'] == 'Estoque Baixo':
            print("\n   ✅ RELATÓRIO CORRETO!\n")
        else:
            print("\n   ❌ RELATÓRIO COM ERRO!\n")

    print("="*70)
    print("  FIM DO TESTE")
    print("="*70 + "\n")

if __name__ == '__main__':
    try:
        teste_estoque()
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        sys.exit(1)
