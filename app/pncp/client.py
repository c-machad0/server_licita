import time

from datetime import datetime, timedelta
from pprint import pprint

import requests

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from logging_config import get_logger


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

        self.logger = get_logger(__name__)


    def configure_date_range(self) -> None:
        """
        Configura o intervalo de datas utilizado nas consultas ao PNCP.

        Define a data inicial como a data atual e a data final como quatro
        dias após a data atual, ambas formatadas no padrão esperado pelos
        parâmetors da API, utilizando 08:00:00 como horário.
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

        Raises: 
            requests.exceptions.RequestException: Se ocorrer uma falha 
                durante a requisição HTTP. 
            requests.exceptions.JSONDecodeError: Se a resposta não puder 
                ser interpretada como JSON
        """
        try:
            self.logger.info(f"Consultando página %d do PNCP.", page)

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
                self.logger.debug("PNCP | página=%d sem registros | encerrando paginação", page)
                return []
            
            bid_data = response.json()

            self.logger.info(
                "Página %d processada | licitações=%d",
                page,
                len(bid_data)
            )

            return self.format_bids(bid_data)

        except requests.exceptions.JSONDecodeError:
            self.logger.error(
                "Resposta inválida do PNCP | status=%s | content-type=%s | body=%r",
                response.status_code,
                response.headers.get("Content-Type"),
                response.text[:500],
                )
            raise
            
        except requests.exceptions.RequestException:
            self.logger.exception(
                "Falha na requisição HTTP."
            )
            raise


    def bid_pagination(self) -> list[dict]:
        """
        Percorre sequencialmente as páginas de licitações do PNCP.

        A consulta continua enquanto houver registros. Quando a API retorna uma
        página sem conteúdo, a paginação é encerrada.

        Returns:
        list[dict]: Lista contendo todas as licitações encontradas em todas
            as páginas consultadas.
        """

        self.logger.info("Consulta no portal PNCP, iniciada.")
        
        page = 1
        bids = []

        while True:
            response = self.fetch_page(page)

            if not response:
                break

            bids.extend(response)
            page += 1

            time.sleep(2)

        self.logger.info(
            "Fim da paginação | "
            "Última página consultada: %d | "
            "Quantidade de licitações retornadas: %d",
            page,
            len(bids)
            )
        
        return bids


    def format_bids(self, data) -> list[dict]:
        """
        Extrai e organiza os campos relevantes das contratações retornadas
        pela API do PNCP.

        Args:
        data (dict): Resposta JSON retornada pela API do PNCP.

        Returns:
            list[dict]: Lista de licitações contendo identificador PNCP, 
            unidade, município, datas, objeto, modalidade e link.
        """

        return [
            {   "numeroControlePNCP": item.get("numeroControlePNCP"),
                "nomeUnidade": item.get("unidadeOrgao", {}).get("nomeUnidade"),
                "municipioNome": item.get("unidadeOrgao", {}).get("municipioNome"),
                "dataAberturaProposta": datetime.fromisoformat(item.get("dataAberturaProposta")).strftime("%d/%m/%Y %H:%M"),
                "dataEncerramentoProposta": datetime.fromisoformat(item.get("dataEncerramentoProposta")).strftime("%d/%m/%Y %H:%M"),
                "objetoCompra": item.get("objetoCompra"),
                "modalidadeNome": item.get("modalidadeNome"),
                "linkSistemaOrigem": item.get("linkSistemaOrigem"),
            }
            for item in data.get("data", [])
        ]
