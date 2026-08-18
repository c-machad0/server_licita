import json
import numpy as np

from cnpj_server.cnpj_client import CNPJClient
from embeddings.embedding_service import EmbeddingService
from pncp_server.pncp_database import PNCPDatabase


class Matcher:


    def __init__(self, cnpj):

        self.company_data = CNPJClient(cnpj)
        self.licitacao_db = PNCPDatabase()
        self.licitacao_db.run_database()
        self.service_embeddings = EmbeddingService()
        

    def cosine_similarity(self, vector_a, vector_b):

        """
        Calcula similaridade entre dois embeddings

        Retorno:
            valor entre -1 e 1

        Quanto mais próximo de 1,
        mais semelhantes são os textos.
        """

        a = np.array(vector_a)
        b = np.array(vector_b)

        similarity = np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

        return similarity


    def get_company_embedding(self):

        company = self.company_data.get_company_info()

        company["embedding"] = self.service_embeddings.generate_company_embeddings(company)

        return company


    def get_bids_embeddings(self):

        bids = self.licitacao_db.list_db()

        self.service_embeddings.generate_bid_embeddings(bids)

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


    def match_company_bid(self):

        """
        Retorna licitações compatíveis
        com empresas.

        threshold:
            percentual mínimo de similaridade
        """

        company = self.get_company_embedding()

        bids = self.get_bids_embeddings()

        threshold=0.50

        matches = []

        for bid in bids:

            score = self.cosine_similarity(
            company["embedding"],
            bid["embedding"]
            )

            if score >= threshold:

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

    resultados = matcher.match_company_bid(
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