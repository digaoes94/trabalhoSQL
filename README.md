# 🏪 Sistema de Gerenciamento - Clientes, Fornecedores e Vendas

> Um sistema completo e robusto de gerenciamento empresarial desenvolvido em **Python** com **Oracle Database**

---

## 📋 Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| 👥 **Gerenciar Clientes** | CPF, dados pessoais, telefone e endereço completo |
| 🏢 **Gerenciar Fornecedores** | CNPJ, razão social, nome fantasia e endereço |
| 📦 **Gerenciar Produtos** | Nome, preço unitário, descrição e estoque |
| 💳 **Registrar Vendas** | Venda de produtos para clientes com relatórios |
| 📥 **Registrar Compras** | Compra de produtos de fornecedores |
| 📊 **Gerar Relatórios** | Clientes, Fornecedores, Produtos, Vendas, Compras, Estoque |

---

## 🛠️ Tecnologias Utilizadas

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle-Database-red?logo=oracle&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ready-green?logo=linux&logoColor=white)

</div>

---

## 📁 Estrutura do Projeto

```
trabalhoSQL/
├── 🎮 controller/              # Controllers CRUD
│   ├── Cont_Cliente.py         # Gerenciamento de clientes
│   ├── Cont_Fornecedor.py      # Gerenciamento de fornecedores
│   ├── Cont_Produto.py         # Gerenciamento de produtos
│   ├── Cont_Compra.py          # Gerenciamento de compras
│   └── Cont_Venda.py           # Gerenciamento de vendas
│
├── 🗂️ model/                   # Modelos de dados
│   ├── Cliente.py
│   ├── Fornecedor.py
│   ├── Produto.py
│   ├── Compra.py
│   ├── Venda.py
│   ├── Endereco.py
│   └── ItemVenda.py
│
├── 🔌 conexion/                # Conexão com banco de dados
│   └── oracle_queries.py       # Queries Oracle parametrizadas
│
├── 📈 views/                   # Relatórios e visualizações
│   └── relatorios.py           # Gerador de relatórios
│
├── 🗄️ sql/                     # Scripts SQL
│   ├── create_tables.sql       # Criação de tabelas e sequences
│   └── relatorio*.sql          # Queries de relatórios
│
├── ⚙️ db_setup/                # Setup do banco de dados
│   ├── run_db_setup.py         # Cria tabelas e triggers
│   └── drop_db.py              # Remove dados (CUIDADO!)
│
├── 🔧 utils/                   # Utilitários
│   ├── splash_screen.py        # Tela de boas-vindas
│   └── config.py               # Configurações
│
├── 📜 main.py                  # Ponto de entrada principal
└── 📖 README.md                # Este arquivo

```

---

## 🚀 Como Executar na LabDatabase

> 🎯 **Se você está usando a máquina virtual LabDatabase, siga este guia!**

### ⚡ Quick Start (3 minutos)

#### 1️⃣ Abrir Terminal e Iniciar Docker

```bash
# Abra um terminal e execute:
cd database

# Inicie o Docker Compose
docker-compose up -d

# Aguarde ~2 minutos para o Oracle ficar pronto
# (A máquina virtual já tem Docker pré-configurado)
```

#### 2️⃣ Abrir IDE e Criar Tabelas

No **terminal integrado da IDE**, execute:

```bash
# Ativar virtualenv (se ainda não estiver ativado)
source venv/bin/activate

# Criar tabelas e estrutura do banco
python3 ./db_setup/run_db_setup.py

# Você deve ver:
# 🏗️ Creating tables and sequences...
# ✅ Successfully executed
# 🎉 Database setup completed successfully!
```

#### 3️⃣ Executar a Aplicação

No **terminal integrado da IDE**, execute:

```bash
# Iniciar o sistema
python3 ./main.py

# A aplicação abrirá com o menu principal
```

---

## 📖 Guia Detalhado para LabDatabase

### ✅ Ambiente Pré-configurado

A máquina virtual LabDatabase já possui:
- ✅ Python 3.12+
- ✅ Docker e Docker Compose
- ✅ Oracle pronto para rodar
- ✅ Virtualenv do projeto configurado
- ✅ IDE com terminal integrado

### 📖 Passo a Passo Completo para LabDatabase

#### 1️⃣ Terminal Externo: Iniciar Docker

```bash
# Abra um terminal externo da máquina virtual
# Execute os seguintes comandos:

cd database

docker-compose up -d

# Aguarde ~2 minutos para o Oracle ficar pronto
# A mensagem "DATABASE IS READY TO USE!" aparecerá nos logs
```

#### 2️⃣ IDE: Terminal Integrado - Criar Tabelas

Na **IDE (VSCode, PyCharm, etc)**, abra o terminal integrado e execute:

```bash
# Verifica se virtualenv está ativado (deve ver (venv) no prompt)
# Se não estiver, ative:
source venv/bin/activate

# Criar tabelas, sequences e triggers
python3 ./db_setup/run_db_setup.py

# Você deve ver:
# 🏗️ Creating tables and sequences...
# ✅ Successfully executed
# 🔧 Creating triggers...
# ✅ Trigger CLIENTES created successfully
# 🎉 Database setup completed successfully!
```

#### 3️⃣ IDE: Terminal Integrado - Executar a Aplicação

No mesmo terminal integrado da IDE:

```bash
# Iniciar o sistema
python3 ./main.py

# O menu principal aparecerá:
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║         🏪 SISTEMA DE GERENCIAMENTO DE VENDAS 🏪                 ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

Selecione uma opção:
1. 📥 Inserir dados
2. ✏️ Atualizar dados
3. 🗑️ Deletar dados
4. 🔍 Pesquisar dados
5. 📋 Ver pedidos
6. 📦 Ver compras
7. 📊 Relatórios
0. 🚪 Sair
```

