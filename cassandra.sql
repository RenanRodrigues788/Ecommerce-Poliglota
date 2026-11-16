
-- ==========================================
-- E-COMMERCE POLIGLOTA
-- BANCO DE DADOS: CASSANDRA
-- Historico de clientes e pedidos
-- ==========================================

-- 1. Criar o Keyspace
CREATE KEYSPACE IF NOT EXISTS ecommerce_auditoria
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

-- 2. Selecionar o Keyspace
USE ecommerce_auditoria;

-- 3. Historico de eventos dos clientes
CREATE TABLE IF NOT EXISTS eventos_clientes (
    cliente_id INT,
    evento_id TIMEUUID,
    tipo_evento TEXT,
    descricao TEXT,
    data_evento TIMESTAMP,
    PRIMARY KEY (cliente_id, evento_id)
) WITH CLUSTERING ORDER BY (evento_id DESC);

-- 4. Historico de eventos dos pedidos
CREATE TABLE IF NOT EXISTS eventos_pedidos (
    pedido_id INT,
    evento_id TIMEUUID,
    cliente_id INT,
    tipo_evento TEXT,
    descricao TEXT,
    data_evento TIMESTAMP,
    PRIMARY KEY (pedido_id, evento_id)
) WITH CLUSTERING ORDER BY (evento_id DESC);
