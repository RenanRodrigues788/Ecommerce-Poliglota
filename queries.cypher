
//
// E-COMMERCE POLIGLOTA - NEO4J
// Sistema de recomendacoes de produtos
//

// 1. Criar clientes de exemplo
MERGE (c1:Cliente {id_cliente: 1})
SET c1.nome = 'Joao';

MERGE (c2:Cliente {id_cliente: 2})
SET c2.nome = 'Maria';

// 2. Criar produtos
MERGE (p1:Produto {id_produto: 1})
SET p1.nome = 'Notebook';

MERGE (p2:Produto {id_produto: 2})
SET p2.nome = 'Mouse sem fio';

MERGE (p3:Produto {id_produto: 3})
SET p3.nome = 'Teclado mecanico';

// 3. Criar categorias
MERGE (cat1:Categoria {nome: 'Informatica'});
MERGE (cat2:Categoria {nome: 'Acessorios'});

// 4. Relacionar produtos e categorias
MATCH (p:Produto {id_produto: 1})
MATCH (c:Categoria {nome: 'Informatica'})
MERGE (p)-[:PERTENCE_A]->(c);

MATCH (p:Produto {id_produto: 2})
MATCH (c:Categoria {nome: 'Acessorios'})
MERGE (p)-[:PERTENCE_A]->(c);

MATCH (p:Produto {id_produto: 3})
MATCH (c:Categoria {nome: 'Acessorios'})
MERGE (p)-[:PERTENCE_A]->(c);

// 5. Registrar compras de exemplo
MATCH (c:Cliente {id_cliente: 1})
MATCH (p:Produto {id_produto: 1})
MERGE (c)-[:COMPROU]->(p);

MATCH (c:Cliente {id_cliente: 2})
MATCH (p:Produto {id_produto: 2})
MERGE (c)-[:COMPROU]->(p);

// 6. Criar recomendacoes entre produtos
MATCH (p1:Produto {id_produto: 1})
MATCH (p2:Produto {id_produto: 2})
MERGE (p1)-[:RELACIONADO_A]->(p2);

MATCH (p1:Produto {id_produto: 1})
MATCH (p3:Produto {id_produto: 3})
MERGE (p1)-[:RELACIONADO_A]->(p3);

// 7. Consultar recomendacoes para o cliente 1
MATCH (c:Cliente {id_cliente: 1})-[:COMPROU]->(p:Produto)
MATCH (p)-[:RELACIONADO_A]-(recomendado:Produto)
WHERE NOT (c)-[:COMPROU]->(recomendado)
RETURN DISTINCT recomendado.id_produto AS id_produto,
       recomendado.nome AS produto_recomendado;

// 8. Visualizar o grafo completo
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;
