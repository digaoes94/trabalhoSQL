from conexion.oracle_queries import OracleQueries

def create_tables(query:str):
    list_of_commands = query.split(';')

    oracle = OracleQueries(can_write=True)
    oracle.connect()

    for command in list_of_commands:    
        if len(command.strip()) > 0: # garante que não executa comandos vazios
            print(f"Executing: {command.strip()}")
            try:
                oracle.executeDDL(command)
                print("Successfully executed")
            except Exception as e:
                print(f"Error executing command: {e}")            

def run():

    with open("sql/create_tables.sql", "r") as f:
        query_create = f.read()

    print("Creating tables...")
    create_tables(query=query_create)
    print("Tables successfully created!")

 
if __name__ == '__main__':
    run()
