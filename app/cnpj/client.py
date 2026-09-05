from pprint import pprint

import requests

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from logging_config import get_logger

class CNPJClient:

    def __init__(self, cnpj):

        self.logger = get_logger(__name__)

        self.__base_url = "https://brasilapi.com.br/api/"

        retry_strategy = Retry(
            total=3,
            status_forcelist=[408, 429, 500, 502, 504],
            allowed_methods=['GET'],
            backoff_factor=1,
            respect_retry_after_header=True
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session = requests.Session()
        self.session.mount("https://", adapter)

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

        try:
            self.logger.info("Coletando dados da empresa.")

            response = self.session.get(
                url,
                timeout=(5, 15)
            )

            response.raise_for_status()

            data = response.json()

            self.logger.info("Coleta de dados feita com sucesso!")

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
        
        except requests.exceptions.RequestException:
            self.logger.exception("Falha na requisição HTTP")
            raise

if __name__ == '__main__':
    client = CNPJClient("61889727000166")
    empresa = client.get_company_info()

    pprint(empresa)