import asyncio
import os

import requests

from dotenv import load_dotenv
from pprint import pprint

from app.cnpj.client import CNPJClient
from app.embeddings.service import EmbeddingService
from app.matching.matcher import Matcher
from app.notification.notifier import Notify
from app.pncp.database import BidDatabase


load_dotenv()


def main():
    try:
        cnpj = os.getenv('CNPJ')

        company_client = CNPJClient(cnpj)
        embedding_service = EmbeddingService()
        bid_database = BidDatabase()

        bid_database.initialize()

        company = company_client.get_company_info()
        company["embedding"] = embedding_service.generate_company_embeddings(company)

        bids = bid_database.sync_bids()
        new_bids = embedding_service.generate_bid_embeddings(bids)

        for bid in new_bids:
            bid_database.update_bid_embedding(
                bid["id_pncp"],
                bid["embedding"]
            )

        bid_database.connection.commit()

        matcher = Matcher()
        matches = matcher.find_matching_bids(company, new_bids)

        notifier = Notify()
        asyncio.run(notifier.send_message(matches))
    
        #pprint(matches)

    except requests.exceptions.RequestException as error:
        print(f'Erro na requisição: {error}')


if __name__ == "__main__":
    main()

