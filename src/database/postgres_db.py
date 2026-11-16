
import os
import psycopg2
from psycopg2 import IntegrityError


class PostgresModule:

    def __init__(self):
        # Configuracao da conexao com PostgreSQL
        self.conexao = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            database=os.getenv("POSTGRES_DB", "ecommerce"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.environ["POSTGRES_PASSWORD"]
        )

        self.cursor = self.conexao.cursor()

    # ======================================
    # CLIENTES
    # ======================================

    def cadastrar_cliente(self, nome, email, telefone=None):
        try:
            self.cursor.execute(
                """
                INSERT INTO clientes (nome, email, telefone)
                VALUES (%s, %s, %s)
                RETURNING id_cliente
                """,
                (nome, email, telefone)
            )

            cliente_id = self.cursor.fetchone()[0]
            self.conexao.commit()

            return f"Cliente cadastrado! ID: {cliente_id}"

        except IntegrityError:
            self.conexao.rollback()
            return "Erro: email ja cadastrado ou dados invalidos."

        except Exception:
            self.conexao.rollback()
            raise

    def listar_clientes(self):
        self.cursor.execute(
            """
            SELECT id_cliente, nome, email, telefone
            FROM clientes
            ORDER BY id_cliente
            """
        )

        return self.cursor.fetchall()

    # ======================================
    # PRODUTOS
    # ======================================

    def cadastrar_produto(self, sku, nome, preco, estoque):
        try:
            self.cursor.execute(
                """
                INSERT INTO produtos (sku, nome, preco, estoque)
                VALUES (%s, %s, %s, %s)
                RETURNING id_produto
                """,
                (sku, nome, preco, estoque)
            )

            produto_id = self.cursor.fetchone()[0]
            self.conexao.commit()

            return f"Produto cadastrado! ID: {produto_id}"

        except IntegrityError:
            self.conexao.rollback()
            return "Erro: SKU ja cadastrado ou dados invalidos."

        except Exception:
            self.conexao.rollback()
            raise

    def listar_produtos(self):
        self.cursor.execute(
            """
            SELECT id_produto, sku, nome, preco, estoque
            FROM produtos
            WHERE ativo = TRUE
            ORDER BY id_produto
            """
        )

        return self.cursor.fetchall()


    # ======================================
    # PEDIDOS
    # ======================================

    def criar_pedido(self, cliente_id, produto_id, quantidade):
        try:
            # Verificar se o cliente existe
            self.cursor.execute(
                "SELECT id_cliente FROM clientes WHERE id_cliente = %s",
                (cliente_id,)
            )

            if self.cursor.fetchone() is None:
                self.conexao.rollback()
                return "Erro: cliente nao encontrado."

            # Buscar produto e bloquear a linha durante a compra
            self.cursor.execute(
                """
                SELECT nome, preco, estoque
                FROM produtos
                WHERE id_produto = %s AND ativo = TRUE
                FOR UPDATE
                """,
                (produto_id,)
            )

            produto = self.cursor.fetchone()

            if produto is None:
                self.conexao.rollback()
                return "Erro: produto nao encontrado ou inativo."

            nome, preco, estoque = produto

            # Validar a quantidade
            if quantidade <= 0:
                self.conexao.rollback()
                return "Erro: quantidade deve ser maior que zero."

            if quantidade > estoque:
                self.conexao.rollback()
                return f"Erro: estoque insuficiente. Disponivel: {estoque}"

            # Calcular o valor total
            valor_total = preco * quantidade

            # Criar o pedido
            self.cursor.execute(
                """
                INSERT INTO pedidos (cliente_id, valor_total)
                VALUES (%s, %s)
                RETURNING id_pedido
                """,
                (cliente_id, valor_total)
            )

            pedido_id = self.cursor.fetchone()[0]

            # Registrar o produto comprado
            self.cursor.execute(
                """
                INSERT INTO itens_pedido
                    (pedido_id, produto_id, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s)
                """,
                (pedido_id, produto_id, quantidade, preco)
            )

            # Atualizar o estoque
            self.cursor.execute(
                """
                UPDATE produtos
                SET estoque = estoque - %s
                WHERE id_produto = %s
                """,
                (quantidade, produto_id)
            )

            # Confirmar todas as alteracoes
            self.conexao.commit()

            return (
                f"Pedido {pedido_id} criado com sucesso! "
                f"Produto: {nome} | "
                f"Quantidade: {quantidade} | "
                f"Total: R$ {valor_total:.2f}"
            )

        except Exception:
            self.conexao.rollback()
            raise


    # ======================================
    # ENCERRAR CONEXAO
    # ======================================

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
