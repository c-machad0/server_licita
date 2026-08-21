import asyncio
import os

from dotenv import load_dotenv
from pprint import pprint

from cnpj_server.cnpj_client import CNPJClient
from embeddings.embedding_service import EmbeddingService
from matcher.matcher import Matcher
from notification.notify import Notify
from pncp_server.pncp_database import BidDatabase


load_dotenv()


def main():
    cnpj = os.getenv('CNPJ')

    company_client = CNPJClient(cnpj)
    embedding_service = EmbeddingService()
    bid_database = BidDatabase()

    bid_database.initialize()

    company = company_client.get_company_info()
    company["embedding"] = embedding_service.generate_company_embedding(company)

    bids = bid_database.get_all_bids()
    new_bids = embedding_service.generate_bid_embeddings(bids)

    for bid in new_bids:
        bid_database.update_bid_embedding(
            bid["id"],
            bid["embedding"]
        )

    matcher = Matcher()
    matches = matcher.find_matching_bids(company, bids)

    notifier = Notify()
    asyncio.run(notifier.send_message(matches))
    
    #pprint(matches)

if __name__ == "__main__":
    main()

