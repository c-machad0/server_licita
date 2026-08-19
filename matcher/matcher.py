import json
import os

import numpy as np

from dotenv import load_dotenv

from cnpj_server.cnpj_client import CNPJClient
from embeddings.embedding_service import EmbeddingService
from pncp_server.pncp_database import BidDatabase


load_dotenv()

class Matcher:


    def __init__(self, cnpj):

        self.company_client = CNPJClient(cnpj)
        self.bid_database = BidDatabase()
        self.bid_database.initialize()
        self.embedding_service = EmbeddingService()
        

    def cosine_similarity(self, vector_a, vector_b) -> float:

        """
        Calcula similaridade entre dois embeddings.

        Retorno:
            valor entre -1 e 1

        Quanto mais próximo de 1,
        mais semelhantes são os textos.
        """

        a = np.array(vector_a)
        b = np.array(vector_b)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = np.dot(a, b) / (norm_a * norm_b)

        return float(similarity)

    
    def get_company_embedding(self) -> dict:
        """
        Obtém os dados da empresa e adiciona seu embedding ao dicionário
        de informações.

        Returns:
            dict: Dados da empresa contendo o embedding gerado.
        """

        company = self.company_client.get_company_info()

        company["embedding"] = self.embedding_service.generate_company_embedding(company)

        return company


    def get_bid_embeddings(self) -> list[dict]:
        """
        Obtém as licitações armazenadas no banco e garante que cada uma
        possua seu embedding.

        Returns:
            list[dict]: Lista de licitações contendo seus embeddings.
        """

        bids = self.bid_database.get_all_bids()

        self.embedding_service.generate_bid_embeddings(bids)

        result = []

        for bid in bids:

            if bid.get("embedding"):

                result.append({

                    "id":
                        bid["id"],

                    "objeto":
                        bid["objeto"],

                    "municipio":
                        bid["municipio"],

                    "unidade":
                        bid["unidade"],

                    "modalidade":
                        bid["modalidade"],

                    "data_abertura":
                        bid["data_abertura"],

                    "data_encerramento":
                        bid["data_encerramento"],

                    "embedding":
                        json.loads(
                            bid["embedding"]
                        )

                })

        return result


    def find_matching_bids(self) -> list[dict]:
        """
        Identifica as licitações semanticamente compatíveis com a empresa.

        As licitações são comparadas com o embedding da empresa e somente
        aquelas que atingem o limite mínimo de similaridade são retornadas.

        Returns:
            list[dict]: Licitações compatíveis ordenadas pela similaridade,
            da maior para a menor.
        """

        company = self.get_company_embedding()

        bids = self.get_bid_embeddings()

        similarity_threshold = float(os.getenv("MATCH_THRESHOLD", "0.50"))

        matches = []

        for bid in bids:

            score = self.cosine_similarity(
            company["embedding"],
            bid["embedding"]
            )

            if score >= similarity_threshold:

                matches.append({
                    "licitacao": bid["objeto"],
                    "modalidade": bid["modalidade"],
                    "unidade": bid["unidade"],
                    "municipio": bid["municipio"],
                    "data_abertura": bid["data_abertura"],
                    "data_encerramento": bid["data_encerramento"],
                    "similaridade": float(round(score * 100, 2))
                })

        return sorted(
            matches,
            key=lambda x:x["similaridade"],
            reverse=True
        )


if __name__ == "__main__":

    matcher = Matcher()

    resultados = matcher.find_matching_bids(
        threshold=0.50
    )

    for item in resultados:

        print("-"*50)

        print(
            f"""
Empresa:
{item['empresa']}

Licitação:
{item['licitacao']}

Município:
{item['municipio']}

Unidade:
{item['unidade']}

Modaliade:
{item['modalidade']}

Data de abertura:
{item['data_abertura']}

Data de encerramento:
{item['data_encerramento']}

Compatibilidade:
{item['similaridade']}%
"""
        )