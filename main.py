import sqlite3

from pprint import pprint

from cnpj_server.cnpj_database import CNPJDatabase
from pncp_server.pncp_database import PNCPDatabase
from embeddings.embedding_service import EmbeddingService
from matcher.matcher import Matcher


cnpj = CNPJDatabase()

try:
    cnpj.create_db()
except sqlite3.OperationalError as op_error:
    print(f'{op_error} - Tabela já existente')

try:
    cnpj.insert_company("50985285000135")
except sqlite3.IntegrityError as int_error:
    print(f'{int_error} - Dados de empresa, ja existentes')


pncp = PNCPDatabase()
pncp.create_db()
pncp.update_db()


embedding = EmbeddingService()
embedding.generate_company_embeddings()
embedding.generate_bid_embeddings()


matcher = Matcher()

pprint(
    matcher.match_company_bid()
)