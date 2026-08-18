# import json
import asyncio
from pprint import pprint

from cnpj_server.cnpj_client import CNPJClient
from pncp_server.pncp_database import PNCPDatabase
from embeddings.embedding_service import EmbeddingService
from matcher.matcher import Matcher
from notification.notify import Notify


def main():
    cnpj = '61889727000166'

    matches = Matcher(cnpj)
    result = matches.match_company_bid()

    notification = Notify()
    asyncio.run(notification.send_message(result))
    
    #pprint(result)

run = main()

