from conexion.oracle_queries import OracleQueries

def create_tables(query: str):
    oracle = OracleQueries(can_write=True)
    oracle.connect()

    # divide por ';' mas trata triggers especiais
    commands = query.split(';')
    
    for command in commands:
        command = command.strip()
        if len(command) == 0:
            continue
            
        # se for um trigger, executa como bloco completo
        if 'CREATE OR REPLACE TRIGGER' in command.upper():
            print(f"Executing trigger: {command[:50]}...")
            try:
                oracle.executeDDL(command)
                print("✅ Trigger created successfully")
            except Exception as e:
                print(f"❌ Error creating trigger: {e}")
        else:
            print(f"Executing: {command[:50]}...")
            try:
                oracle.executeDDL(command)
                print("✅ Successfully executed")
            except Exception as e:
                print(f"❌ Error executing command: {e}")

def create_triggers():
    """Cria todos os triggers necessários"""
    oracle = OracleQueries(can_write=True)
    oracle.connect()
    
    triggers = [
        {
            'name': 'CLIENTES',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_clientes_pk
    BEFORE INSERT ON clientes
    FOR EACH ROW
BEGIN
    :new.id_cliente := clientes_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'PRODUTOS',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_produtos_pk
    BEFORE INSERT ON produtos
    FOR EACH ROW
BEGIN
    :new.id_produto := produtos_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'FORNECEDORES',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_fornecedores_pk
    BEFORE INSERT ON fornecedores
    FOR EACH ROW
BEGIN
    :new.id_fornecedor := fornecedores_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'VENDAS',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_vendas_pk
    BEFORE INSERT ON vendas
    FOR EACH ROW
BEGIN
    :new.id_venda := vendas_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'COMPRAS',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_compras_pk
    BEFORE INSERT ON compras
    FOR EACH ROW
BEGIN
    :new.id_compra := compras_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'ITEM_VENDA',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_item_venda_pk
    BEFORE INSERT ON item_venda
    FOR EACH ROW
BEGIN
    :new.id_item_venda := item_venda_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'ITEM_COMPRA',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_item_compra_pk
    BEFORE INSERT ON item_compra
    FOR EACH ROW
BEGIN
    :new.id_item_compra := item_compra_id_seq.NEXTVAL;
END;
'''
        },
        {
            'name': 'ENDERECOS',
            'sql': '''
CREATE OR REPLACE TRIGGER trg_enderecos_pk
    BEFORE INSERT ON enderecos
    FOR EACH ROW
BEGIN
    :new.id_endereco := enderecos_id_seq.NEXTVAL;
END;
'''
        }
    ]
    
    print("🔧 Creating triggers...")
    for trigger in triggers:
        try:
            oracle.executeDDL(trigger['sql'])
            print(f"✅ Trigger {trigger['name']} created successfully")
        except Exception as e:
            print(f"❌ Error creating trigger {trigger['name']}: {e}")
    
    oracle.close()

def run():
    with open("sql/create_tables.sql", "r") as f:
        query_create = f.read()

    print("🏗️ Creating tables and sequences...")
    create_tables(query=query_create)
    
    print("🔧 Creating triggers...")
    create_triggers()
    
    print("🎉 Database setup completed successfully!")
    print("📋 All tables, sequences and triggers are ready!")

if __name__ == '__main__':
    run()
