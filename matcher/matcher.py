import os

import numpy as np


class Matcher:

    def __init__(self, threshold=None):

        self.threshold = float(os.getenv("MATCH_THRESHOLD", "0.50"))
        

    @staticmethod
    def cosine_similarity(vector_a, vector_b) -> float:

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


    def find_matching_bids(self, company, bids) -> list[dict]:
        """
        Identifica as licitações semanticamente compatíveis com a empresa.

        As licitações são comparadas com o embedding da empresa e somente
        aquelas que atingem o limite mínimo de similaridade são retornadas.

        Returns:
            list[dict]: Licitações compatíveis ordenadas pela similaridade,
            da maior para a menor.
        """

        matches = []

        for bid in bids:

            score = self.cosine_similarity(
            company["embedding"],
            bid["embedding"]
            )

            if score >= self.threshold:

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