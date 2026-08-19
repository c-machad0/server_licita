from pprint import pprint

import requests


class CNPJClient:

    def __init__(self, cnpj):

        self.__base_url = "https://brasilapi.com.br/api/"

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "pncp-client/1.0",
            "Accept": "application/json",
        })

        self.cnpj = cnpj


    def get_company_info(self) -> dict:
        """
        Consulta a BrasilAPI utilizando o CNPJ configurado e retorna
        as principais informações cadastrais e atividades econômicas
        da empresa.

        Returns:
            dict: Dados da empresa, incluindo razão social, CNPJ,
            CNAE principal e CNAEs secundários.
        """

        url = f"{self.__base_url}cnpj/v1/{self.cnpj}"

        response = self.session.get(
            url,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return {

            "razao_social":
                data.get("razao_social"),

            "cnpj":
                data.get("cnpj"),

            "cnae_principal":
                data.get("cnae_fiscal_descricao"),

            "cnaes_secundarios":
                [
                    cnae.get("descricao")
                    for cnae in data.get(
                        "cnaes_secundarios",
                        []
                    )
                ]
        }

if __name__ == '__main__':
    client = CNPJClient("61889727000166")
    empresa = client.get_company_info()

    pprint(empresa)