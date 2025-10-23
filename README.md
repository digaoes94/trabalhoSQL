# 🏪 Sistema de Vendas - Oracle Database com Docker

> Ambiente de desenvolvimento completo e autocontido, utilizando Docker Compose para orquestrar a aplicação Python e o banco de dados Oracle.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)

---

## 🚀 Como Executar

Com o Docker e Docker Compose instalados, o projeto inteiro (aplicação + banco de dados) é iniciado com um único comando. **Não é necessário ter um Oracle separado rodando.**

**1. Limpeza (Opcional, mas recomendado se houve erros):**
Se você teve problemas com execuções anteriores, limpe o ambiente completamente. **Atenção: isso apagará o banco de dados antigo.**
```bash
docker-compose down --volumes
```

**2. Inicie o Ambiente Completo:**
Na pasta do projeto, execute:
```bash
docker-compose up --build
```
-   O comando `--build` reconstrói a imagem da aplicação se houver mudanças no código.
-   Na primeira vez, o Docker irá baixar a imagem do Oracle e criar o banco de dados, o que pode levar alguns minutos. Aguarde até ver a mensagem `DATABASE IS READY TO USE!` nos logs do serviço `database`.
-   Após o banco de dados ficar pronto, a aplicação Python irá se conectar e exibir o menu principal no mesmo terminal.

**3. Crie as Tabelas (em um novo terminal):**
Com o ambiente rodando (após o passo 2), abra um **novo terminal** na mesma pasta e execute:
```bash
docker-compose exec app python -c "from db_setup.run_db_setup import run; run()"
```
Após executar, você pode voltar para o terminal do `docker-compose up` para usar o sistema.

**4. Para Desligar Tudo:**
No terminal onde o `docker-compose up` está rodando, pressione `Ctrl+C`. Para garantir que tudo seja removido (incluindo a rede e os contêineres), execute:
```bash
docker-compose down
```

---

## ⚙️ Detalhes da Configuração

-   **Serviço da Aplicação (`app`):** Constrói a partir do `Dockerfile` local.
-   **Serviço do Banco de Dados (`database`):**
    -   **Imagem:** `container-registry.oracle.com/database/free:latest`
    -   **Nome do Contêiner:** `trabalhosql-oracle-db`
    -   **Credenciais:** A senha do usuário `SYSTEM` é `Trabalho204012`, definida no `docker-compose.yml`.
    -   **Persistência:** Os dados do banco são salvos em um volume Docker chamado `oracle_data` para não serem perdidos.
-   **Conexão:** A aplicação se conecta ao banco de dados usando o endereço `database`, que é o nome do serviço na rede interna do Docker.
