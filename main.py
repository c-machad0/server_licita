import asyncio
import os
import time

import requests

from dotenv import load_dotenv

from app.cnpj.client import CNPJClient
from app.embeddings.service import EmbeddingService
from app.matching.matcher import Matcher
from app.notification.notifier import Notify
from app.pncp.database import BidDatabase

from logging_config import get_logger


load_dotenv()


def main():
    logger = get_logger(__name__)
    start_time = time.time()

    try:
        logger.info("Iniciando execução")

        cnpj = os.getenv("CNPJ")

        company_client = CNPJClient(cnpj)
        embedding_service = EmbeddingService()
        bid_database = BidDatabase()

        bid_database.initialize()

        company = company_client.get_company_info()
        company["embedding"] = embedding_service.generate_company_embeddings(company)

        bids = bid_database.sync_bids()
        new_bids = embedding_service.generate_bid_embeddings(bids)

        if not new_bids:
            logger.warning(
                "Nenhuma nova licitação encontrada para processamento. "
                "Sincronização concluída, mas não há novos registros para gerar embeddings."
            )

        for bid in new_bids:
            bid_database.update_bid_embedding(
                bid["id_pncp"],
                bid["embedding"]
            )

        bid_database.connection.commit()

        matcher = Matcher()
        matches = matcher.find_matching_bids(company, new_bids)

        if not matches:
            logger.warning(
                "Nenhuma licitação compatível encontrada para a empresa. "
            )

        notifier = Notify()
        asyncio.run(notifier.send_message(matches))

        logger.info(
            "Execução concluída em %.2f segundos | "
            "Embeddings de licitações geradas: %d | "
            "Licitações compatíveis encontradas: %d",
            time.time() - start_time,
            len(new_bids),
            len(matches)
        )

    except Exception:
        logger.exception("Erro inesperado durante execução")

    finally:
        logger.info("Fim da execução")

if __name__ == "__main__":
    main()

