# 🛒 E-commerce Poliglota — Persistência Poliglota

Sistema de comércio eletrônico desenvolvido em Python, utilizando quatro bancos de dados diferentes (PostgreSQL, MongoDB, Neo4j e Apache Cassandra), cada um responsável por um domínio específico da aplicação.

O projeto demonstra o conceito de **Persistência Poliglota (Polyglot Persistence)**, utilizando diferentes modelos de armazenamento dentro de um mesmo sistema para atender às necessidades específicas de cada operação.

---

## 👥 Integrantes do Grupo

- **Renan Ferreira Rodrigues**
- **Akira Higa**

---

## 🎯 1. Tema do Projeto

O projeto consiste no desenvolvimento de um sistema de E-commerce com arquitetura poliglota de bancos de dados.

A proposta é demonstrar como diferentes tecnologias de armazenamento podem trabalhar em conjunto, aproveitando as características de cada banco de dados.

O sistema contempla:

- Cadastro e gerenciamento de clientes.
- Cadastro e gerenciamento de produtos.
- Controle de estoque.
- Criação e consulta de pedidos.
- Registro de pagamentos.
- Armazenamento de informações detalhadas dos produtos.
- Recomendação de produtos relacionados.
- Auditoria de pedidos e pagamentos.

## 🏗️ 2. Arquitetura e Bancos de Dados

O sistema utiliza quatro bancos de dados, integrados por uma aplicação desenvolvida em Python.

### 2.1 PostgreSQL — Banco Relacional

**Modelo:** Relacional (SQL).

**Responsabilidade:** Armazenar os dados transacionais e estruturados do e-commerce.

Principais informações:
- Clientes.
- Produtos.
- Pedidos.
- Itens dos pedidos.
- Pagamentos.

**Justificativa da escolha:**

O PostgreSQL foi escolhido pela capacidade de trabalhar com transações, relacionamentos entre tabelas, integridade referencial e propriedades ACID.

É especialmente adequado para operações críticas, como criação de pedidos, atualização de estoque e registro de pagamentos.

### 2.2 MongoDB — Banco Orientado a Documentos

**Modelo:** NoSQL — Documentos BSON.

**Responsabilidade:** Armazenar informações complementares e detalhadas dos produtos.

Exemplos de informações:
- Categoria.
- Marca.
- Descrição.
- Atributos específicos.
- Tags.
- Imagens.

**Justificativa da escolha:**

O MongoDB permite armazenar documentos com estruturas flexíveis, sendo adequado para produtos que possuem características diferentes.

Assim, podemos adicionar atributos específicos sem precisar alterar constantemente a estrutura de tabelas relacionais.

### 2.3 Neo4j — Banco Orientado a Grafos

**Modelo:** NoSQL — Grafos.

**Responsabilidade:** Armazenar relacionamentos entre clientes, produtos e categorias, possibilitando recomendações de produtos.

Exemplo de relacionamentos:
- Cliente compra produto.
- Produto pertence a categoria.
- Produto está relacionado a outro produto.

**Justificativa da escolha:**

O Neo4j foi escolhido por sua capacidade de representar e consultar relacionamentos complexos por meio de nós e arestas.

Utiliza a linguagem Cypher para consultar os relacionamentos e identificar produtos que podem interessar aos clientes.

### 2.4 Apache Cassandra — Banco de Colunas Largas

**Modelo:** NoSQL — Wide-Column.

**Responsabilidade:** Armazenar os eventos de auditoria do sistema.

Exemplos:
- Criação de pedidos.
- Pagamentos aprovados.
- Pagamentos pendentes.
- Pagamentos recusados.
- Histórico de operações.

**Justificativa da escolha:**

O Cassandra foi escolhido por sua arquitetura distribuída, capacidade de escrita em grande volume e escalabilidade horizontal.

É adequado para armazenar históricos de eventos e registros de auditoria.

---

## 🐍 3. Linguagens e Tecnologias

A linguagem principal da aplicação é Python, responsável por integrar os quatro bancos de dados e executar as regras de negócio.

| Tecnologia | Utilização |
|---|---|
| Python | Lógica principal e integração |
| SQL | Consultas e operações PostgreSQL |
| PyMongo | Comunicação com MongoDB |
| Cypher | Consultas e relacionamentos Neo4j |
| CQL | Consultas e operações Cassandra |
| Docker | Contêineres e infraestrutura |
| YAML | Configuração do Docker Compose |

