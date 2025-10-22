from model.Fornecedor import Fornecedor
from model.Endereco import Endereco
from conexion.oracle_queries import OracleQueries

class Cont_Fornecedor:
    def __init__(self):
        pass
        
    def _recupera_fornecedor(self, oracle: OracleQueries, cnpj: str = None) -> Fornecedor:
        """ 
        Método interno para buscar os dados de Fornecedor e Endereco no BD e instanciar o objeto Fornecedor completo.
        Retorna o objeto Fornecedor ou None se não encontrado.
        """
        if cnpj is None:
            return None
            
        # Assumindo que a tabela FORNECEDORES e ENDERECOS estão ligadas por uma chave (ex: cnpj_fornecedor = cnpj)
        query = f"""
            SELECT 
                f.id_fornecedor, f.cnpj, f.razaoSocial, f.nomeFantasia, f.email, f.telefone, 
                e.cep, e.logradouro, e.numero, e.complemento, e.bairro, e.cidade, e.estado 
            FROM fornecedores f 
            INNER JOIN enderecos e ON f.id_fornecedor = e.id_fornecedor 
            WHERE f.cnpj = '{cnpj}'
        """
        
        df_fornecedor = oracle.sqlToDataFrame(query)

        if df_fornecedor.empty:
            return None
        else:
            fornecedor_data = df_fornecedor.iloc[0]
            
            # 1. Cria o objeto Endereco
            endereco = Endereco(
                cep=fornecedor_data["cep"],
                logradouro=fornecedor_data["logradouro"],
                numero=int(fornecedor_data["numero"]) if pd.notna(fornecedor_data["numero"]) else None,
                complemento=fornecedor_data["complemento"],
                bairro=fornecedor_data["bairro"],
                cidade=fornecedor_data["cidade"],
                estado=fornecedor_data["estado"]
            )
            
            # 2. Cria o objeto Fornecedor
            # O campo 'telefone' é uma lista no model, mas vem como string do BD.
            telefone_lista = [fornecedor_data["telefone"]] if pd.notna(fornecedor_data["telefone"]) else []
            
            fornecedor = Fornecedor(
                id_fornecedor=int(fornecedor_data["id_fornecedor"]),
                cnpj=fornecedor_data["cnpj"],
                razaoSocial=fornecedor_data["razaoSocial"],
                nomeFantasia=fornecedor_data["nomeFantasia"],
                endereco=endereco,
                email=fornecedor_data["email"],
                telefone=telefone_lista
            )
            return fornecedor
            
    def verifica_existencia_fornecedor(self, oracle:OracleQueries, cnpj:str=None) -> bool:
        """
        Verifica se o Fornecedor *NÃO* existe no BD (DataFrame vazio).
        (Retorna True se o fornecedor *pode* ser inserido)
        """
        query = f"SELECT cnpj FROM fornecedores WHERE cnpj = '{cnpj}'"
        df_fornecedor = oracle.sqlToDataFrame(query)
        return df_fornecedor.empty

    # ---------------------------------------------------------------------------
    # MÉTODOS CRUD SOLICITADOS
    # ---------------------------------------------------------------------------
    
    def pesquisarFornecedor(self) -> Fornecedor:
        oracle = OracleQueries(can_write=False)
        oracle.connect()

        cnpj = input("Informe o CNPJ do Fornecedor que deseja pesquisar: ")
        fornecedor = self._recupera_fornecedor(oracle, cnpj)

        if fornecedor is None:
            print(f"O CNPJ {cnpj} não existe.")
        else:
            print("\nFornecedor Encontrado:")
            print(f"CNPJ: {fornecedor.cnpj} | Nome Fantasia: {fornecedor.nomeFantasia} | Razão Social: {fornecedor.razaoSocial}")
            print(f"E-mail: {fornecedor.email} | Telefone: {fornecedor.telefone[0] if fornecedor.telefone else 'N/A'}")
            print(f"Endereço: {fornecedor.endereco.to_string()}")
            
        return fornecedor

    def novoFornecedor(self) -> Fornecedor:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cnpj = input("CNPJ (Novo): ")

        # verifica_existencia_fornecedor retorna True se o fornecedor *NÃO* existe
        if self.verifica_existencia_fornecedor(oracle, cnpj):
            
            # Coleta dados do Fornecedor
            print("--- Dados do Fornecedor ---")
            razao_social = input("Razão Social: ")
            nome_fantasia = input("Nome Fantasia: ")
            email = input("E-mail: ")
            telefone_str = input("Telefone: ")
            
            # Coleta dados do Endereço
            print("--- Dados do Endereço ---")
            cep = input("CEP: ")
            logradouro = input("Logradouro: ")
            numero = input("Número: ")
            complemento = input("Complemento (opcional): ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")
            estado = input("Estado (UF): ")
            
            # Cria objetos Modelo
            endereco = Endereco(cep, logradouro, int(numero), complemento, bairro, cidade, estado)
            novo_fornecedor = Fornecedor(cnpj, razao_social, nome_fantasia, endereco, email, [telefone_str])

            # 2. Insere e persiste o novo Fornecedor
            sql_fornecedor = f"""
                INSERT INTO fornecedores (cnpj, razaoSocial, nomeFantasia, email, telefone) 
                VALUES ('{cnpj}', '{razao_social}', '{nome_fantasia}', '{email}', '{telefone_str}')
            """
            oracle.write(sql_fornecedor)

            # Recupera o ID do fornecedor recém-inserido
            query_id_fornecedor = "SELECT fornecedores_id_seq.CURRVAL AS id_fornecedor FROM DUAL"
            df_id_fornecedor = oracle.sqlToDataFrame(query_id_fornecedor)
            id_fornecedor_gerado = int(df_id_fornecedor.id_fornecedor.values[0])

            # 1. Insere e persiste o novo Endereço (tabela dependente)
            sql_endereco = f"""
                INSERT INTO enderecos (cep, logradouro, numero, complemento, bairro, cidade, estado, id_fornecedor) 
                VALUES ('{cep}', '{logradouro}', {int(numero)}, '{complemento}', '{bairro}', '{cidade}', '{estado}', {id_fornecedor_gerado})
            """
            oracle.write(sql_endereco)
            
            print("\nFornecedor cadastrado com sucesso!")
            print(f"CNPJ: {novo_fornecedor.cnpj} | Nome Fantasia: {novo_fornecedor.nomeFantasia}")
            return novo_fornecedor
        else:
            print(f"O CNPJ {cnpj} já está cadastrado.")
            return None

    def atualizarFornecedor(self) -> Fornecedor:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cnpj = input("CNPJ do Fornecedor que deseja alterar: ")

        # Verifica se o fornecedor existe na base de dados (se retorna True, NÃO existe)
        if self.verifica_existencia_fornecedor(oracle, cnpj):
            print(f"O CNPJ {cnpj} não existe.")
            return None
        else:
            fornecedor_existente = self._recupera_fornecedor(oracle, cnpj)
            print(f"\nDados atuais do Fornecedor: CNPJ: {fornecedor_existente.cnpj} | Nome Fantasia: {fornecedor_existente.nomeFantasia}")
            
            # Coleta novos dados do Fornecedor
            nova_razao = input(f"Nova Razão Social (Atual: {fornecedor_existente.razaoSocial}): ") or fornecedor_existente.razaoSocial
            novo_nome_fantasia = input(f"Novo Nome Fantasia (Atual: {fornecedor_existente.nomeFantasia}): ") or fornecedor_existente.nomeFantasia
            novo_email = input(f"Novo E-mail (Atual: {fornecedor_existente.email}): ") or fornecedor_existente.email
            novo_telefone = input(f"Novo Telefone (Atual: {fornecedor_existente.telefone[0] if fornecedor_existente.telefone else 'N/A'}): ") or (fornecedor_existente.telefone[0] if fornecedor_existente.telefone else '')
            
            # Coleta novos dados do Endereço (Logradouro e Número como exemplo)
            endereco_atual = fornecedor_existente.endereco
            novo_logradouro = input(f"Novo Logradouro (Atual: {endereco_atual.logradouro}): ") or endereco_atual.logradouro
            novo_numero = input(f"Novo Número (Atual: {endereco_atual.numero}): ") or str(endereco_atual.numero)
            
            # 1. Atualiza no BD (FORNECEDORES)
            sql_update_forn = f"""
                UPDATE fornecedores 
                SET razao_social = '{nova_razao}', nome_fantasia = '{novo_nome_fantasia}', email = '{novo_email}', telefone = '{novo_telefone}' 
                WHERE cnpj = '{cnpj}'
            """
            oracle.write(sql_update_forn)
            
            # 2. Atualiza no BD (ENDERECOS)
            sql_update_endereco = f"""
                UPDATE enderecos 
                SET logradouro = '{novo_logradouro}', numero = {int(novo_numero)}
                WHERE id_fornecedor = {fornecedor_existente.id_fornecedor}
            """
            oracle.write(sql_update_endereco)
            
            # Recupera o fornecedor atualizado
            fornecedor_atualizado = self._recupera_fornecedor(oracle, cnpj)
            
            print("\nFornecedor atualizado com sucesso!")
            print(f"CNPJ: {fornecedor_atualizado.cnpj} | Nome Fantasia: {fornecedor_atualizado.nomeFantasia}")
            return fornecedor_atualizado

    def deletarFornecedor(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cnpj = input("CNPJ do Fornecedor que irá excluir: ")        

        # Verifica se o fornecedor existe na base de dados
        if self.verifica_existencia_fornecedor(oracle, cnpj):            
            print(f"O CNPJ {cnpj} não existe.")
        else:
            fornecedor_excluido = self._recupera_fornecedor(oracle, cnpj)
            
            # 1. Deleta Endereço (tabela dependente)
            sql_del_endereco = f"DELETE FROM enderecos WHERE id_fornecedor = {fornecedor_excluido.id_fornecedor}"
            oracle.write(sql_del_endereco)
            
            # 2. Deleta Fornecedor (tabela principal)
            sql_del_forn = f"DELETE FROM fornecedores WHERE cnpj = '{cnpj}'"
            oracle.write(sql_del_forn)
            
            print("Fornecedor Removido com Sucesso!")
            print(f"CNPJ: {fornecedor_excluido.cnpj} | Nome Fantasia: {fornecedor_excluido.nomeFantasia}")
            
    def verPedidos(self):
        # O método 'verPedidos' para Fornecedor será interpretado como 'ver Compras'
        oracle = OracleQueries(can_write=False)
        oracle.connect()

        cnpj = input("Informe o CNPJ do Fornecedor para ver as compras (Pedidos): ")
        
        if self.verifica_existencia_fornecedor(oracle, cnpj):
            print(f"O CNPJ {cnpj} não existe.")
        else:
            fornecedor = self._recupera_fornecedor(oracle, cnpj) # Recupera o objeto fornecedor
            # Busca as compras (pedidos) do fornecedor com seus itens.
            query_pedidos = f"""
                SELECT 
                    c.data_compra, c.id_compra, p.nome as nome_produto, 
                    ic.preco_unitario_compra, ic.quantidade, ic.subtotal
                FROM compras c
                INNER JOIN item_compra ic ON c.id_compra = ic.id_compra
                INNER JOIN produtos p ON ic.id_produto = p.id_produto
                WHERE c.id_fornecedor = {fornecedor.id_fornecedor}
                ORDER BY c.data_compra, c.id_compra
            """
            
            df_pedidos = oracle.sqlToDataFrame(query_pedidos)
            
            if df_pedidos.empty:
                print(f"O Fornecedor de CNPJ {cnpj} não possui compras registradas.")
                return None
            
            print(f"\n--- Compras (Pedidos) do Fornecedor (CNPJ: {cnpj}) ---")
            
            try:
                import pandas as pd
                # Agrupa os itens pela compra (pedido)
                for id_compra, grupo in df_pedidos.groupby('id_compra'):
                    data = grupo['data'].iloc[0]
                    data_str = data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else str(data)
                    
                    print(f"\n{data_str} – ID Compra: {id_compra} – Total da Compra: R$ {grupo['subtotal'].sum():.2f}")
                    
                    # Lista os itens da compra
                    for index, row in grupo.iterrows():
                        print(f"   - Produto: {row['nome_produto']} | Qtd: {row['quantidade']} | Preço Un.: R$ {row['preco_unitario_compra']:.2f} | Subtotal: R$ {row['subtotal']:.2f}")
            except ImportError:
                 # Tratamento de erro caso o pandas não esteja disponível
                 print("Aviso: Falha ao formatar relatorio (Pandas não disponível). Exibindo resultados brutos:")
                 print(df_pedidos.to_string())