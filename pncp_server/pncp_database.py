import json
import sqlite3
from pathlib import Path

from .pncp_client import PNCPClient



class BidDatabase:


    def __init__(self):

        base_dir = Path(__file__).resolve().parent.parent

        database_dir = base_dir / "databases"

        database_dir.mkdir(exist_ok=True)

        db_path = database_dir / "licitacoes.db"

        self.connection = sqlite3.connect(db_path)

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()


    def create_db(self):
        """
        Cria a tabela de licitações caso ela ainda não exista.
        """

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS licitacoes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pncp TEXT UNIQUE NOT NULL,
                municipio TEXT,
                unidade TEXT,
                data_abertura TEXT,
                data_encerramento TEXT,
                objeto TEXT,
                modalidade TEXT,
                link TEXT,
                embedding TEXT
            )
            """
        )

        self.connection.commit()


    def sync_bids(self):
        """
        Consulta as licitações disponíveis no PNCP e sincroniza os dados
        com a tabela local de licitações.
        """

        client = PNCPClient()
        pncp_response = client.get_pncp_bids()

        for item in pncp_response:

            self.cursor.execute(
                """
                INSERT OR IGNORE INTO licitacoes

                (   
                    id_pncp,
                    municipio,
                    unidade,
                    data_abertura,
                    data_encerramento,
                    objeto,
                    modalidade,
                    link
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

                """,

                (   
                    item["numeroControlePNCP"],
                    item["municipioNome"],
                    item["nomeUnidade"],
                    item["dataAberturaProposta"],
                    item["dataEncerramentoProposta"],
                    item["objetoCompra"],
                    item["modalidadeNome"],
                    item["linkSistemaOrigem"],
                )
            )

        self.connection.commit()


    def get_all_bids(self) -> list[dict]:
        """
        Retorna todas as licitações armazenadas no banco de dados.

        Returns:
            list[dict]: Lista de licitações representadas como dicionários.
        """
        modalidade = 'Dispensa'

        self.cursor.execute(
            """
            SELECT * FROM licitacoes WHERE modalidade = ?
            """,
            (modalidade,)
        )

        return [
            dict(row)
            for row in self.cursor.fetchall()
        ]


    def update_bid_embedding(self, bid_id, embedding):
        """
        Atualiza o embedding de uma licitação existente.

        Args:
            bid_id: Identificador da licitação.
            embedding: Vetor de embedding associado à licitação.
        """
        
        self.cursor.execute(
            """
            UPDATE licitacoes
            SET embedding = ?
            WHERE id = ?
            """,
            (
                json.dumps(embedding),
                bid_id
            )
        )
        
        self.connection.commit()


    def initialize(self):
        """
        Inicializa a estrutura do banco e sincroniza as licitações
        disponíveis no PNCP.
        """
        self.create_db()
        self.sync_bids()
        

if __name__ == "__main__":

    db = BidDatabase()

    db.create_db()

    db.sync_bids()