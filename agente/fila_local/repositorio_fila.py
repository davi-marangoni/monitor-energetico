import json
import sqlite3
from pathlib import Path


class RepositorioFilaLocal:
    def __init__(self, caminho_banco="fila_agente.sqlite3"):
        self.caminho = Path(caminho_banco)
        self._inicializar()

    def _conexao(self):
        return sqlite3.connect(self.caminho)

    def _inicializar(self):
        with self._conexao() as conexao:
            conexao.execute(
                """
                CREATE TABLE IF NOT EXISTS fila_telemetria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payload TEXT NOT NULL
                )
                """
            )

    def enfileirar(self, telemetria):
        with self._conexao() as conexao:
            conexao.execute("INSERT INTO fila_telemetria (payload) VALUES (?)", (json.dumps(telemetria),))

    def listar(self, limite=1000):
        with self._conexao() as conexao:
            linhas = conexao.execute("SELECT id, payload FROM fila_telemetria ORDER BY id ASC LIMIT ?", (limite,)).fetchall()
        return [{"id": linha[0], "payload": json.loads(linha[1])} for linha in linhas]

    def remover(self, ids):
        if not ids:
            return
        with self._conexao() as conexao:
            conexao.executemany("DELETE FROM fila_telemetria WHERE id = ?", [(item,) for item in ids])
