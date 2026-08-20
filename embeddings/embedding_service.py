import json

from .embedding_client import EmbeddingClient


class EmbeddingService:

    def __init__(self):

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
        Gera embeddings para licitações que ainda não possuem embedding.

        Retorna:
            Lista de licitações que receberam um novo embedding.
        """

        generated_bids = []

        for bid in bids:
            if bid.get("embedding"):
                bid["embedding"] = json.loads(bid["embedding"])
                continue

            text = f"""
            Objeto da contratação:
            {bid['objeto']}
            """

            embedding = self.embedding_client.embed(text)

            bid["embedding"] = embedding
            generated_bids.append(bid)

        return generated_bids