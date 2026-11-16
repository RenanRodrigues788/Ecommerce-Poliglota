
import os
from neo4j import GraphDatabase


URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.environ["NEO4J_PASSWORD"]
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def executar_query(query, **parametros):
    with GraphDatabase.driver(
        URI,
        auth=(USER, PASSWORD)
    ) as driver:

        dados, _, _ = driver.execute_query(
            query,
            database_=DATABASE,
            **parametros
        )

        return dados


def recomendar_produtos(cliente_id):
    query = """
    MATCH (c:Cliente {id_cliente: $cliente_id})-[:COMPROU]->(p:Produto)
    MATCH (p)-[:RELACIONADO_A]-(recomendado:Produto)
    WHERE NOT (c)-[:COMPROU]->(recomendado)
    RETURN DISTINCT
        recomendado.id_produto AS id,
        recomendado.nome AS nome
    ORDER BY nome
    """

    resultado = executar_query(
        query,
        cliente_id=cliente_id
    )

    return [
        {
            "id": registro["id"],
            "nome": registro["nome"]
        }
        for registro in resultado
    ]