#### 4️⃣ Resetar o Banco (Se Necessário)

No terminal integrado da IDE:

```bash
# ⚠️ CUIDADO: Isso apaga TODOS os dados!
python3 ./db_setup/drop_db.py

# Depois recriar:
python3 ./db_setup/run_db_setup.py
```

#### 5️⃣ Encerrar a Aplicação

Para sair da aplicação:
```bash
# No menu principal, selecione: 0 (Sair)
# Ou pressione: Ctrl+C no terminal
```

---

## 📖 Menu da Aplicação

### Opção 1: Inserir Dados

```
1. 👥 Cliente
   - CPF, nome, email, telefone
   - Endereço completo (CEP, logradouro, nº, complemento, bairro, cidade, estado)

2. 🏢 Fornecedor
   - CNPJ, razão social, nome fantasia, email, telefone
   - Endereço completo

3. 📦 Produto
   - Nome, descrição, preço unitário
   - Estoque automático

4. 💳 Venda
   - Seleciona cliente e produtos
   - Calcula total automaticamente

5. 📥 Compra
   - Seleciona fornecedor e produtos
   - Registra valor total
```

### Opção 7: Gerar Relatórios

```
1. 👥 Clientes - Lista todos os clientes cadastrados
2. 🏢 Fornecedores - Lista todos os fornecedores
3. 📦 Produtos - Lista produtos com estoque
4. 💳 Vendas - Histórico de vendas
5. 📥 Compras - Histórico de compras
6. 🗄️ Estoque - Status do estoque
```

---

## ✅ Validações Implementadas

### 🔐 CPF
- ✔️ 11 dígitos numéricos
- ✔️ Sem duplicação no banco

### 🏢 CNPJ
- ✔️ 14 dígitos numéricos
- ✔️ Sem duplicação no banco

### 📮 CEP
- ✔️ Formato: `12345-678` ou `12345678`
- ✔️ Armazenado como: `12345-678` (com hífen)
- ✔️ Aceita números com ou sem hífen

### 🗺️ Estado (UF)
- ✔️ Aceita código: `ES`, `SP`, `RJ`
- ✔️ Aceita nome completo: `Espírito Santo`, `São Paulo`
- ✔️ Case-insensitive: `es`, `Es`, `ES`
- ✔️ Remove acentos automaticamente
- ✔️ Armazenado como código: `ES`

---

## 🐛 Solução de Problemas

### Problema: "ModuleNotFoundError: No module named 'conexion'"

**Solução:**
```bash
# Certifique-se que está no diretório correto
pwd  # Deve mostrar: /home/user/trabalhoSQL

# Verifique se virtualenv está ativado
# Você deve ver (venv) no prompt
```

### Problema: "ORA-12541: TNS:no listener"

**Solução:**
```bash
# Verificar se Oracle está rodando
docker-compose ps

# Se não estiver:
docker-compose up -d

# Aguardar inicialização:
sleep 120  # Aguarda 2 minutos
```

### Problema: "cx_Oracle.DatabaseError: ORA-01017"

**Solução:**
```bash
# Verificar credenciais em conexion/oracle_queries.py
# Usuário padrão: SYSTEM
# Senha padrão: oracle (ou conforme docker-compose.yml)
```

### Problema: "Permission denied" ao executar ./main.py

**Solução:**
```bash
# Adicionar permissão de execução
chmod +x main.py

# Depois executar
./main.py
```

---

## 🔐 Considerações de Segurança

⚠️ **AVISO:** Este projeto ainda contém vulnerabilidades de **SQL Injection**.

📖 **Como corrigir:**
Consulte o arquivo `SECURITY_FIX_GUIDE.md` para detalhes completos e instruções de correção.

---

## 📚 Documentação Adicional

| Arquivo | Descrição |
|---------|-----------|
| `SECURITY_FIX_GUIDE.md` | 🔒 Guia de segurança e correção de SQL Injection |
| `VALIDACAO_UF.md` | ✅ Documentação da validação de Estado (UF) |
| `TESTE_RAPIDO.md` | 🧪 Instruções para testes rápidos |
| `RESUMO_VERIFICACAO.md` | 📋 Resumo da análise de código |
| `ANALISE_COMPLETA.txt` | 📊 Análise técnica detalhada |

---

## 🎓 Sobre Este Projeto

- 📚 Projeto educacional de gerenciamento de banco de dados
- 🎯 Foco em CRUD, validações e relatórios
- 💾 Utiliza Oracle Database (21c+)
- 🐍 Desenvolvido em Python 3.12
- 🔗 Sequences e Triggers para integridade de dados

---

## 📋 Requisitos do Sistema

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| **Python** | 3.10 | 3.12+ |
| **RAM** | 2GB | 4GB |
| **Disco** | 500MB | 2GB |
| **SO** | Linux | Ubuntu 20.04+ / Fedora 35+ |
| **Oracle** | 12c | 21c+ |

---

## 🤝 Contribuições

Este é um projeto educacional. Sugestões de melhorias são bem-vindas!

---

## 📝 Licença

Projeto educacional - Uso livre para fins didáticos.

---

## 👨‍💻 Desenvolvedor

Desenvolvido como projeto de banco de dados com foco em gerenciamento empresarial.

**Última atualização:** 2025-10-23

---

<div align="center">

### ⭐ Se este projeto foi útil, considere deixar uma estrela!


</div>
