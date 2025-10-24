from model.Cliente import Cliente
from model.Endereco import Endereco
from conexion.oracle_queries import OracleQueries
import pandas as pd
import re

class Cont_Cliente:
    def __init__(self):
        pass

    def _validar_e_formatar_cep(self, cep: str) -> str:
        """
        Valida e formata o CEP.
        Aceita: "12345678" ou "12345-678"
        Retorna: "12345-678" (formato padrão com hífen)
        """
        # Remove espaços em branco
        cep = cep.strip()

        # Remove hífen se existir
        cep_sem_hifen = cep.replace('-', '')

        # Verifica se tem 8 dígitos
        if not cep_sem_hifen.isdigit() or len(cep_sem_hifen) != 8:
            raise ValueError(f"CEP inválido: '{cep}'. Deve conter 8 dígitos (ex: 12345-678 ou 12345678)")

        # Formata com hífen: XXXXX-XXX
        cep_formatado = f"{cep_sem_hifen[:5]}-{cep_sem_hifen[5:]}"
        return cep_formatado

    def _validar_uf(self, estado: str) -> str:
        """
        Valida e formata o Estado (UF).
        Aceita: "ES" ou "es" ou "Espírito Santo" ou "espirito santo"
        Retorna: "ES" (código UF em maiúscula)
        """
        import unicodedata

        # Dicionário de Estados Brasileiros
        estados_map = {
            'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
            'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
            'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
            'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
            'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
        }

        estado = estado.strip().upper()

        # Se for um código de 2 letras válido
        if len(estado) == 2 and estado in estados_map:
            return estado

        # Função para remover acentos
        def remove_acentos(text):
            nfkd = unicodedata.normalize('NFKD', text)
            return ''.join([c for c in nfkd if not unicodedata.combining(c)])

        # Se for um nome de estado, encontrar o código
        estado_sem_acentos = remove_acentos(estado)
        for uf, nome in estados_map.items():
            nome_sem_acentos = remove_acentos(nome.upper())
            if estado_sem_acentos == nome_sem_acentos:
                return uf

        # Se nenhuma opção funcionar, listar as válidas
        uf_validos = ", ".join(sorted(estados_map.keys()))
        raise ValueError(
            f"Estado inválido: '{estado}'\n"
            f"Use o código UF com 2 letras (ex: ES, SP, RJ)\n"
            f"UFs válidos: {uf_validos}"
        )

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
            
            print("--- Dados do Cliente ---")
            nome = input("Nome do Cliente: ")
            email = input("E-mail: ")
            telefone_str = input("Telefone: ")
            
            print("--- Dados do Endereço ---")
            while True:
                try:
                    cep_entrada = input("CEP (formato: 12345-678 ou 12345678): ")
                    cep = self._validar_e_formatar_cep(cep_entrada)
                    break
                except ValueError as e:
                    print(f"❌ {e}")
                    continue
            logradouro = input("Logradouro: ")
            numero = input("Número: ")
            complemento = input("Complemento (opcional): ")
            bairro = input("Bairro: ")
            cidade = input("Cidade: ")

            # Validar Estado (UF)
            while True:
                try:
                    estado_entrada = input("Estado (UF) (ex: ES, SP, RJ ou nome completo): ")
                    estado = self._validar_uf(estado_entrada)
                    break
                except ValueError as e:
                    print(f"❌ {e}")
                    continue
            
            sql_cliente = f"""
                INSERT INTO clientes (cpf, nome, email, telefone)
                VALUES ('{cpf}', '{nome}', '{email}', '{telefone_str}')
            """
            oracle.write(sql_cliente)

            query_id_cliente = "SELECT clientes_id_seq.CURRVAL AS id_cliente FROM DUAL"
            df_id_cliente = oracle.sqlToDataFrame(query_id_cliente)
            id_cliente_gerado = int(df_id_cliente.id_cliente.values[0])

            sql_endereco = f"""
                INSERT INTO enderecos (id_endereco, cep, logradouro, numero, complemento, bairro, cidade, estado, id_cliente)
                VALUES (enderecos_id_seq.NEXTVAL, '{cep}', '{logradouro}', {int(numero) if numero else 'NULL'}, '{complemento}', '{bairro}', '{cidade}', '{estado}', {id_cliente_gerado})
            """
            oracle.write(sql_endereco)

            novo_cliente = self._recupera_cliente(oracle, cpf)

            print("\nCliente cadastrado com sucesso!")
            print(novo_cliente.to_string())
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
                data = grupo['data_venda'].iloc[0]
                data_str = data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else str(data)
                
                print(f"\n{data_str} – ID Venda: {id_venda} – Total da Venda: R$ {grupo['subtotal'].sum():.2f}")
                
                # Lista os itens da venda
                for index, row in grupo.iterrows():
                    print(f"   - Produto: {row['nome_produto']} | Qtd: {row['quantidade']} | Preço Un.: R$ {row['preco_unitario_venda']:.2f} | Subtotal: R$ {row['subtotal']:.2f}")