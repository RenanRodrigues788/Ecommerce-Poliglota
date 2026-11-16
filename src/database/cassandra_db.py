import os
import time
from cassandra.cluster import Cluster


class CassandraModule:

    def __init__(self):
        self.cluster = None
        self.session = None

        host = os.getenv("CASSANDRA_HOST", "cassandra")

        for tentativa in range(1, 7):
            try:
                self.cluster = Cluster([host], port=9042)
                self.session = self.cluster.connect(
                    "sistema_auditoria"
                )

                print("Conexao com Cassandra estabelecida!")
                break

            except Exception as erro:
                if self.cluster:
                    self.cluster.shutdown()
                    self.cluster = None

                if tentativa == 6:
                    raise ConnectionError(
                        f"Nao foi possivel conectar ao Cassandra: {erro}"
                    ) from erro

                print(
                    f"Cassandra indisponivel. "
                    f"Tentativa {tentativa}/6. "
                    f"Aguardando 10 segundos..."
                )

                time.sleep(10)

    def registrar_log_evento(self, cliente_id, acao, detalhe, pedido_id=None):
        from datetime import datetime, timezone

        query = """
        INSERT INTO logs_eventos (
            cliente_id,
            evento_id,
            pedido_id,
            acao,
            detalhe,
            data_evento
        )
        VALUES (%s, now(), %s, %s, %s, %s)
        """

        self.session.execute(
            query,
            (
                cliente_id,
                pedido_id,
                acao,
                detalhe,
                datetime.now(timezone.utc)
            )
        )

        print("Log de auditoria registrado com sucesso!")

    def listar_logs_cliente(self, cliente_id):
        query = """
        SELECT
            cliente_id,
            evento_id,
            pedido_id,
            acao,
            detalhe,
            data_evento
        FROM logs_eventos
        WHERE cliente_id = %s
        """

        resultados = self.session.execute(
            query,
            (cliente_id,)
        )

        return [
            {
                "cliente_id": registro.cliente_id,
                "evento_id": str(registro.evento_id),
                "pedido_id": registro.pedido_id,
                "acao": registro.acao,
                "detalhe": registro.detalhe,
                "data_evento": registro.data_evento
            }
            for registro in resultados
        ]

    def fechar_conexao(self):
        if self.cluster:
            self.cluster.shutdown()
            self.cluster = None
            self.session = None