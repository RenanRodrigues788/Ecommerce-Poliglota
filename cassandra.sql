-- ==========================================
-- E-COMMERCE POLIGLOTA
-- BANCO DE DADOS: APACHE CASSANDRA
-- Sistema de auditoria de pedidos e pagamentos
-- ==========================================

-- 1. Criar o Keyspace
CREATE KEYSPACE IF NOT EXISTS sistema_auditoria
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

-- 2. Selecionar o Keyspace
USE sistema_auditoria;

-- 3. Criar tabela de eventos de auditoria
CREATE TABLE IF NOT EXISTS logs_eventos (
    cliente_id INT,
    evento_id TIMEUUID,
    pedido_id INT,
    acao TEXT,
    detalhe TEXT,
    data_evento TIMESTAMP,
    PRIMARY KEY (cliente_id, evento_id)
) WITH CLUSTERING ORDER BY (evento_id DESC);
