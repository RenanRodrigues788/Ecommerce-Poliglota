
-- E-commerce Poliglota: PostgreSQL

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(150) NOT NULL,
    preco NUMERIC(12,2) NOT NULL CHECK (preco >= 0),
    estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id_cliente),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE'
        CHECK (status IN ('PENDENTE', 'PAGO', 'CANCELADO')),
    valor_total NUMERIC(12,2) NOT NULL DEFAULT 0
        CHECK (valor_total >= 0),
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE itens_pedido (
    id_item SERIAL PRIMARY KEY,
    pedido_id INTEGER NOT NULL
        REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES produtos(id_produto),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(12,2) NOT NULL
        CHECK (preco_unitario >= 0),
    UNIQUE (pedido_id, produto_id)
);

CREATE TABLE pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    pedido_id INTEGER NOT NULL UNIQUE REFERENCES pedidos(id_pedido),
    metodo VARCHAR(30) NOT NULL
        CHECK (metodo IN ('PIX', 'CARTAO', 'BOLETO')),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE'
        CHECK (status IN ('PENDENTE', 'APROVADO', 'RECUSADO')),
    valor NUMERIC(12,2) NOT NULL CHECK (valor >= 0),
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_itens_produto ON itens_pedido(produto_id);
