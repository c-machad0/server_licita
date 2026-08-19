import json

from .embedding_client import EmbeddingClient

from pncp_server.pncp_database import BidDatabase


class EmbeddingService:

    def __init__(self):

        self.bid_database = BidDatabase()
        self.embedding_client = EmbeddingClient()


    def generate_company_embedding(self, company) -> list[float]:
        """
        Gera o embedding a partir das atividades econômicas da empresa.

        Args:
            company: Dados da empresa, incluindo CNAE principal e
            atividades secundárias.

        Returns:
            list[float]: Vetor de embedding gerado para a empresa.
        """

        text = f"""
            Atividades econômicas da empresa:

            Atividade principal:
            {company['cnae_principal']}

            Atividades secundárias:
            {", ".join(company['cnaes_secundarios'])}
            """

        return self.embedding_client.embed(text)


    def generate_bid_embeddings(self, bids) -> None:
        """
        Gera os embeddings das licitações que ainda não possuem embedding.

        As licitações processadas também recebem o embedding gerado
        diretamente em seus respectivos dicionários.

        Args:
            bids: Lista de licitações a serem processadas.
        """

        for bid in bids:

            if bid.get("embedding"):
                continue

            text = f"""
            Objeto da contratação:
            {bid['objeto']}
            """

            embedding = self.embedding_client.embed(text)

            self.bid_database.update_bid_embedding(
                bid["id"],
                embedding
            )

            bid["embedding"] = json.dumps(embedding)


if __name__ == '__main__':
    service = EmbeddingService()

    service.generate_company_embedding()

    service.generate_bid_embeddings()
