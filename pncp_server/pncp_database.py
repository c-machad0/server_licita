import sqlite3
from pncp_client import PNCPClient


class PNCPDatabase:

    def __init__(self, client):
        self.db_connector = sqlite3.connect("licitacoes.db")
        self.db_cursor = self.db_connector.cursor()
        self.client = client

    def create_db(self):
        try:
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS licitacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    municipio TEXT NOT NULL,
                    unidade TEXT NOT NULL,
                    data_abertura TEXT NOT NULL,
                    data_encerramento TEXT NOT NULL,
                    objeto TEXT NOT NULL,
                    modalidade TEXT NOT NULL
                )
            """)
            self.db_connector.commit()

        except sqlite3.Error as e:
            print(f"Erro encontrado: {e}")



    def update_db(self):
        dados = self.client.filtrar_contratacoes()

        for item in dados:
            self.db_cursor.execute("""
                INSERT INTO licitacoes
                (municipio, unidade, data_abertura, data_encerramento, objeto, modalidade)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item["municipioNome"],
                item["nomeUnidade"],
                item["dataAberturaProposta"],
                item["dataEncerramentoProposta"],
                item["objetoCompra"],
                item["modalidadeNome"],
            ))

        self.db_connector.commit()


client = PNCPClient()

client.get_contratacoes()

database = PNCPDatabase(client)

database.create_db()
database.update_db()