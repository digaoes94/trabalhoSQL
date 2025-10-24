from model.Fornecedor import Fornecedor
from model.Endereco import Endereco
from conexion.oracle_queries import OracleQueries
import pandas as pd # Importação adicionada para garantir que o pd esteja disponível

class Cont_Fornecedor:
    def __init__(self):
        pass

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
        
    def _recupera_fornecedor(self, oracle: OracleQueries, cnpj: str = None) -> Fornecedor:
        """ 
        Método interno para buscar os dados de Fornecedor e Endereco no BD e instanciar o objeto Fornecedor completo.
        Retorna o objeto Fornecedor ou None se não encontrado.
        """
        if cnpj is None:
            return None
            
        # Assumindo que a tabela FORNECEDORES e ENDERECOS estão ligadas por uma chave (ex: id_fornecedor)
        # Atenção: Esta SELECT usa 'razaoSocial' e 'nomeFantasia' conforme o seu código Python.
        # CERTIFIQUE-SE que seu create_tables.sql foi ajustado!
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
                numero=int(fornecedor_data["numero"]) if pd.notna(fornecedor_data["numero"]) and str(fornecedor_data["numero"]).isdigit() else None,
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

    def _recupera_id_fornecedor(self, oracle: OracleQueries, cnpj: str = None) -> int:
        """
        Método auxiliar para buscar apenas o ID do fornecedor pelo CNPJ.
        Retorna o ID do fornecedor ou None se não encontrado.
        """
        if cnpj is None:
            return None

        query = f"SELECT id_fornecedor, nomeFantasia FROM fornecedores WHERE cnpj = '{cnpj}'"
        df_fornecedor = oracle.sqlToDataFrame(query)

        if df_fornecedor.empty:
            return None
        else:
            return int(df_fornecedor.iloc[0]["id_fornecedor"])

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

            # Validar Estado (UF)
            while True:
                try:
                    estado_entrada = input("Estado (UF) (ex: ES, SP, RJ ou nome completo): ")
                    estado = self._validar_uf(estado_entrada)
                    break
                except ValueError as e:
                    print(f"❌ {e}")
                    continue
            
            # Cria objetos Modelo
            try:
                num_int = int(numero)
            except ValueError:
                num_int = None
                print("Aviso: Número inválido. Definido como Nulo na inserção do Endereço.")
                
            endereco = Endereco(cep, logradouro, num_int, complemento, bairro, cidade, estado)
            # O Fornecedor será instanciado sem o ID, que será gerado pelo BD
            novo_fornecedor = Fornecedor(cnpj=cnpj, razaoSocial=razao_social, nomeFantasia=nome_fantasia, endereco=endereco, email=email, telefone=[telefone_str])

            # 2. Insere e persiste o novo Fornecedor (usando sequence)
            # ESTE É O BLOCO CORRIGIDO. Presume-se que 'razaoSocial' e 'nomeFantasia' existem.
            sql_fornecedor = f"""
                INSERT INTO fornecedores (id_fornecedor, cnpj, razaoSocial, nomeFantasia, email, telefone) 
                VALUES (fornecedores_id_seq.NEXTVAL, '{cnpj}', '{razao_social}', '{nome_fantasia}', '{email}', '{telefone_str}')
            """
            oracle.write(sql_fornecedor)

            # Recupera o ID do fornecedor recém-inserido
            query_id_fornecedor = "SELECT fornecedores_id_seq.CURRVAL AS id_fornecedor FROM DUAL"
            df_id_fornecedor = oracle.sqlToDataFrame(query_id_fornecedor)
            id_fornecedor_gerado = int(df_id_fornecedor.id_fornecedor.values[0])

            # 1. Insere e persiste o novo Endereço (tabela dependente)
            sql_endereco = f"""
                INSERT INTO enderecos (id_endereco, cep, logradouro, numero, complemento, bairro, cidade, estado, id_fornecedor)
                VALUES (enderecos_id_seq.NEXTVAL, '{cep}', '{logradouro}', {num_int if num_int is not None else 'NULL'}, '{complemento}', '{bairro}', '{cidade}', '{estado}', {id_fornecedor_gerado})
            """
            oracle.write(sql_endereco)
            
            # Atualiza o ID no objeto Python
            novo_fornecedor.setIDFornecedor(id_fornecedor_gerado)

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
            # Recupera o ID do fornecedor de forma segura
            id_fornecedor = self._recupera_id_fornecedor(oracle, cnpj)

            if id_fornecedor is None:
                print(f"Erro ao recuperar dados do fornecedor com CNPJ {cnpj}.")
                return None

            # Tenta recuperar o fornecedor completo (com endereço)
            fornecedor_existente = self._recupera_fornecedor(oracle, cnpj)

            # Exibe dados atuais (com tratamento para quando não tem endereço)
            if fornecedor_existente:
                print(f"\nDados atuais do Fornecedor: CNPJ: {fornecedor_existente.cnpj} | Nome Fantasia: {fornecedor_existente.nomeFantasia}")
            else:
                # Se não tem endereço, busca informações básicas
                query_info = f"SELECT cnpj, razaoSocial, nomeFantasia, email, telefone FROM fornecedores WHERE cnpj = '{cnpj}'"
                df_info = oracle.sqlToDataFrame(query_info)
                if not df_info.empty:
                    info = df_info.iloc[0]
                    print(f"\nDados atuais do Fornecedor:")
                    print(f"  CNPJ: {info['cnpj']} | Razão Social: {info['razaoSocial']} | Nome Fantasia: {info['nomeFantasia']}")
                    print(f"  Email: {info['email']} | Telefone: {info['telefone']}")
                    print("  Obs: Endereço não cadastrado para este fornecedor")

            # Coleta dados atuais para usar como padrão
            query_fornecedor_data = f"SELECT razaoSocial, nomeFantasia, email, telefone FROM fornecedores WHERE cnpj = '{cnpj}'"
            df_fornecedor_data = oracle.sqlToDataFrame(query_fornecedor_data)
            if df_fornecedor_data.empty:
                print("Erro ao recuperar dados do fornecedor.")
                return None

            fornecedor_data = df_fornecedor_data.iloc[0]
            razao_atual = fornecedor_data["razaoSocial"]
            fantasia_atual = fornecedor_data["nomeFantasia"]
            email_atual = fornecedor_data["email"]
            telefone_atual = fornecedor_data["telefone"]

            # Coleta novos dados do Fornecedor
            nova_razao = input(f"Nova Razão Social (Atual: {razao_atual}): ") or razao_atual
            novo_nome_fantasia = input(f"Novo Nome Fantasia (Atual: {fantasia_atual}): ") or fantasia_atual
            novo_email = input(f"Novo E-mail (Atual: {email_atual}): ") or email_atual
            novo_telefone = input(f"Novo Telefone (Atual: {telefone_atual}): ") or telefone_atual

            # Coleta novos dados do Endereço (se existir)
            endereco_para_atualizar = False
            novo_logradouro = None
            novo_numero = None

            # Verifica se existe endereço cadastrado
            query_endereco = f"SELECT logradouro, numero FROM enderecos WHERE id_fornecedor = {id_fornecedor}"
            df_endereco = oracle.sqlToDataFrame(query_endereco)

            if not df_endereco.empty:
                endereco_para_atualizar = True
                endereco_data = df_endereco.iloc[0]
                logradouro_atual = endereco_data["logradouro"]
                numero_atual = endereco_data["numero"]

                novo_logradouro = input(f"Novo Logradouro (Atual: {logradouro_atual}): ") or logradouro_atual
                novo_numero = input(f"Novo Número (Atual: {numero_atual}): ") or str(numero_atual)
            else:
                print("  ⚠️  Este fornecedor não possui endereço cadastrado")
                deseja_cadastrar = input("  Deseja cadastrar um endereço agora? (s/n): ").lower()
                if deseja_cadastrar == 's':
                    # Aqui você poderia implementar lógica para adicionar endereço
                    print("  Funcionalidade de adicionar endereço ainda não implementada")

            # 1. Atualiza no BD (FORNECEDORES)
            sql_update_forn = f"""
                UPDATE fornecedores
                SET razaoSocial = '{nova_razao}', nomeFantasia = '{novo_nome_fantasia}', email = '{novo_email}', telefone = '{novo_telefone}'
                WHERE cnpj = '{cnpj}'
            """
            oracle.write(sql_update_forn)

            # 2. Atualiza no BD (ENDERECOS) se existir
            if endereco_para_atualizar:
                try:
                    num_int_update = int(novo_numero)
                except ValueError:
                    num_int_update = 'NULL'

                sql_update_endereco = f"""
                    UPDATE enderecos
                    SET logradouro = '{novo_logradouro}', numero = {num_int_update}
                    WHERE id_fornecedor = {id_fornecedor}
                """
                oracle.write(sql_update_endereco)

            # Recupera o fornecedor atualizado
            fornecedor_atualizado = self._recupera_fornecedor(oracle, cnpj)

            print("\n✅ Fornecedor atualizado com sucesso!")
            if fornecedor_atualizado:
                print(f"CNPJ: {fornecedor_atualizado.cnpj} | Nome Fantasia: {fornecedor_atualizado.nomeFantasia}")
            else:
                # Mostra informações básicas se não conseguir recuperar com endereço
                query_final = f"SELECT cnpj, razaoSocial, nomeFantasia FROM fornecedores WHERE cnpj = '{cnpj}'"
                df_final = oracle.sqlToDataFrame(query_final)
                if not df_final.empty:
                    info = df_final.iloc[0]
                    print(f"CNPJ: {info['cnpj']} | Razão Social: {info['razaoSocial']} | Nome Fantasia: {info['nomeFantasia']}")

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
            # Recupera o ID do fornecedor de forma segura (sem necessidade de endereço)
            id_fornecedor = self._recupera_id_fornecedor(oracle, cnpj)

            if id_fornecedor is None:
                print(f"Erro ao recuperar dados do fornecedor com CNPJ {cnpj}.")
                return

            # Verifica se existem compras associadas ao fornecedor
            query_compras = f"SELECT COUNT(*) as qtde FROM compras WHERE id_fornecedor = {id_fornecedor}"
            df_compras = oracle.sqlToDataFrame(query_compras)
            qtde_compras = int(df_compras.iloc[0]["qtde"])

            if qtde_compras > 0:
                # Busca o nome fantasia do fornecedor para exibição
                query_nome = f"SELECT nomeFantasia FROM fornecedores WHERE id_fornecedor = {id_fornecedor}"
                df_nome = oracle.sqlToDataFrame(query_nome)
                nome_fantasia = df_nome.iloc[0]["nomeFantasia"] if not df_nome.empty else "Desconhecido"

                print(f"\n⚠️  Não é possível excluir o fornecedor '{nome_fantasia}'")
                print(f"Motivo: Existem {qtde_compras} compra(s) associada(s) a este fornecedor")
                print("\n💡 Dica: Remova as compras associadas antes de deletar o fornecedor.")
                return

            # Recupera os dados do fornecedor antes de excluir para exibição (tenta, mas não garante endereço)
            fornecedor_excluido = self._recupera_fornecedor(oracle, cnpj)

            # 1. Deleta Endereço (tabela dependente)
            sql_del_endereco = f"DELETE FROM enderecos WHERE id_fornecedor = {id_fornecedor}"
            oracle.write(sql_del_endereco)

            # 2. Deleta Fornecedor (tabela principal)
            sql_del_forn = f"DELETE FROM fornecedores WHERE cnpj = '{cnpj}'"
            oracle.write(sql_del_forn)

            print("\n✅ Fornecedor Removido com Sucesso!")
            if fornecedor_excluido:
                print(f"CNPJ: {fornecedor_excluido.cnpj} | Nome Fantasia: {fornecedor_excluido.nomeFantasia}")
            else:
                # Se não conseguiu recuperar com endereço, mostra informações básicas
                query_info = f"SELECT cnpj, razaoSocial, nomeFantasia FROM fornecedores WHERE cnpj = '{cnpj}' AND ROWNUM = 1"
                df_info = oracle.sqlToDataFrame(query_info)
                if not df_info.empty:
                    info = df_info.iloc[0]
                    print(f"CNPJ: {info['cnpj']} | Razão Social: {info['razaoSocial']} | Nome Fantasia: {info['nomeFantasia']}")
            
    def verPedidos(self):
        # O método 'verPedidos' para Fornecedor será interpretado como 'ver Compras'
        oracle = OracleQueries(can_write=False)
        oracle.connect()

        cnpj = input("Informe o CNPJ do Fornecedor para ver as compras (Pedidos): ")
        
        if self.verifica_existencia_fornecedor(oracle, cnpj):
            print(f"O CNPJ {cnpj} não existe.")
        else:
            fornecedor = self._recupera_fornecedor(oracle, cnpj) # Recupera o objeto fornecedor
            
            if fornecedor is None:
                 print(f"Erro ao recuperar o fornecedor {cnpj}.")
                 return None

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
            
            # Agrupa os itens pela compra (pedido)
            for id_compra, grupo in df_pedidos.groupby('id_compra'):
                # Garante que a coluna 'data_compra' está sendo usada para a data
                data = grupo['data_compra'].iloc[0] 
                data_str = data.strftime('%d/%m/%Y') if hasattr(data, 'strftime') else str(data)
                
                print(f"\n{data_str} – ID Compra: {id_compra} – Total da Compra: R$ {grupo['subtotal'].sum():.2f}")
                
                # Lista os itens da compra
                for _, row in grupo.iterrows():
                    print(f"   - Produto: {row['nome_produto']} | Qtd: {row['quantidade']} | Preço Un.: R$ {row['preco_unitario_compra']:.2f} | Subtotal: R$ {row['subtotal']:.2f}")