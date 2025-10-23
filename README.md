# 🏪 Sistema de Vendas - Oracle Database

> Sistema completo de gerenciamento de vendas desenvolvido em Python com integração ao Oracle Database, agora totalmente orquestrado com Docker.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)](https://www.oracle.com/database/free/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
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

O sistema permite gerenciar uma loja completa através de uma interface de linha de comando:

- 👥 **Gestão de Clientes e Fornecedores**
- 📦 **Controle de Estoque de Produtos**
- 💰 **Registro de Compras e Vendas**
- 📊 **Geração de Relatórios Detalhados**
- 🔄 **Manutenção Completa de Dados (CRUD)**

> 💡 **Tudo através de menus interativos no terminal, sem precisar mexer no banco diretamente.**

---

## 🚀 Começando (Novo Método com Docker)

Com a nova estrutura, você só precisa do Docker e Docker Compose instalados para rodar todo o ambiente (aplicação + banco de dados).

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (geralmente já vem com o Docker)

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/digaoes94/trabalhoSQL.git
    cd trabalhoSQL
    ```

2.  **Suba os serviços com Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    - O comando `--build` garante que a imagem da aplicação será construída.
    - O Oracle Database pode levar alguns minutos para inicializar completamente. Você verá logs de ambos os serviços no seu terminal.

3.  **Acesse o terminal da aplicação:**
    Após a inicialização do banco de dados, o menu da aplicação aparecerá diretamente no seu terminal.

### Criando as Tabelas do Banco

Na primeira vez que executar, você precisa criar a estrutura do banco de dados. Para fazer isso, execute o seguinte comando **em um novo terminal**, com os contêineres rodando:

```bash
docker-compose exec app python -c "from db_setup.run_db_setup import run; run()"
```

Após executar este comando, o sistema estará pronto para ser usado no terminal onde o `docker-compose up` está rodando.

---

## ⚡ Scripts de Automação

Para facilitar ainda mais o processo, foram criados alguns scripts na pasta `scripts/`.

-   `scripts/setup.sh`: Constrói as imagens e sobe os contêineres em modo detached.
-   `scripts/create_tables.sh`: Aguarda o banco de dados inicializar e executa o script de criação de tabelas.
-   `scripts/logs.sh`: Exibe os logs de todos os serviços em tempo real, para você acompanhar o que está acontecendo.
-   `scripts/stop.sh`: Para e remove os contêineres.

### Novo Fluxo com Scripts

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/digaoes94/trabalhoSQL.git
    cd trabalhoSQL
    ```

2.  **Execute o script de setup:**
    ```bash
    ./scripts/setup.sh
    ```

3.  **Execute o script para criar as tabelas:**
    ```bash
    ./scripts/create_tables.sh
    ```

4.  **Para ver a aplicação rodando e interagir com ela, veja os logs:**
    ```bash
    ./scripts/logs.sh
    ```
    Pressione `Ctrl+C` para sair dos logs. A aplicação continuará rodando em background.

5.  **Quando terminar, pare tudo com:**
    ```bash
    ./scripts/stop.sh
    ```

---

## ▶️ Como Usar o Sistema

A interface principal do sistema é executada no terminal onde você iniciou o `docker-compose up`.

### 🎛️ Menu Principal

```
Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Remover Registros
4 - Atualizar Registros
5 - Sair
```

- **opção 1: relatórios**: Gera relatórios de clientes, compras, estoque, etc.
- **opção 2: inserir registros**: Cadastra novos clientes, fornecedores, produtos e transações.
- **opção 3: remover registros**: Deleta registros do sistema.
- **opção 4: atualizar registros**: Modifica dados existentes.
- **opção 5: sair**: Encerra a aplicação (e o contêiner da aplicação).

---

## 🏗️ Estrutura do Projeto

A estrutura foi atualizada para incluir os arquivos de containerização:

```
trabalhoSQL/
├── Dockerfile              # Define a imagem Docker da aplicação Python
├── docker-compose.yml      # Orquestra os serviços da app e do banco
├── scripts/                # Scripts de automação (setup, logs, etc.)
├── conexion/               # Conexão com o Oracle
├── controller/             # Lógica de negócio
├── model/                  # Modelos de dados
├── sql/                    # Scripts SQL (criação de tabelas)
├── utils/                  # Utilitários
├── views/                  # Visualizações (relatórios)
├── db_setup/               # Script para setup do banco
├── main.py                 # Arquivo principal da aplicação
└── requirements.txt        # Dependências Python
```

---

## ⚙️ Configuração do Banco de Dados

As configurações do banco de dados foram atualizadas:

-   **Imagem Docker:** `gvenzl/oracle-free:latest`
-   **Usuário:** `SYSTEM`
-   **Senha:** `Trabalho204012`
-   **Service Name:** `FREEPBD1`
-   **Host (dentro do Docker):** `oracle-db`

As credenciais são lidas do arquivo `conexion/passphrase/authentication.oracle`, e as configurações de conexão estão em `conexion/oracle_queries.py`. O `docker-compose.yml` cuida de passar as variáveis de ambiente necessárias para o contêiner do Oracle.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Banco de Dados.