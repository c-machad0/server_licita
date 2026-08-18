# import json
import asyncio
from pprint import pprint

from cnpj_server.cnpj_client import CNPJClient
from pncp_server.pncp_database import PNCPDatabase
from embeddings.embedding_service import EmbeddingService
# from matcher.matcher import Matcher
from notification.notify import Notify


def main():
    client_cnpj = CNPJClient()
    service_embedding = EmbeddingService()

    cnpj = '61889727000166'

    company = client_cnpj.get_company_info(cnpj)

    company["embedding"] = service_embedding.generate_company_embeddings(company)

    pprint(company)

run = main()

