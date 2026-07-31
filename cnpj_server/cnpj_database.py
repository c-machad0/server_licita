import json
import sqlite3
from cnpj_client import CNPJClient


class CNPJDatabase:

    def __init__(self):
        self.db_connector = sqlite3.connect('empresas.db')
        self.db_cursor = self.db_connector.cursor()

        self.client = CNPJClient()

    def create_db(self):
        try:
            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnpj TEXT NOT NULL UNIQUE,
                razao_social TEXT NOT NULL,
                cnae_principal TEXT NOT NULL,
                cnaes_secundarios TEXT
            )
            """)

            self.db_connector.commit()

        except sqlite3.Error as e:
            print(f'Erro encontrado: {e}')


    def update_table(self):
        data = self.client.filter_info()

        self.db_cursor.execute(
        """
        INSERT INTO empresas
        (cnpj, razao_social, cnae_principal, cnaes_secundarios)
        VALUES (?, ?, ?, ?)
        """,
        (
            data["cnpj"],
            data["razao_social"],
            data["cnae_principal"],
            json.dumps(data["cnaes_secundarios"], ensure_ascii=False)
        )
    )

        self.db_connector.commit()

database = CNPJDatabase()

database.create_db()

database.client.get_cnpj('61889727000166')

database.update_table()
