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
                    "Connection": "keep-alive",
                })
        self.date_format()
        self.data = {}


    def date_format(self):
        date_today = datetime.today()
        future_date = date_today + timedelta(days=4)

        self.date_today_formatted = date_today.strftime("%Y%m%dT08:00:00")
        self.future_date_formatted = future_date.strftime("%Y%m%dT08:00:00")


    def get_contratacoes(self):
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
            return self.data

        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
            self.data = {}
            return {}


    def filtrar_contratacoes(self):

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
    client.get_contratacoes() # Captura todas as licitações
    filter_response = client.filtrar_contratacoes() # Filtra somente as informações necessárias

    pprint(filter_response)