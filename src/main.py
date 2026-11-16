
from database.postgres_db import PostgresModule


# ==========================================
# MENU PRINCIPAL
# ==========================================

def exibir_menu():
    print("\n" + "=" * 40)
    print("         E-COMMERCE POLIGLOTA")
    print("=" * 40)

    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Cadastrar produto")
    print("4 - Listar produtos")
    print("5 - Criar pedido")
    print("6 - Listar pedidos")
    print("0 - Sair")

    print("=" * 40)


# ==========================================
# SISTEMA PRINCIPAL
# ==========================================

def iniciar_sistema():

    try:
        postgres_db = PostgresModule()
        print("Conexao com PostgreSQL estabelecida!")

    except Exception as erro:
        print(f"Erro ao conectar ao PostgreSQL: {erro}")
        return

    try:
        while True:

            exibir_menu()
            opcao = input("Escolha uma opcao: ").strip()

            # CADASTRAR CLIENTE
            if opcao == "1":

                print("\n--- CADASTRAR CLIENTE ---")

                nome = input("Nome: ").strip()
                email = input("Email: ").strip()
                telefone = input("Telefone: ").strip()

                if not nome or not email:
                    print("Nome e email sao obrigatorios.")
                    continue

                resultado = postgres_db.cadastrar_cliente(
                    nome, email, telefone or None
                )

                print(resultado)

            # LISTAR CLIENTES
            elif opcao == "2":

                print("\n--- LISTA DE CLIENTES ---")

                clientes = postgres_db.listar_clientes()

                if not clientes:
                    print("Nenhum cliente cadastrado.")

                for cliente in clientes:
                    print(
                        f"ID: {cliente[0]} | "
                        f"Nome: {cliente[1]} | "
                        f"Email: {cliente[2]} | "
                        f"Telefone: {cliente[3]}"
                    )

            # CADASTRAR PRODUTO
            elif opcao == "3":

                print("\n--- CADASTRAR PRODUTO ---")

                sku = input("SKU: ").strip()
                nome = input("Nome do produto: ").strip()

                try:
                    preco = float(input("Preco: "))
                    estoque = int(input("Quantidade em estoque: "))

                except ValueError:
                    print("Preco ou estoque invalido.")
                    continue

                if not sku or not nome:
                    print("SKU e nome sao obrigatorios.")
                    continue

                resultado = postgres_db.cadastrar_produto(
                    sku, nome, preco, estoque
                )

                print(resultado)

            # LISTAR PRODUTOS
            elif opcao == "4":

                print("\n--- LISTA DE PRODUTOS ---")

                produtos = postgres_db.listar_produtos()

                if not produtos:
                    print("Nenhum produto cadastrado.")

                for produto in produtos:
                    print(
                        f"ID: {produto[0]} | "
                        f"SKU: {produto[1]} | "
                        f"Nome: {produto[2]} | "
                        f"Preco: R$ {produto[3]:.2f} | "
                        f"Estoque: {produto[4]}"
                    )


            # CRIAR PEDIDO
            elif opcao == "5":

                print("\n--- CRIAR PEDIDO ---")

                try:
                    cliente_id = int(input("ID do cliente: "))
                    produto_id = int(input("ID do produto: "))
                    quantidade = int(input("Quantidade: "))

                except ValueError:
                    print("Erro: informe apenas numeros inteiros.")
                    continue

                try:
                    resultado = postgres_db.criar_pedido(
                        cliente_id,
                        produto_id,
                        quantidade
                    )

                    print(resultado)

                except Exception as erro:
                    print(f"Erro ao criar pedido: {erro}")


            # LISTAR PEDIDOS
            elif opcao == "6":

                print("\n--- LISTA DE PEDIDOS ---")

                pedidos = postgres_db.listar_pedidos()

                if not pedidos:
                    print("Nenhum pedido cadastrado.")

                for pedido in pedidos:
                    print(
                        f"Pedido: {pedido[0]} | "
                        f"Cliente: {pedido[1]} | "
                        f"Produto: {pedido[2]} | "
                        f"Quantidade: {pedido[3]} | "
                        f"Preco unitario: R$ {pedido[4]:.2f} | "
                        f"Total do pedido: R$ {pedido[5]:.2f} | "
                        f"Status: {pedido[6]}"
                    )


            # SAIR
            elif opcao == "0":

                print("\nEncerrando o e-commerce...")
                break

            else:
                print("Opcao invalida.")

    finally:
        postgres_db.fechar_conexao()


# ==========================================
# INICIAR PROGRAMA
# ==========================================

if __name__ == "__main__":
    iniciar_sistema()
