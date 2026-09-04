import json
import sqlite3
from pathlib import Path

from .client import PNCPClient



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

        new_bids = []

        for item in pncp_response:

            # Essa condição pode ser tanto alterada, para conter outra modalidade, quanto retirada por completo
            if item["modalidadeNome"] != "Dispensa":
                continue

            bid = {
            "id_pncp": item["numeroControlePNCP"],
            "municipio": item["municipioNome"],
            "unidade": item["nomeUnidade"],
            "data_abertura": item["dataAberturaProposta"],
            "data_encerramento": item["dataEncerramentoProposta"],
            "objeto": item["objetoCompra"],
            "modalidade": item["modalidadeNome"],
            "link": item["linkSistemaOrigem"],
            }
            
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
                    bid["id_pncp"],
                    bid["municipio"],
                    bid["unidade"],
                    bid["data_abertura"],
                    bid["data_encerramento"],
                    bid["objeto"],
                    bid["modalidade"],
                    bid["link"],
                )
            )

            if self.cursor.rowcount > 0:
                new_bids.append(bid)

        self.connection.commit()

        return new_bids


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


    def update_bid_embedding(self, id_pncp, embedding):
        """
        Atualiza o embedding de uma licitação existente.

        Args:
            id_pncp: Identificador da licitação no PNCP.
            embedding: Vetor de embedding associado à licitação.
        """
        
        self.cursor.execute(
            """
            UPDATE licitacoes
            SET embedding = ?
            WHERE id_pncp = ?
            """,
            (
                json.dumps(embedding),
                id_pncp
            )
        )


    def initialize(self):
        """
        Inicializa a estrutura do banco e sincroniza as licitações
        disponíveis no PNCP.
        """
        self.create_db()
        

if __name__ == "__main__":

    db = BidDatabase()

    db.create_db()

    db.sync_bids()