# import json
import asyncio
from pprint import pprint

from cnpj_server.cnpj_database import CNPJDatabase
from pncp_server.pncp_database import PNCPDatabase
from embeddings.embedding_service import EmbeddingService
# from matcher.matcher import Matcher
from notification.notify import Notify

cnpj = CNPJDatabase()

cnpj.create_db()
cnpj.clear_company()
cnpj.insert_company("61889727000166")


pncp = PNCPDatabase()

pncp.create_db()
pncp.update_db()


embedding = EmbeddingService()

embedding.generate_company_embeddings()
embedding.generate_bid_embeddings()

notification = Notify()
asyncio.run(notification.send_message())

# matcher = Matcher()

# resultados = matcher.match_company_bid(
#     threshold=0.50
# )

# with open('match.json', 'w', encoding='utf-8') as file:
#     json.dump(resultados, file, ensure_ascii=False, indent=4)

