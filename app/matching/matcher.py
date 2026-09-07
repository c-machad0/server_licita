import os

import numpy as np

from logging_config import get_logger


class Matcher:

    def __init__(self, threshold=None):

        self.threshold = (
            threshold
            if threshold is not None
            else float(os.getenv("MATCH_THRESHOLD", "0.50"))
            )

        self.logger = get_logger(__name__)
        

    @staticmethod
    def cosine_similarity(vector_a, vector_b) -> float:

        """
        Calcula a similaridade de cosseno entre dois vetores. 
        
        A similaridade varia teoricamente entre -1 e 1. Quanto mais próximo 
        de 1, maior a similaridade entre os vetores. Caso algum vetor possua 
        norma zero, retorna 0.0 para evitar divisão por zero. 
        
        Args: 
            vector_a: Primeiro vetor numérico. 
            vector_b: Segundo vetor numérico. 
        
        Returns: 
            float: Valor da similaridade de cosseno entre os dois vetores. 
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
        Identifica as licitações semanticamente compatíveis com as atividades
        econômicas da empresa.

        Cada atividade econômica da empresa é comparada com o embedding de 
        cada licitação. Uma licitação é considerada compatível quando pelo 
        menos uma  atividade apresenta similaridade igual ou superior ao 
        threshold configurado.

        As atividades compatíveis são incluídas no resultado e ordenadas 
        pela maior similaridade.

        
        Args: 
            company: Dados da empresa contendo seus embeddings de atividades. 
            bids: Lista de licitações contendo seus respectivos embeddings.
            
        Returns:
            list[dict]: Licitações compatíveis ordenadas pela similaridade, 
            da maior para a menor.
        """
        self.logger.info("Iniciando processo de matching.")

        matches = []

        for bid in bids:

            activities = []

            for activity in company["embedding"]:

                score = self.cosine_similarity(
                activity["embedding"],
                bid["embedding"]
                )

                if score >= self.threshold:
                    activities.append({
                        "atividade": activity["atividade"],
                        "similaridade": round(score * 100, 2)
                    })

            if activities:
                matches.append({
                    "licitacao": bid["objeto"],
                    "modalidade": bid["modalidade"],
                    "unidade": bid["unidade"],
                    "municipio": bid["municipio"],
                    "data_abertura": bid["data_abertura"],
                    "data_encerramento": bid["data_encerramento"],
                    "link": bid["link"],
                    "atividades": sorted(
                        activities,
                        key=lambda x:x["similaridade"],
                        reverse=True
                    )
                })
        self.logger.info(
            "Matching concluído | licitações analisadas=%d | "
            "compatíveis=%d | threshold=%.2f",
            len(bids),
            len(matches),
            self.threshold
        )

        return matches