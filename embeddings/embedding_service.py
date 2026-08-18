from .embedding_client import EmbeddingClient

from pncp_server.pncp_database import PNCPDatabase
from cnpj_server.cnpj_database import CNPJClient


class EmbeddingService:

    def __init__(self):

        self.licitacao_db = PNCPDatabase()
        self.embedding_client = EmbeddingClient()


    def generate_company_embeddings(self, company):

        text = f"""
            Atividades econômicas da empresa:

            Atividade principal:
            {company['cnae_principal']}

            Atividades secundárias:
            {", ".join(company['cnaes_secundarios'])}
            """

        return self.embedding_client.embed(text)


    def generate_bid_embeddings(self):
        licitacoes = self.licitacao_db.list_db()

        for licitacao in licitacoes:

            if licitacao.get("embedding"):
                continue
            
            text=f"""
            Objeto da contratação:
            {licitacao['objeto']}
            """
            embedding=self.embedding_client.embed(text)

            self.licitacao_db.update_embedding(licitacao["id"], embedding)


if __name__ == '__main__':
    service = EmbeddingService()

    service.generate_company_embeddings()

    service.generate_bid_embeddings()
