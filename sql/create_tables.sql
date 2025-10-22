-- Comandos DROP para limpar o ambiente antes da criação das tabelas e sequences
-- Dropar triggers
DROP TRIGGER trg_clientes_pk;
DROP TRIGGER trg_produtos_pk;
DROP TRIGGER trg_fornecedores_pk;
DROP TRIGGER trg_vendas_pk;
DROP TRIGGER trg_compras_pk;
DROP TRIGGER trg_item_venda_pk;
DROP TRIGGER trg_item_compra_pk;
DROP TRIGGER trg_enderecos_pk;

-- Dropar tabelas (em ordem inversa de dependência)
DROP TABLE item_venda CASCADE CONSTRAINTS;
DROP TABLE item_compra CASCADE CONSTRAINTS;
DROP TABLE enderecos CASCADE CONSTRAINTS;
DROP TABLE vendas CASCADE CONSTRAINTS;
DROP TABLE compras CASCADE CONSTRAINTS;
DROP TABLE estoque CASCADE CONSTRAINTS;
DROP TABLE produtos CASCADE CONSTRAINTS;
DROP TABLE clientes CASCADE CONSTRAINTS;
DROP TABLE fornecedores CASCADE CONSTRAINTS;

-- Dropar sequences
DROP SEQUENCE clientes_id_seq;
DROP SEQUENCE produtos_id_seq;
DROP SEQUENCE fornecedores_id_seq;
DROP SEQUENCE vendas_id_seq;
DROP SEQUENCE compras_id_seq;
DROP SEQUENCE item_venda_id_seq;
DROP SEQUENCE item_compra_id_seq;
DROP SEQUENCE enderecos_id_seq;

-- Conteúdo original de criação de tabelas e sequences
-- Criação das SEQUENCES para as chaves primárias
CREATE SEQUENCE clientes_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE produtos_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE fornecedores_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE vendas_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE compras_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE item_venda_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE item_compra_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE enderecos_id_seq START WITH 1 INCREMENT BY 1;

-- Criação da tabela de Fornecedores
CREATE TABLE fornecedores (
    id_fornecedor NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    cnpj VARCHAR2(14) UNIQUE NOT NULL,
    telefone VARCHAR2(20),
    email VARCHAR2(100)
);

-- Criação da tabela de Clientes
CREATE TABLE clientes (
    id_cliente NUMBER(10) PRIMARY KEY,
    cpf VARCHAR2(11) UNIQUE NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    email VARCHAR2(100),
    telefone VARCHAR2(20)
);

-- Criação da tabela de Endereços (associada a Clientes e Fornecedores)
CREATE TABLE enderecos (
    id_endereco NUMBER(10) PRIMARY KEY,
    cep VARCHAR2(8) NOT NULL,
    logradouro VARCHAR2(255) NOT NULL,
    numero NUMBER(5),
    complemento VARCHAR2(100),
    bairro VARCHAR2(100),
    cidade VARCHAR2(100),
    estado VARCHAR2(2),
    id_cliente NUMBER(10),
    id_fornecedor NUMBER(10),
    CONSTRAINT fk_endereco_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    CONSTRAINT fk_endereco_fornecedor FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor) ON DELETE CASCADE,
    CONSTRAINT chk_cliente_fornecedor CHECK ( (id_cliente IS NOT NULL AND id_fornecedor IS NULL) OR (id_cliente IS NULL AND id_fornecedor IS NOT NULL) )
);

-- Criação da tabela de Produtos
CREATE TABLE produtos (
    id_produto NUMBER(10) PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    descricao VARCHAR2(255),
    preco_unitario NUMBER(10, 2) NOT NULL,
    qtde_estoque NUMBER(10) DEFAULT 0
);

-- Criação da tabela de Estoque (Adicionado)
CREATE TABLE estoque (
    id_produto NUMBER(10) PRIMARY KEY,
    custo_unitario NUMBER(10, 2) NOT NULL,
    quantidade NUMBER(10) NOT NULL,
    total NUMBER(10, 2) NOT NULL,
    CONSTRAINT fk_estoque_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE
);

-- Criação da tabela de Vendas
CREATE TABLE vendas (
    id_venda NUMBER(10) PRIMARY KEY,
    data_venda DATE NOT NULL,
    valor_total NUMBER(10, 2),
    id_cliente NUMBER(10),
    CONSTRAINT fk_venda_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Criação da tabela de Itens de Venda (tabela associativa)
CREATE TABLE item_venda (
    id_item_venda NUMBER(10) PRIMARY KEY,
    id_venda NUMBER(10) NOT NULL,
    id_produto NUMBER(10) NOT NULL,
    quantidade NUMBER(10) NOT NULL,
    preco_unitario_venda NUMBER(10, 2) NOT NULL,
    subtotal NUMBER(10, 2),
    CONSTRAINT fk_item_venda_venda FOREIGN KEY (id_venda) REFERENCES vendas(id_venda) ON DELETE CASCADE,
    CONSTRAINT fk_item_venda_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- Criação da tabela de Compras
CREATE TABLE compras (
    id_compra NUMBER(10) PRIMARY KEY,
    data_compra DATE NOT NULL,
    valor_total NUMBER(10, 2),
    id_fornecedor NUMBER(10),
    CONSTRAINT fk_compra_fornecedor FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
);

-- Criação da tabela de Itens de Compra (tabela associativa)
CREATE TABLE item_compra (
    id_item_compra NUMBER(10) PRIMARY KEY,
    id_compra NUMBER(10) NOT NULL,
    id_produto NUMBER(10) NOT NULL,
    quantidade NUMBER(10) NOT NULL,
    preco_unitario_compra NUMBER(10, 2) NOT NULL,
    subtotal NUMBER(10, 2),
    CONSTRAINT fk_item_compra_compra FOREIGN KEY (id_compra) REFERENCES compras(id_compra) ON DELETE CASCADE,
    CONSTRAINT fk_item_compra_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- Triggers para auto-incremento das chaves primárias usando as sequences
CREATE OR REPLACE TRIGGER trg_clientes_pk
BEFORE INSERT ON clientes
FOR EACH ROW
BEGIN
  :new.id_cliente := clientes_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_produtos_pk
BEFORE INSERT ON produtos
FOR EACH ROW
BEGIN
  :new.id_produto := produtos_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_fornecedores_pk
BEFORE INSERT ON fornecedores
FOR EACH ROW
BEGIN
  :new.id_fornecedor := fornecedores_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_vendas_pk
BEFORE INSERT ON vendas
FOR EACH ROW
BEGIN
  :new.id_venda := vendas_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_compras_pk
BEFORE INSERT ON compras
FOR EACH ROW
BEGIN
  :new.id_compra := compras_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_item_venda_pk
BEFORE INSERT ON item_venda
FOR EACH ROW
BEGIN
  :new.id_item_venda := item_venda_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_item_compra_pk
BEFORE INSERT ON item_compra
FOR EACH ROW
BEGIN
  :new.id_item_compra := item_compra_id_seq.NEXTVAL;
END;
/

CREATE OR REPLACE TRIGGER trg_enderecos_pk
BEFORE INSERT ON enderecos
FOR EACH ROW
BEGIN
  :new.id_endereco := enderecos_id_seq.NEXTVAL;
END;
/
