from .embedding_client import EmbeddingClient

from pncp_server.pncp_database import PNCPDatabase
from cnpj_server.cnpj_database import CNPJDatabase


class EmbeddingService:

    def __init__(self):

        self.company_db = CNPJDatabase()
        self.licitacao_db = PNCPDatabase()
        self.embedding_client = EmbeddingClient()



    def generate_company_embeddings(self):

        companies = self.company_db.get_all_companies()

        print(
            f"{len(companies)} empresas encontradas"
        )


        for company in companies:

            if company.get("embedding"):
                continue


            text = f"""
            Empresa:
            {company['razao_social']}

            CNAE Principal:
            {company['cnae_principal']}

            CNAEs Secundários:
            {", ".join(company['cnaes_secundarios'])}
            """


            embedding = self.embedding_client.embed(
                text
            )


            self.company_db.update_embedding(
                company["id"],
                embedding
            )



    def generate_bid_embeddings(self):
        licitacoes = self.licitacao_db.list_db()

        for licitacao in licitacoes:

            if licitacao.get("embedding"):
                continue
            
            text=f"""

            Objeto:
            {licitacao['objeto']}


            Modalidade:
            {licitacao['modalidade']}


            Município:
            {licitacao['municipio']}
            """
            embedding=self.embedding_client.embed(text)

            self.licitacao_db.update_embedding(
                licitacao["id"],
                embedding
            )

if __name__ == '__main__':
    service = EmbeddingService()


    service.generate_company_embeddings()

    service.generate_bid_embeddings()
