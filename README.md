# 🏪 Sistema de Vendas - Oracle Database

> Sistema de gerenciamento de vendas que roda em Docker e se conecta a um banco de dados Oracle existente na máquina host.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)

---

## ⚠️ Arquitetura e Pré-requisitos

Este projeto foi reconfigurado para rodar a aplicação Python em um contêiner Docker que se conecta a um banco de dados Oracle **já existente e rodando na sua máquina (host)**.

**Antes de iniciar, você PRECISA ter:**

1.  **Docker e Docker Compose** instalados.
2.  Um **contêiner Oracle Database rodando**. O projeto está configurado para usar:
    -   **Imagem:** `container-registry.oracle.com/database/free:latest` (a que você já usa, `oracle-23ai-free`).
    -   **Porta Exposta:** A porta `1521` do contêiner deve estar mapeada para a porta `1521` da sua máquina.

---

## ⚙️ Configuração de Conexão

A aplicação está configurada para se conectar usando os seguintes dados. Garanta que o seu banco de dados corresponde a eles:

-   **Usuário:** `SYSTEM`
-   **Senha:** `Trabalho204012`
-   **Service Name:** `FREEPDB1`

O arquivo `conexion/passphrase/authentication.oracle` contém o usuário e a senha. O arquivo `conexion/oracle_queries.py` contém o Service Name e a lógica de conexão.

---

## 🚀 Como Executar

O processo agora é muito mais simples.

**1. Garanta que seu contêiner Oracle (`oracle-23ai-free`) esteja rodando.**

**2. Inicie a aplicação Python:**
Na pasta do projeto (`~/projeto/trabalhoSQL`), execute:
```bash
./scripts/setup.sh
```
Este comando irá construir a imagem da aplicação e iniciá-la em segundo plano.

**3. Crie as Tabelas (se for a primeira vez):**
Com a aplicação rodando, abra outro terminal e execute:
```bash
./scripts/create_tables.sh
```

**4. Use o Sistema:**
Para ver o menu e interagir com o programa, execute:
```bash
./scripts/logs.sh
```

**5. Para Desligar a Aplicação:**
Quando terminar, para desligar apenas o contêiner da aplicação, execute:
```bash
./scripts/stop.sh
```
*(Isso não irá parar o seu contêiner do banco de dados `oracle-23ai-free`.)*
