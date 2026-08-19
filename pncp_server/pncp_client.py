from datetime import datetime, timedelta
from pprint import pprint

import requests


class PNCPClient:

    def __init__(self):
        self.__base_url = "https://pncp.gov.br/api/consulta"
        self.session = requests.Session()
        self.session.headers.update({
                    "Accept": "application/json",
                    "User-Agent": "server-licita/0.1",
                })
        self.configure_date_range()
        self.data = {}


    def configure_date_range(self):
        """
        Configura o intervalo de datas utilizado nas consultas ao PNCP.

        Define a data inicial como a data atual e a data final como quatro
        dias após a data atual, ambas formatadas no padrão esperado pela API.
        """
        date_today = datetime.today()
        future_date = date_today + timedelta(days=4)

        self.start_date = date_today.strftime("%Y%m%dT08:00:00")
        self.end_date = future_date.strftime("%Y%m%dT08:00:00")


    def get_pncp_bids(self) -> list[dict]:
        """
        Consulta as contratações disponíveis no PNCP dentro do período
        configurado e retorna os dados filtrados para o sistema.
        """

        url = f"{self.__base_url}/v1/contratacoes/proposta"

        params = {
            "pagina": 1,
            "tamanhoPagina": 50,
            "dataInicial": self.start_date,
            "dataFinal": self.end_date,
            "uf": "BA",
        }

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=(10, 60)
            )

            response.raise_for_status()

            self.data = response.json()

            if self.data:
                filter_contracts = self.format_bids()

                return filter_contracts

        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
            self.data = {}
            return []


    def format_bids(self) -> list[dict]:
        """
        Extrai e organiza os campos relevantes das contratações retornadas
        pela API do PNCP.

        Returns:
            list[dict]: Lista contendo município, unidade, datas, objeto
            e modalidade de cada contratação.
        """

        return [
            {
                "nomeUnidade": item.get("unidadeOrgao", {}).get("nomeUnidade"),
                "municipioNome": item.get("unidadeOrgao", {}).get("municipioNome"),
                "dataAberturaProposta": item.get("dataAberturaProposta"),
                "dataEncerramentoProposta": item.get("dataEncerramentoProposta"),
                "objetoCompra": item.get("objetoCompra"),
                "modalidadeNome": item.get("modalidadeNome"),
            }
            for item in self.data.get("data", [])
        ]


if __name__ == "__main__":

    client = PNCPClient()
    filter_response = client.get_pncp_bids() # Captura todas as licitações
    # filter_response = client.filter_pncp_contracts() # Filtra somente as informações necessárias

    pprint(filter_response)