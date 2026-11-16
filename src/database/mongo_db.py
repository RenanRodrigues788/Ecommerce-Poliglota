
import os
from pymongo import MongoClient


class MongoModule:

    def __init__(self):
        # Configuracao da conexao com MongoDB
        usuario = os.getenv("MONGO_USER", "admin")
        senha = os.environ["MONGO_PASSWORD"]
        host = os.getenv("MONGO_HOST", "mongodb")

        self.client = MongoClient(
            host=host,
            port=27017,
            username=usuario,
            password=senha,
            authSource="admin",
            serverSelectionTimeoutMS=5000
        )

        # Verificar se o MongoDB esta acessivel
        self.client.admin.command("ping")

        # Banco e colecao do e-commerce
        self.db = self.client["ecommerce"]
        self.catalogo = self.db["catalogo_produtos"]

        # Evitar produtos duplicados
        self.catalogo.create_index(
            "produto_id",
            unique=True
        )

    # ======================================
    # CATALOGO DE PRODUTOS
    # ======================================

    def cadastrar_detalhes_produto(self, produto):
        if "produto_id" not in produto:
            return "Erro: produto_id obrigatorio."

        self.catalogo.update_one(
            {"produto_id": produto["produto_id"]},
            {"$set": produto},
            upsert=True
        )

        return "Detalhes do produto salvos com sucesso!"

    def buscar_detalhes_produto(self, produto_id):
        return self.catalogo.find_one(
            {"produto_id": produto_id},
            {"_id": 0}
        )

    def listar_catalogo(self):
        return list(
            self.catalogo.find(
                {},
                {"_id": 0}
            )
        )

    # ======================================
    # ENCERRAR CONEXAO
    # ======================================

    def fechar_conexao(self):
        self.client.close()
