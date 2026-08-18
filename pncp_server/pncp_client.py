import requests

from datetime import datetime, timedelta
from pprint import pprint


class PNCPClient:

    def __init__(self):
        self.__base_url = "https://pncp.gov.br/api/consulta"
        self.session = requests.Session()
        self.session.headers.update({
                    "Accept": "application/json",
                    "User-Agent": "PostmanRuntime/7.43.0",
                })
        self.date_format()
        self.data = {}


    def date_format(self):
        date_today = datetime.today()
        future_date = date_today + timedelta(days=4)

        self.date_today_formatted = date_today.strftime("%Y%m%dT08:00:00")
        self.future_date_formatted = future_date.strftime("%Y%m%dT08:00:00")


    def get_pncp_contracts(self):
        url = f"{self.__base_url}/v1/contratacoes/proposta"

        params = {
            "pagina": 1,
            "tamanhoPagina": 50,
            "dataInicial": self.date_today_formatted,
            "dataFinal": self.future_date_formatted,
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
                filter_contracts = self.filter_pncp_contracts()

                return filter_contracts

        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
            self.data = {}
            return []


    def filter_pncp_contracts(self):

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
    filter_response = client.get_pncp_contracts() # Captura todas as licitações
    # filter_response = client.filter_pncp_contracts() # Filtra somente as informações necessárias

    pprint(filter_response)