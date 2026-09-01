import json
import time

from datetime import datetime, timedelta
from pprint import pprint

import requests

from requests.adapters import HTTPAdapter
from urllib3 import Retry


class PNCPClient:

    def __init__(self):
        self.__base_url = "https://pncp.gov.br/api/consulta"

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
                    "Accept": "application/json",
                    "User-Agent": "server-licita/0.1",
                })
        
        self.configure_date_range()


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


    def get_pncp_bids(self):
        """
        Consulta as licitações disponíveis no PNCP no período configurado.

        A consulta percorre todas as páginas disponíveis e retorna as licitações
        encontradas em uma única lista.

        Returns:
        list[dict]: Lista contendo todas as licitações encontradas.
        """
        return self.bid_pagination()


    def fetch_page(self, page) -> list[dict]:
        """
        Consulta uma página de licitações disponíveis no PNCP.

        Args:
            page (int): Número da página a ser consultada.

        Returns:
        list[dict]: Lista de licitações encontradas na página. Retorna uma
            lista vazia quando a API não possui mais registros.
        """

        url = f"{self.__base_url}/v1/contratacoes/proposta"

        params = {
            "pagina": page,
            "tamanhoPagina": 50,
            "dataInicial": self.start_date,
            "dataFinal": self.end_date,
            "uf": "BA",
        }

        response = self.session.get(
            url,
            params=params,
            timeout=(10, 60)
        )

        response.raise_for_status()
        
        if response.status_code == 204:
            return []
        
        bid_data = response.json()

        return self.format_bids(bid_data)


    def bid_pagination(self) -> list[dict]:
        """
        Percorre sequencialmente as páginas de licitações do PNCP.

        A consulta continua enquanto houver registros. Quando a API retorna uma
        página sem conteúdo, a paginação é encerrada.

        Returns:
        list[dict]: Lista contendo todas as licitações encontradas em todas
            as páginas consultadas.
        """
        
        page = 1
        bids = []

        while True:
            response = self.fetch_page(page)

            if not response:
                break

            bids.extend(response)
            page += 1

            time.sleep(2)
            
        return bids


    def format_bids(self, data) -> list[dict]:
        """
        Extrai e organiza os campos relevantes das contratações retornadas
        pela API do PNCP.

        Args:
        data (dict): Resposta da API do PNCP contendo as licitações no campo
            ``data``.

        Returns:
            list[dict]: Lista contendo município, unidade, datas, objeto
            e modalidade de cada contratação.
        """

        return [
            {   "numeroControlePNCP": item.get("numeroControlePNCP"),
                "nomeUnidade": item.get("unidadeOrgao", {}).get("nomeUnidade"),
                "municipioNome": item.get("unidadeOrgao", {}).get("municipioNome"),
                "dataAberturaProposta": item.get("dataAberturaProposta"),
                "dataEncerramentoProposta": item.get("dataEncerramentoProposta"),
                "objetoCompra": item.get("objetoCompra"),
                "modalidadeNome": item.get("modalidadeNome"),
                "linkSistemaOrigem": item.get("linkSistemaOrigem"),
            }
            for item in data.get("data", [])
        ]


if __name__ == "__main__":

    client = PNCPClient()
    filter_response = client.get_pncp_bids()

    with open("contratacoes_filtradas.json", "w", encoding="utf-8") as file:
        json.dump(filter_response, file, ensure_ascii=False, indent=4)