
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
    # ENCERRAR CONEXAO
    # ======================================

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
