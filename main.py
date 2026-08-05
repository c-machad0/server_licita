from cnpj_server.cnpj_database import CNPJDatabase
from pncp_server.pncp_database import PNCPDatabase
from embeddings.embedding_service import EmbeddingService
from matcher.matcher import Matcher



cnpj = CNPJDatabase()
cnpj.create_db()
cnpj.insert_company("61889727000166")


pncp = PNCPDatabase()
pncp.create_db()
pncp.update_db()


embedding = EmbeddingService()
embedding.generate_company_embeddings()
embedding.generate_bid_embeddings()


matcher = Matcher()

print(
    matcher.match_company_bid()
)