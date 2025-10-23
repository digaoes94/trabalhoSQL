import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexion.oracle_queries import OracleQueries

def drop_database_objects():
    oracle = OracleQueries(can_write=True)
    oracle.connect()

    drop_commands = [
        "DROP TABLE item_venda CASCADE CONSTRAINTS",
        "DROP TABLE item_compra CASCADE CONSTRAINTS",
        "DROP TABLE enderecos CASCADE CONSTRAINTS",
        "DROP TABLE vendas CASCADE CONSTRAINTS",
        "DROP TABLE compras CASCADE CONSTRAINTS",
        "DROP TABLE estoque CASCADE CONSTRAINTS",
        "DROP TABLE produtos CASCADE CONSTRAINTS",
        "DROP TABLE clientes CASCADE CONSTRAINTS",
        "DROP TABLE fornecedores CASCADE CONSTRAINTS",
        "DROP SEQUENCE clientes_id_seq",
        "DROP SEQUENCE produtos_id_seq",
        "DROP SEQUENCE fornecedores_id_seq",
        "DROP SEQUENCE vendas_id_seq",
        "DROP SEQUENCE compras_id_seq",
        "DROP SEQUENCE item_venda_id_seq",
        "DROP SEQUENCE item_compra_id_seq",
        "DROP SEQUENCE enderecos_id_seq",
        "DROP TRIGGER trg_clientes_pk",
        "DROP TRIGGER trg_produtos_pk",
        "DROP TRIGGER trg_fornecedores_pk",
        "DROP TRIGGER trg_vendas_pk",
        "DROP TRIGGER trg_compras_pk",
        "DROP TRIGGER trg_item_venda_pk",
        "DROP TRIGGER trg_item_compra_pk",
        "DROP TRIGGER trg_enderecos_pk",
    ]

    print("Iniciando a remoção de objetos do banco de dados...")
    for command in drop_commands:
        try:
            oracle.executeDDL(command)
            print(f"✅ Executado: {command}")
        except Exception as e:
            error_str = str(e)
            # Ignora erros de 'não existe' ao dropar
            if 'ORA-00942' in error_str or 'ORA-02289' in error_str or 'ORA-04080' in error_str:
                print(f"ℹ️ Ignorado (não existe): {command}")
            else:
                print(f"❌ Erro ao executar '{command}': {e}")
    
    oracle.close()
    print("Remoção de objetos do banco de dados concluída.")

if __name__ == '__main__':
    drop_database_objects()