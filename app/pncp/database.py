import json
import sqlite3
from pathlib import Path

from .client import PNCPClient
from logging_config import get_logger



class BidDatabase:

    def __init__(self):

        self.logger = get_logger(__name__)

        base_dir = Path(__file__).resolve().parent.parent
        database_dir = base_dir / "databases"

        database_dir.mkdir(parents=True, exist_ok=True)

        db_path = database_dir / "licitacoes.db"

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_db()


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

        self.logger.info("Tabela 'licitacoes' verificada/criada com sucesso.")


    def sync_bids(self):
        """
        Consulta as licitações disponíveis no PNCP e sincroniza os dados
        com a tabela local de licitações.
        """

        self.logger.info("Sicronizando os dados...")

        client = PNCPClient()
        pncp_response = client.get_pncp_bids()

        if not pncp_response:
            self.logger.warning(
                "PNCP não retornou licitações para o período consultado."
            )
            return []

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
        self.logger.info("Dados sincronizados com sucesso!")

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

        try:
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
        except sqlite3.Error:
            self.logger.exception(
                "Erro ao atualizar embedding | id_pncp=%s",
                id_pncp
            )
            raise


if __name__ == "__main__":

    db = BidDatabase()

    db.create_db()

    db.sync_bids()