**Justificativa da escolha do Python:**

Python possui bibliotecas específicas para integração com os quatro bancos, sintaxe simples e um ecossistema amplo para desenvolvimento de aplicações e automações.

---

## ⚖️ 4. Teorema CAP e Consistência

O teorema CAP apresenta três propriedades importantes em sistemas distribuídos:

- **C — Consistency (Consistência):** todos os nós apresentam dados consistentes de acordo com as garantias do sistema.
- **A — Availability (Disponibilidade):** as requisições continuam recebendo respostas.
- **P — Partition Tolerance (Tolerância a Partições):** o sistema consegue lidar com falhas de comunicação entre nós.

Durante uma partição de rede, sistemas distribuídos precisam equilibrar consistência e disponibilidade.

### Comportamento dos bancos no projeto

**PostgreSQL:**

Utiliza transações ACID para garantir a integridade dos dados. No ambiente atual, utiliza uma única instância.

Se ficar indisponível, as operações principais de cadastro, pedidos e pagamentos não poderão ser realizadas.

**MongoDB:**

Oferece consistência configurável por meio de mecanismos de leitura e escrita. No ambiente atual, utiliza uma única instância.

Se ficar indisponível, a consulta dos detalhes complementares dos produtos ficará comprometida.

**Neo4j:**

Utiliza transações ACID para manter a integridade das operações no grafo. No ambiente atual, utiliza uma única instância.

Se ficar indisponível, as recomendações de produtos não poderão ser consultadas.

**Apache Cassandra:**

Oferece consistência ajustável (Tunable Consistency), permitindo configurar os níveis de consistência das operações.

No ambiente atual, utiliza uma única instância e fator de replicação igual a 1.

Se ficar indisponível, novos registros de auditoria não poderão ser armazenados.

### Observação sobre a arquitetura

O projeto atual utiliza uma instância de cada banco de dados no Docker Compose. Portanto, a arquitetura demonstra a integração entre diferentes modelos de persistência, mas ainda não implementa alta disponibilidade com múltiplas réplicas.

---

## 🔄 5. Consistência e Replicação

### PostgreSQL
Utiliza propriedades ACID:
- Atomicidade.
- Consistência.
- Isolamento.
- Durabilidade.

### MongoDB
Oferece atomicidade em operações de documento único e permite configurar mecanismos de leitura e escrita.

Em uma arquitetura com Replica Set, os nós secundários podem assumir a função de primário após uma eleição, desde que exista maioria elegível.

### Neo4j
Utiliza transações ACID.

Em uma arquitetura Causal Cluster, utiliza o protocolo Raft para coordenar a replicação e as operações de escrita.

### Cassandra
Utiliza consistência ajustável e arquitetura distribuída sem um nó mestre único.

O número de réplicas necessárias depende do fator de replicação e do nível de consistência configurado.

**Exemplo teórico:**

Considerando três réplicas e nível de consistência QUORUM:

\[
QUORUM = \lfloor 3/2 \rfloor + 1 = 2
\]

Dessa forma, duas réplicas precisam responder para atender ao quorum.

Uma instância pode ficar indisponível e ainda permitir operações que exigem quorum, desde que as demais condições de disponibilidade sejam atendidas.

**Configuração atual:** fator de replicação 1 no Cassandra. O exemplo de três réplicas é uma explicação teórica de uma possível expansão da arquitetura.

---

## 🔗 6. Integração entre os Bancos

A aplicação Python funciona como camada de integração entre os quatro bancos.

Principais fluxos:

1. O PostgreSQL armazena clientes, produtos, pedidos e pagamentos.
2. O MongoDB armazena informações complementares do catálogo.
3. O Neo4j utiliza relacionamentos para recomendar produtos.
4. O Cassandra registra eventos de auditoria após operações realizadas com sucesso no PostgreSQL.

### Auditoria automática

Quando um pedido é criado, a aplicação registra um evento no Cassandra.

Quando um pagamento é registrado, o sistema também gera um evento de auditoria, identificando:
- ID do cliente.
- ID do pedido.
- ID do pagamento.
- Método de pagamento.
- Status.
- Valor.

A operação principal é confirmada no PostgreSQL antes da tentativa de registro no Cassandra. Caso a auditoria falhe, o sistema apresenta um aviso, sem desfazer o pedido ou pagamento já confirmado.

