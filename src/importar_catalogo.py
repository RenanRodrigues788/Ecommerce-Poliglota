import json

from database.mongo_db import MongoModule


def importar_catalogo():
    with open("/app/catalogo.json", "r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

    mongo = MongoModule()

    try:
        for produto in produtos:
            resultado = mongo.cadastrar_detalhes_produto(produto)
            print(f"Produto {produto['produto_id']}: {resultado}")
    finally:
        mongo.fechar_conexao()


if __name__ == "__main__":
    importar_catalogo()
