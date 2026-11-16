#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo " INICIALIZACAO DO E-COMMERCE POLIGLOTA"
echo "========================================"

echo "[1/3] Preparando Cassandra..."
docker compose exec -T cassandra cqlsh < cassandra.sql

echo "[2/3] Preparando Neo4j..."
docker compose exec -T app_python python - <<'PY'
from pathlib import Path
from database.neo4j_db import executar_query

script = Path("/dados/queries.cypher").read_text(encoding="utf-8")

linhas = [
    linha for linha in script.splitlines()
    if linha.strip() and not linha.strip().startswith("//")
]

comandos = [
    comando.strip()
    for comando in "\n".join(linhas).split(";")
    if comando.strip()
]

for numero, comando in enumerate(comandos, start=1):
    executar_query(comando)
    print(f"  Comando Cypher {numero}: OK")

print(f"  {len(comandos)} comandos executados.")
PY

echo "[3/3] Importando catalogo MongoDB..."
docker compose exec -T app_python python importar_catalogo.py

echo "========================================"
echo " INICIALIZACAO CONCLUIDA COM SUCESSO!"
echo "========================================"
