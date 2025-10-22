# 🏪 Sistema de Vendas - Oracle Database

> Sistema completo de gerenciamento de vendas desenvolvido em Python com integração ao Oracle Database. Interface de linha de comando para gerenciar clientes, fornecedores, produtos, compras e vendas com relatórios detalhados.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)](https://oracle.com)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()

---

## 📚 Informações do Projeto

| Campo | Informação |
|-------|------------|
| **Matéria** | Banco de Dados |
| **Professor** | Howard Roatti |
| **Membros** | Gabriely, Guilherme, Luiz, Ricardo e Rodrigo |
| **Repositório** | [GitHub](https://github.com/digaoes94/trabalhoSQL.git) |
| **Semestre** | 2025/2 |

---

## 🎯 O que o Sistema Faz

O sistema permite gerenciar uma loja completa através de uma interface intuitiva:

- 👥 **Cadastrar clientes e fornecedores** - gestão completa de pessoas
- 📦 **Controlar estoque de produtos** - controle de inventário em tempo real
- 💰 **Registrar compras e vendas** - fluxo completo de transações
- 📊 **Gerar relatórios detalhados** - vendas, estoque e clientes
- ✏️ **Atualizar e remover registros** - manutenção dos dados

> 💡 **Tudo através de menus interativos no terminal, sem precisar mexer no banco diretamente.**

## 🔧 Requisitos do Sistema

Antes de começar, você precisa ter instalado:

| Software | Versão | Descrição |
|----------|--------|-----------|
| 🐍 **Python** | 3.8+ | Para rodar o código |
 |
| 🗄️ **Oracle Instant Client** | 21.x | Para o Python conseguir conectar no Oracle |
| 📁 **Git** | Qualquer | Para baixar o código |

## 🚀 Instalação Passo a Passo

### 1️⃣ Preparando o Ambiente

Abra o terminal e navegue até onde quer instalar o projeto:

```bash
# vai para a pasta home (ou onde preferir)
cd ~

# clona o repositório
git clone https://github.com/digaoes94/trabalhoSQL.git
cd trabalhoSQL
```

### 2️⃣ Instalando Oracle Instant Client

#### 🐧 No Linux:

Abra o terminal e execute:

```bash
# baixa o instant client da oracle
wget https://download.oracle.com/otn_software/linux/instantclient/2119000/oracle-instantclient-basiclite-21.19.0.0.0-1.el8.x86_64.rpm

# instala o pacote (precisa de sudo)
sudo rpm -i oracle-instantclient-basiclite-21.19.0.0.0-1.el8.x86_64.rpm

# configura a variável de ambiente (isso aqui vai ajudar o python achar as bibliotecas do oracle)
echo 'export LD_LIBRARY_PATH=/usr/lib/oracle/21/client64/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

#### 🪟 No Windows:

1. 📥 Baixa o Oracle Instant Client do [site oficial da Oracle](https://www.oracle.com/database/technologies/instant-client/downloads.html)
2. 📂 Extrai os arquivos em `C:\oracle\instantclient_21_19`
3. ⚙️ Adiciona `C:\oracle\instantclient_21_19` no PATH do sistema (Configurações > Variáveis de Ambiente)

### 3️⃣ Configurando o Projeto

No terminal, dentro da pasta do projeto:

```bash
# cria o ambiente virtual (isso aqui isola as dependências do projeto)
python3 -m venv venv

# ativa o ambiente virtual
source venv/bin/activate

# instala as dependências python
pip install -r requirements.txt
```

**🪟 No Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4️⃣ Configurando o Banco de Dados

#### 🐳 Opção 1: Docker (Recomendado - Mais Fácil)

Se você tem Docker instalado, pode usar um container Oracle:

```bash
# sobe o oracle no docker
docker run -d --name oracle-db -p 1521:1521 -e ORACLE_PASSWORD=oracle gvenzl/oracle-xe:21-slim-faststart

# aguarda uns 2-3 minutos pro oracle inicializar completamente
# você pode verificar se está rodando com: docker ps
```

#### 🖥️ Opção 2: Oracle Local

Se preferir instalar o Oracle Database localmente:
1. 📥 Baixa e instala o Oracle Database XE
2. ⚙️ Configura o serviço XEPDB1
3. 👤 Cria usuário system com senha oracle

### 5️⃣ Configurando Credenciais

Edita o arquivo `conexion/passphrase/authentication.oracle` e coloca:

```
system,oracle
```

### 6️⃣ Criando as Tabelas

Depois que o Oracle estiver rodando, cria as tabelas:

```bash
# ativa o venv se não estiver ativo
source venv/bin/activate

# executa o script que cria as tabelas
python3 -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"
```

**🪟 No Windows:**
```cmd
venv\Scripts\activate
python -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"
```

## ▶️ Como Executar o Sistema

### 🐧 Linux/Mac:

```bash
# navega para a pasta do projeto
cd /caminho/para/trabalhoSQL

# ativa o ambiente virtual
source venv/bin/activate

# executa o sistema
python3 main.py
```

### 🪟 Windows:

```cmd
# navega para a pasta do projeto
cd C:\caminho\para\trabalhoSQL

# ativa o ambiente virtual
venv\Scripts\activate

# executa o sistema
python main.py
```

> 🎉 **Quando executar, vai aparecer um menu com as opções do sistema!**

## 📖 Como Usar o Sistema

### 🖥️ Console Principal (main.py)

O arquivo `main.py` é o **console principal** do sistema - é onde você vai navegar por toda a interface. É basicamente o "coração" da aplicação que gerencia todos os menus e funcionalidades.

**O que o main.py faz:**
- 🎯 **Controla toda a navegação** - gerencia os menus e submenus
- 🔄 **Loop principal** - mantém o sistema rodando até você escolher sair
- 📊 **Chama os relatórios** - executa as consultas SQL e mostra os dados
- ➕ **Gerencia inserções** - coordena o cadastro de novos registros
- ✏️ **Controla atualizações** - permite modificar dados existentes
- 🗑️ **Gerencia remoções** - coordena a exclusão de registros
- 🎨 **Interface amigável** - apresenta tudo de forma organizada no terminal

> 💡 **É através do main.py que você acessa todas as funcionalidades do sistema!**

### 🎛️ Menu Principal

Quando você rodar o `python3 main.py`, vai aparecer um menu assim:

```
Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Remover Registros
4 - Atualizar Registros
5 - Sair
```

### opção 1: relatórios

aqui você pode ver:
- **relatório de clientes** - lista todos os clientes cadastrados
- **relatório de compras** - mostra todas as compras feitas
- **relatório de estoque** - controla o estoque dos produtos
- **relatório de fornecedores** - lista os fornecedores
- **relatório de produtos** - catálogo completo
- **relatório de vendas** - histórico de vendas

### opção 2: inserir registros

permite cadastrar:
- **clientes** - nome, cpf, email, telefone
- **fornecedores** - nome, cnpj, telefone, email
- **produtos** - nome, descrição, preço, estoque
- **compras** - compra de produtos dos fornecedores
- **vendas** - venda de produtos para clientes

### opção 3: remover registros

deleta registros de:
- **clientes** - remove um cliente do sistema
- **fornecedores** - remove um fornecedor
- **produtos** - remove um produto

### opção 4: atualizar registros

modifica dados de:
- **clientes** - atualiza informações do cliente
- **fornecedores** - atualiza dados do fornecedor
- **produtos** - modifica preço, descrição, etc.

### opção 5: sair

fecha o sistema e volta pro terminal.

### 🔄 Fluxo de Navegação

O sistema funciona com **menus em cascata**:

1. **Menu Principal** → Escolhe a categoria (Relatórios, Inserir, etc.)
2. **Submenu** → Escolhe o tipo específico (Clientes, Produtos, etc.)
3. **Ação** → Executa a operação desejada
4. **Volta** → Retorna ao menu anterior ou principal

**Exemplo de navegação:**
```
Menu Principal → 1 (Relatórios) → 1 (Clientes) → Mostra relatório
                ↓
            Volta ao Menu Principal
```

> 🎯 **Toda a navegação é feita através do main.py - é sua interface principal!**

## ⭐ Funcionalidades Principais

O sistema gerencia uma loja completa:

| Funcionalidade | Descrição |
|----------------|-----------|
| 👥 **Cadastro de Clientes** | Armazena dados pessoais e endereços |
| 🏢 **Cadastro de Fornecedores** | Gerencia fornecedores e seus dados |
| 🛍️ **Controle de Produtos** | Catálogo com preços e estoque |
| 🛒 **Sistema de Compras** | Registra compras dos fornecedores |
| 💰 **Sistema de Vendas** | Processa vendas para clientes |
| 📊 **Relatórios Detalhados** | Visualiza dados de forma organizada |
| ✏️ **Atualização de Dados** | Modifica informações quando necessário |
| 🗑️ **Remoção de Registros** | Deleta dados obsoletos |

## estrutura do projeto

```
trabalhoSQL/
├── conexion/              # conexão com oracle
│   ├── oracle_queries.py  # classe principal de conexão
│   └── passphrase/
│       └── authentication.oracle  # credenciais
├── controller/            # controladores (lógica de negócio)
│   ├── Cont_Cliente.py
│   ├── Cont_Compra.py
│   ├── Cont_Fornecedor.py
│   ├── Cont_Produto.py
│   └── Cont_Venda.py
├── model/                 # modelos de dados
│   ├── Cliente.py
│   ├── Compra.py
│   ├── Endereco.py
│   ├── Fornecedor.py
│   ├── ItemCompra.py
│   ├── ItemVenda.py
│   ├── Produto.py
│   └── Venda.py
├── sql/                   # scripts sql
│   ├── create_tables.sql
│   └── relatorio*.sql
├── utils/                 # utilitários
│   ├── config.py
│   └── splash_screen.py
├── views/                 # visualizações
│   └── relatorios.py
├── db_setup/             # setup do banco
│   └── run_db_setup.py
├── main.py               # arquivo principal
└── requirements.txt      # dependências
```

## comandos úteis

### criar tabelas no banco
```bash
# linux/mac
source venv/bin/activate
python3 -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"

# windows
venv\Scripts\activate
python -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"
```

### testar conexão
```bash
# linux/mac
source venv/bin/activate
python3 -c "from conexion.oracle_queries import OracleQueries; oracle = OracleQueries(); oracle.connect(); print('conexão ok!'); oracle.close()"

# windows
venv\Scripts\activate
python -c "from conexion.oracle_queries import OracleQueries; oracle = OracleQueries(); oracle.connect(); print('conexão ok!'); oracle.close()"
```

## problemas comuns e soluções

### erro: "ORA-12541: TNS:no listener"
**o que significa:** o oracle database não está rodando
**como resolver:**
- se estiver usando docker: `docker ps` para ver se o container está rodando
- se não estiver: `docker start oracle-db` ou `docker run -d --name oracle-db -p 1521:1521 -e ORACLE_PASSWORD=oracle gvenzl/oracle-xe:21-slim-faststart`
- se estiver usando oracle local: verifica se o serviço oracle está ativo

### erro: "ORA-12514: TNS:listener does not currently know of service"
**o que significa:** o oracle está rodando mas ainda não terminou de inicializar
**como resolver:** aguarda uns 2-3 minutos e tenta novamente. o oracle demora pra inicializar completamente.

### erro: "ModuleNotFoundError: No module named 'cx_Oracle'"
**o que significa:** o ambiente virtual não está ativo ou as dependências não foram instaladas
**como resolver:**
```bash
# ativa o venv
source venv/bin/activate  # linux/mac
# ou
venv\Scripts\activate     # windows

# instala as dependências
pip install -r requirements.txt
```

### erro: "ORA-00942: table or view does not exist"
**o que significa:** as tabelas ainda não foram criadas no banco
**como resolver:**
```bash
# ativa o venv
source venv/bin/activate

# cria as tabelas
python3 -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"
```

### erro: "externally-managed-environment"
**o que significa:** o sistema não permite instalar pacotes globalmente
**como resolver:** sempre use ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## dicas importantes

1. **sempre ative o ambiente virtual** antes de rodar o sistema
2. **aguarde o oracle inicializar** completamente antes de usar
3. **verifique se o docker está rodando** se estiver usando container
4. **teste a conexão** antes de rodar o sistema principal
5. **mantenha as credenciais** no arquivo authentication.oracle atualizadas

## 👥 Desenvolvedores

| Campo | Informação |
|-------|------------|
| **👨‍💻 Criado por** | Howard Roatti |
| **👥 Alterado por** | Gabriely, Guilherme, Luiz, Ricardo e Rodrigo |
| **👨‍🏫 Professor** | Prof. M.Sc. Howard Roatti |
| **📚 Disciplina** | Banco de Dados |
| **📅 Semestre** | 2025/2 |

---

## 🚀 Guia Completo - Do Zero ao Sistema Funcionando

### **PASSO 1: Preparar o Ambiente**

```bash
# 1. Clona o repositório
git clone https://github.com/digaoes94/trabalhoSQL.git
cd trabalhoSQL

# 2. Cria o ambiente virtual
python3 -m venv venv

# 3. Ativa o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Instala as dependências
pip install -r requirements.txt
```

### **PASSO 2: Configurar o Banco de Dados**

#### **Opção A: Docker (Recomendado)**
```bash
# Sobe o Oracle no Docker
docker run -d --name oracle-db -p 1521:1521 -e ORACLE_PASSWORD=oracle gvenzl/oracle-xe:21-slim-faststart

# Aguarda 2-3 minutos para o Oracle inicializar
# Verifica se está rodando: docker ps
```

#### **Opção B: Oracle Local**
- Instala o Oracle Database XE
- Configura o serviço XEPDB1
- Cria usuário system com senha oracle

### **PASSO 3: Criar as Tabelas**

```bash
# IMPORTANTE: Execute este comando para criar todas as tabelas
python3 -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"
```

**O que este comando faz:**
- 🗑️ Remove tabelas antigas (se existirem)
- ➕ Cria todas as sequences
- ➕ Cria todas as tabelas (clientes, produtos, fornecedores, etc.)
- ✅ Sistema pronto para uso

### **PASSO 4: Executar o Sistema**

```bash
# Roda o sistema principal
python3 main.py
```

**O que vai aparecer:**
- 🎨 **Splash screen** com informações do projeto
- 📊 **Contadores** de registros (inicialmente 0)
- 🎛️ **Menu principal** com 5 opções

### **PASSO 5: Usar o Sistema**

```
Menu Principal
1 - Relatórios
2 - Inserir Registros  
3 - Remover Registros
4 - Atualizar Registros
5 - Sair
```

**Navegação:**
- Digite o número da opção (1-5)
- Siga os submenus
- Use 0 para voltar
- Use 5 para sair

### **PASSO 6: Testar Funcionalidades**

1. **Inserir um cliente:**
   - Menu → 2 → 1
   - Preencha os dados
   - Confirme a inserção

2. **Ver relatórios:**
   - Menu → 1 → 1 (Relatório de Clientes)
   - Veja os dados inseridos

3. **Inserir produtos e vendas:**
   - Menu → 2 → 3 (Produtos)
   - Menu → 2 → 5 (Vendas)

## 🎯 **Sequência Completa (Copy & Paste)**

```bash
# 1. Clona e configura
git clone https://github.com/digaoes94/trabalhoSQL.git
cd trabalhoSQL
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Sobe o Oracle
docker run -d --name oracle-db -p 1521:1521 -e ORACLE_PASSWORD=oracle gvenzl/oracle-xe:21-slim-faststart

# 3. Aguarda 2-3 minutos e cria as tabelas
python3 -c "import sys; sys.path.append('.'); from db_setup.run_db_setup import run; run()"

# 4. Roda o sistema
python3 main.py
```

> 🎉 **Pronto! Sistema funcionando perfeitamente!**

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Banco de Dados da Universidade FAESA .


