import json
import numpy as np

from cnpj_server.cnpj_database import CNPJDatabase
from pncp_server.pncp_database import PNCPDatabase



class Matcher:


    def __init__(self):

        self.company_db = CNPJDatabase()
        self.licitacao_db = PNCPDatabase()



    def cosine_similarity(
            self,
            vector_a,
            vector_b
        ):

        """
        Calcula similaridade entre dois embeddings

        Retorno:
            valor entre -1 e 1

        Quanto mais próximo de 1,
        mais semelhantes são os textos.
        """

        a = np.array(vector_a)

        b = np.array(vector_b)


        similarity = np.dot(a,b) / (
            np.linalg.norm(a) *
            np.linalg.norm(b)
        )


        return similarity



    def get_companies_embeddings(self):

        companies = self.company_db.get_all_companies()


        result = []


        for company in companies:

            if company.get("embedding"):


                result.append({

                    "id":
                        company["id"],

                    "razao_social":
                        company["razao_social"],

                    "embedding":
                        json.loads(company["embedding"])

                })


        return result



    def get_bids_embeddings(self):

        bids = self.licitacao_db.list_db()


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

                    "embedding":
                        json.loads(
                            bid["embedding"]
                        )

                })


        return result




    def match_company_bid(
            self,
            company_id=None,
            threshold=0.70
        ):

        """
        Retorna licitações compatíveis
        com empresas.

        threshold:
            percentual mínimo de similaridade
        """


        companies = self.get_companies_embeddings()

        bids = self.get_bids_embeddings()


        matches = []


        for company in companies:


            if company_id and company["id"] != company_id:
                continue



            for bid in bids:


                score = self.cosine_similarity(
                    company["embedding"],
                    bid["embedding"]
                )


                if score >= threshold:


                    matches.append({

                        "empresa":
                            company["razao_social"],


                        "licitacao":
                            bid["objeto"],


                        "municipio":
                            bid["municipio"],


                        "similaridade":
                            round(
                                score * 100,
                                2
                            )

                    })


        return sorted(
            matches,
            key=lambda x:x["similaridade"],
            reverse=True
        )




if __name__ == "__main__":


    matcher = Matcher()


    resultados = matcher.match_company_bid(
        threshold=0.75
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


Compatibilidade:
{item['similaridade']}%
"""
        )