---

## 📂 7. Estrutura do Repositório

```text
Ecommerce-Poliglota/
│
├── README.md
├── inicializar.sh
├── cassandra.sql
├── catalogo.json
├── docker-compose.yml
├── init.sql
├── queries.cypher
│
└── src/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── importar_catalogo.py
    │
    └── database/
        ├── __init__.py
        ├── cassandra_db.py
        ├── mongo_db.py
        ├── neo4j_db.py
        └── postgres_db.py
```

---

## 🚀 8. Como Executar o Projeto

### Pré-requisitos

- Docker.
- Docker Compose.
- Git.

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/RenanRodrigues788/Ecommerce-Poliglota.git

cd Ecommerce-Poliglota
```

### Passo 2 — Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

Configure as seguintes variáveis:

```env
POSTGRES_PASSWORD=sua_senha_postgres
MONGO_PASSWORD=sua_senha_mongodb
NEO4J_PASSWORD=sua_senha_neo4j
```

Utilize senhas próprias para o ambiente de execução.

Não publique o arquivo `.env` no GitHub.

### Passo 3 — Construir e iniciar os contêineres

```bash
docker compose up -d --build
```

### Passo 4 — Verificar os contêineres

```bash
docker compose ps
```

Verifique se os cinco serviços estão em execução: PostgreSQL, MongoDB, Neo4j, Cassandra e aplicação Python.

**Atenção:** na primeira execução, os bancos podem demorar para ficar disponíveis, especialmente o Cassandra. Aguarde a conclusão da inicialização antes de prosseguir.

### Passo 5 — Inicializar os bancos de dados

Após os serviços estarem disponíveis, execute:

```bash
./inicializar.sh
```

O script realiza automaticamente as seguintes operações:

1. **Cassandra:** cria o keyspace `sistema_auditoria` e a tabela `logs_eventos`, caso ainda não existam.
2. **Neo4j:** executa os comandos de `queries.cypher`, criando clientes, produtos, categorias e relacionamentos de exemplo.
3. **MongoDB:** importa os três produtos do arquivo `catalogo.json`.

O PostgreSQL é inicializado separadamente pelo arquivo `init.sql`, executado automaticamente pelo contêiner na primeira criação do volume de dados.

O script `inicializar.sh` foi desenvolvido para permitir novas execuções sem duplicar os registros de exemplo identificados por suas respectivas chaves.

### Passo 6 — Executar a aplicação

```bash
docker compose exec app_python python main.py
```

O sistema apresentará um menu interativo com as opções de cadastro, consulta, pedidos, pagamentos, recomendações e auditoria.

### Passo 7 — Encerrar os serviços

No menu da aplicação, selecione a opção `0` para sair.

Para desligar os contêineres:

```bash
docker compose down
```

Esse comando preserva os volumes persistentes dos bancos de dados.

## 🖥️ 9. Funcionalidades do Sistema

O sistema possui um menu interativo em Python com as seguintes opções:

| Opção | Funcionalidade | Banco principal |
|---|---|---|
| 1 | Cadastrar cliente | PostgreSQL |
| 2 | Listar clientes | PostgreSQL |
| 3 | Cadastrar produto | PostgreSQL |
| 4 | Listar produtos | PostgreSQL |
| 5 | Criar pedido | PostgreSQL + Cassandra |
| 6 | Listar pedidos | PostgreSQL |
| 7 | Registrar pagamento | PostgreSQL + Cassandra |
| 8 | Consultar detalhes de produto | MongoDB |
| 9 | Recomendar produtos | Neo4j |
| 10 | Consultar logs de auditoria | Cassandra |
| 0 | Encerrar o sistema | — |

---

## 🎓 10. Considerações Finais

O E-commerce Poliglota demonstra na prática como diferentes modelos de bancos de dados podem trabalhar de maneira integrada em uma mesma aplicação.

A utilização de PostgreSQL, MongoDB, Neo4j e Apache Cassandra permite explorar diferentes estratégias de armazenamento, consistência, relacionamentos e persistência.

O projeto também demonstra a importância de escolher a tecnologia adequada para cada necessidade do negócio, considerando fatores como integridade dos dados, flexibilidade, escalabilidade e disponibilidade.

Dessa forma, o sistema representa uma aplicação prática do conceito de Persistência Poliglota e dos fundamentos de bancos de dados relacionais e não relacionais.