import json

from .client import EmbeddingClient
from logging_config import get_logger


class EmbeddingService:

    def __init__(self):

        self.embedding_client = EmbeddingClient()
        self.logger = get_logger(__name__)


    def generate_company_embeddings(self, company) -> list[dict]:
        """
        Gera o embedding a partir das atividades econômicas da empresa.

        Args:
            company: Dados da empresa, incluindo CNAE principal e
            atividades secundárias.

        Returns:
            list[dict]: Vetor de embedding gerado para a empresa.
        """

        activities = [
            company["cnae_principal"],
            *company["cnaes_secundarios"]
        ]

        self.logger.info("Gerando embeddings da empresa | atividades=%d",
                         len(activities)
        )

        embeddings = []

        for activity in activities:
            if not activity:
                continue

            text = f"Atividade econômica: {activity}"

            embeddings.append({
                "atividade": activity,
                "embedding": self.embedding_client.embed(text)
            })

        self.logger.info(
                "Embeddings da empresa gerados | quantidade=%d",
                len(embeddings)
            )
        
        return embeddings


    def generate_bid_embeddings(self, bids) -> list[dict]:
        """
        Gera embeddings para licitações que ainda não possuem embedding.

        Licitações que já possuem um embedding são mantidas sem uma nova 
        chamada à API. Os embeddings existentes são desserializados para 
        listas Python e as licitações que receberam novos embeddings são 
        retornadas.

        Args: 
            bids: Lista de licitações a serem processadas.

        Returns:
            list[dict]: Lista contendo apenas as licitações que receberam 
            um novo embedding.
        """

        self.logger.info("Gerando embeddings da das licitações | quantidade=%d",
                        len(bids)
        )

        generated_bids = []

        for bid in bids:
            if bid.get("embedding"):
                bid["embedding"] = json.loads(bid["embedding"])
                continue

            text = f"Objeto da contratação: {bid['objeto']}"

            embedding = self.embedding_client.embed(text)

            bid["embedding"] = embedding
            generated_bids.append(bid)


        self.logger.info(
                "Embeddings das licitações gerados | quantidade=%d",
                len(generated_bids)
        )
        
        return generated_bids