from model.Cliente import Cliente
from model.Endereco import Endereco
from conexion.oracle_queries import OracleQueries

class Cont_Cliente:
    def __init__(self):
        pass
        
    def _recupera_cliente(self, oracle: OracleQueries, cpf: str = None) -> Cliente:
        """ 
        Método interno para buscar os dados de Cliente e Endereco no BD e instanciar o objeto Cliente completo.
        Retorna o objeto Cliente ou None se não encontrado.
        """
        if cpf is None:
            return None
            
        # Assumindo que a tabela CLIENTES e ENDERECOS estão ligadas por uma chave (ex: cpf_cliente = cpf)
        query = f"""
            SELECT 
                c.id_cliente, c.cpf, c.nome, c.email, c.telefone, 
                e.cep, e.logradouro, e.numero, e.complemento, e.bairro, e.cidade, e.estado 
            FROM clientes c 
            INNER JOIN enderecos e ON c.id_cliente = e.id_cliente 
            WHERE c.cpf = '{cpf}'
        """
        
        df_cliente = oracle.sqlToDataFrame(query)

        if df_cliente.empty:
            return None
        else:
            cliente_data = df_cliente.iloc[0]
            
            # 1. Cria o objeto Endereco
            endereco = Endereco(
                cep=cliente_data["cep"],
                logradouro=cliente_data["logradouro"],
                # Garante que numero é int
                numero=int(cliente_data["numero"]) if pd.notna(cliente_data["numero"]) else None,
                complemento=cliente_data["complemento"],
                bairro=cliente_data["bairro"],
                cidade=cliente_data["cidade"],
                estado=cliente_data["estado"]
            )
            
            # 2. Cria o objeto Cliente
            # O campo 'telefone' é uma lista no model, mas vem como string do BD.
            telefone_lista = [cliente_data["telefone"]] if pd.notna(cliente_data["telefone"]) else []
            
            cliente = Cliente(
                id_cliente=int(cliente_data["id_cliente"]),
                cpf=cliente_data["cpf"],
                nome=cliente_data["nome"],
                endereco=endereco,
                email=cliente_data["email"],
                telefone=telefone_lista
            )
            return cliente
            
    def verifica_existencia_cliente(self, oracle:OracleQueries, cpf:str=None) -> bool:
        """
        Verifica se o Cliente *NÃO* existe no BD (DataFrame vazio).
        (Logica do professor, onde True significa que o cliente *pode* ser inserido)
        """
        query = f"SELECT cpf, nome FROM clientes WHERE cpf = '{cpf}'"
        df_cliente = oracle.sqlToDataFrame(query)
        return df_cliente.empty

    # ---------------------------------------------------------------------------
    # MÉTODOS CRUD SOLICITADOS
    # ---------------------------------------------------------------------------
    
    def pesquisarCliente(self) -> Cliente:
        oracle = OracleQueries(can_write=False)
        oracle.connect()

        cpf = input("Informe o CPF do Cliente que deseja pesquisar: ")
        cliente = self._recupera_cliente(oracle, cpf)

        if cliente is None:
            print(f"O CPF {cpf} não existe.")
        else:
            print("\nCliente Encontrado:")
            print(cliente.to_string())
            print(f"Endereço: {cliente.endereco.to_string()}")
            
        return cliente

    def novoCliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        # verifica_existencia_cliente retorna True se o cliente *NÃO* existe
        if self.verifica_existencia_cliente(oracle, cpf):
            
            # Coleta dados do Cliente
            print("--- Dados do Cliente ---")
            nome = input("Nome do Cliente: ")
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
            
            # 2. Insere e persiste o novo Cliente (usando sequence manualmente)
            sql_cliente = f"""
                INSERT INTO clientes (id_cliente, cpf, nome, email, telefone) 
                VALUES (clientes_id_seq.NEXTVAL, '{cpf}', '{nome}', '{email}', '{telefone_str}')
            """
            oracle.write(sql_cliente)

            # Recupera o ID do cliente recém-inserido
            query_id_cliente = "SELECT clientes_id_seq.CURRVAL AS id_cliente FROM DUAL"
            df_id_cliente = oracle.sqlToDataFrame(query_id_cliente)
            id_cliente_gerado = int(df_id_cliente.id_cliente.values[0])

            # 1. Insere e persiste o novo Endereço (tabela dependente) - usando sequence
            sql_endereco = f"""
                INSERT INTO enderecos (id_endereco, cep, logradouro, numero, complemento, bairro, cidade, estado, id_cliente) 
                VALUES (enderecos_id_seq.NEXTVAL, '{cep}', '{logradouro}', {int(numero)}, '{complemento}', '{bairro}', '{cidade}', '{estado}', {id_cliente_gerado})
            """
            oracle.write(sql_endereco)

            # 3. Recupera o objeto Cliente completo para retorno
            novo_cliente = self._recupera_cliente(oracle, cpf)
            
            # Exibe os atributos do novo cliente
            print("\nCliente cadastrado com sucesso!")
            print(novo_cliente.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizarCliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = input("CPF do cliente que deseja alterar: ")

        # Verifica se o cliente existe na base de dados (se retorna True, NÃO existe)
        if self.verifica_existencia_cliente(oracle, cpf):
            print(f"O CPF {cpf} não existe.")
            return None
        else:
            # Recupera o cliente existente para preencher os valores antigos (melhor experiência do usuário)
            cliente_existente = self._recupera_cliente(oracle, cpf)
            print(f"\nDados atuais do Cliente: {cliente_existente.to_string()}")
            print(f"Endereço atual: {cliente_existente.endereco.to_string()}")
            
            # Coleta novos dados do Cliente
            novo_nome = input(f"Novo nome (Atual: {cliente_existente.nome}): ") or cliente_existente.nome
            novo_email = input(f"Novo e-mail (Atual: {cliente_existente.email}): ") or cliente_existente.email
            # Assume que telefone é o primeiro item da lista
            novo_telefone = input(f"Novo telefone (Atual: {cliente_existente.telefone[0] if cliente_existente.telefone else 'N/A'}): ") or (cliente_existente.telefone[0] if cliente_existente.telefone else '')
            
            # Coleta novos dados do Endereço (simplificado para Logradouro e Número, mas pode ser estendido)
            endereco_atual = cliente_existente.endereco
            novo_logradouro = input(f"Novo Logradouro (Atual: {endereco_atual.logradouro}): ") or endereco_atual.logradouro
            novo_numero = input(f"Novo Número (Atual: {endereco_atual.numero}): ") or str(endereco_atual.numero)
            
            # 1. Atualiza no BD (CLIENTES)
            sql_update_cliente = f"""
                UPDATE clientes 
                SET nome = '{novo_nome}', email = '{novo_email}', telefone = '{novo_telefone}' 
                WHERE cpf = '{cpf}'
            """
            oracle.write(sql_update_cliente)
            
            # 2. Atualiza no BD (ENDERECOS)
            sql_update_endereco = f"""
                UPDATE enderecos 
                SET logradouro = '{novo_logradouro}', numero = {int(novo_numero)}
                WHERE id_cliente = {cliente_existente.id_cliente}
            """
            oracle.write(sql_update_endereco)
            
            # 3. Recupera o cliente atualizado
            cliente_atualizado = self._recupera_cliente(oracle, cpf)
            
            print("\nCliente atualizado com sucesso!")
            print(cliente_atualizado.to_string())
            return cliente_atualizado

    def deletarCliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do Cliente a ser excluído
        cpf = input("CPF do Cliente que irá excluir: ")        

        # Verifica se o cliente existe na base de dados
        if self.verifica_existencia_cliente(oracle, cpf):            
            print(f"O CPF {cpf} não existe.")
        else:
            # Recupera os dados do cliente antes de excluir para exibição (modelo do professor)
            cliente_excluido = self._recupera_cliente(oracle, cpf)
            
            # 1. Deleta Endereço (tabela dependente)
            sql_del_endereco = f"DELETE FROM enderecos WHERE id_cliente = {cliente_excluido.id_cliente}"
            oracle.write(sql_del_endereco)
            
            # 2. Deleta Cliente (tabela principal)
            sql_del_cliente = f"DELETE FROM clientes WHERE cpf = '{cpf}'"
            oracle.write(sql_del_cliente)
            
            # Exibe os atributos do cliente excluído
            print("Cliente Removido com Sucesso!")
            print(cliente_excluido.to_string())
            
    def verPedidos(self):
        oracle = OracleQueries(can_write=False) # Apenas leitura
        oracle.connect()

        cpf = input("Informe o CPF do Cliente para ver os pedidos: ")
        
        # Se verifica_existencia_cliente retorna True, o cliente NÃO existe
        if self.verifica_existencia_cliente(oracle, cpf):
            print(f"O CPF {cpf} não existe.")
        else:
            cliente = self._recupera_cliente(oracle, cpf) # Recupera o objeto cliente
            # Busca as vendas (pedidos) do cliente com seus itens.
            query_pedidos = f"""
                SELECT 
                    v.data_venda, v.id_venda, p.nome as nome_produto, 
                    iv.preco_unitario_venda, iv.quantidade, iv.subtotal
                FROM vendas v
                INNER JOIN item_venda iv ON v.id_venda = iv.id_venda
                INNER JOIN produtos p ON iv.id_produto = p.id_produto
                WHERE v.id_cliente = {cliente.id_cliente}
                ORDER BY v.data_venda, v.id_venda
            """
            
            df_pedidos = oracle.sqlToDataFrame(query_pedidos)
            
            if df_pedidos.empty:
                print(f"O Cliente de CPF {cpf} não possui pedidos registrados.")
                return None
            
            print(f"\n--- Pedidos do Cliente (CPF: {cpf}) ---")
            
            # Agrupa os itens pela venda (pedido) para formatar a saída
            # Importante: você pode precisar importar pandas (import pandas as pd)
            try:
                import pandas as pd
                if not isinstance(df_pedidos, pd.DataFrame):
                     print("Erro: A função sqlToDataFrame não retornou um DataFrame.")
                     return
            except ImportError:
                 # Caso pandas não esteja disponível, faz uma iteração simples
                 print("Aviso: Pandas não está importado/disponível. Listando resultados brutos.")
                 print(df_pedidos.to_string())
                 return

            # Agrupa os itens pela venda (pedido)
            for id_venda, grupo in df_pedidos.groupby('id_venda'):
                data = grupo['data'].iloc[0]
                data_str = data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else str(data)
                
                print(f"\n{data_str} – ID Venda: {id_venda} – Total da Venda: R$ {grupo['subtotal'].sum():.2f}")
                
                # Lista os itens da venda
                for index, row in grupo.iterrows():
                    print(f"   - Produto: {row['nome_produto']} | Qtd: {row['quantidade']} | Preço Un.: R$ {row['preco_unitario_venda']:.2f} | Subtotal: R$ {row['subtotal']:.2f}")