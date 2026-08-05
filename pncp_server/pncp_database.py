import sqlite3
import json

from pathlib import Path

from .pncp_client import PNCPClient



class PNCPDatabase:


    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent

        DATABASE_DIR = BASE_DIR / "databases"

        DATABASE_DIR.mkdir(
            exist_ok=True
        )


        db_path = DATABASE_DIR / "licitacoes.db"


        self.db_connector = sqlite3.connect(
            db_path
        )


        self.db_connector.row_factory = sqlite3.Row


        self.db_cursor = self.db_connector.cursor()



    def create_db(self):

        self.db_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS licitacoes(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                municipio TEXT,

                unidade TEXT,

                data_abertura TEXT,

                data_encerramento TEXT,

                objeto TEXT UNIQUE,

                modalidade TEXT,

                embedding TEXT

            )
            """
        )


        self.db_connector.commit()



    def update_db(self):

        client = PNCPClient()

        client.get_contratacoes()


        for item in client.filtrar_contratacoes():

            self.db_cursor.execute(
                """
                INSERT OR IGNORE INTO licitacoes

                (
                    municipio,
                    unidade,
                    data_abertura,
                    data_encerramento,
                    objeto,
                    modalidade
                )

                VALUES (?, ?, ?, ?, ?, ?)

                """,

                (

                    item["municipioNome"],

                    item["nomeUnidade"],

                    item["dataAberturaProposta"],

                    item["dataEncerramentoProposta"],

                    item["objetoCompra"],

                    item["modalidadeNome"]

                )
            )


        self.db_connector.commit()



    def list_db(self):

        self.db_cursor.execute(
            """
            SELECT * FROM licitacoes
            """
        )


        return [
            dict(row)
            for row in self.db_cursor.fetchall()
        ]



    def update_embedding(
            self,
            id,
            embedding
        ):


        self.db_cursor.execute(
            """
            UPDATE licitacoes

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

    db = PNCPDatabase()

    db.create_db()

    db.update_db()