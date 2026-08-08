import json
import sqlite3

from pathlib import Path

from .cnpj_client import CNPJClient


class CNPJDatabase:


    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent

        DATABASE_DIR = BASE_DIR / "databases"

        DATABASE_DIR.mkdir(exist_ok=True)

        db_path = DATABASE_DIR / "empresas.db"

        print(f"Banco empresas: {db_path}")

        self.db_connector = sqlite3.connect(db_path)

        self.db_connector.row_factory = sqlite3.Row

        self.db_cursor = self.db_connector.cursor()

        self.client = CNPJClient()


    def create_db(self):

        self.db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS empresas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnpj TEXT NOT NULL UNIQUE,
                razao_social TEXT NOT NULL,
                cnae_principal TEXT NOT NULL,
                cnaes_secundarios TEXT,
                embedding TEXT

            )
            """
        )

        self.db_connector.commit()


    def insert_company(self, cnpj):

        data = self.client.get_company_info(cnpj)

        self.db_cursor.execute(
            """
            INSERT INTO empresas

            (
                cnpj,
                razao_social,
                cnae_principal,
                cnaes_secundarios
            )

            VALUES (?, ?, ?, ?)

            """,
            (
                data["cnpj"],
                data["razao_social"],
                data["cnae_principal"],
                json.dumps(
                    data["cnaes_secundarios"],
                    ensure_ascii=False
                )
            )
        )

        self.db_connector.commit()


    def get_all_companies(self):

        self.db_cursor.execute(
            """
            SELECT *
            FROM empresas
            """
        )

        companies = []

        for row in self.db_cursor.fetchall():
            company = dict(row)

            company["cnaes_secundarios"] = json.loads(
                company["cnaes_secundarios"]
            )

            companies.append(company)

        return companies


    def update_embedding(self, id, embedding):

        self.db_cursor.execute(
            """
            UPDATE empresas

            SET embedding = ?

            WHERE id = ?

            """,

            (
                json.dumps(embedding),
                id
            )
        )

        self.db_connector.commit()

if __name__ == "__main__":

    db = CNPJDatabase()

    db.create_db()

    db.insert_company("61889727000166")