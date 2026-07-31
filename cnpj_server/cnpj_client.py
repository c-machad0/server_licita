import requests


class CNPJClient:

    def __init__(self):
        self.__base_url = "https://brasilapi.com.br/api/"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "pncp-client/1.0",
            "Accept": "application/json",
        })

        self.data = None


    def get_cnpj(self, cnpj):
        url = f"{self.__base_url}cnpj/v1/{cnpj}"
        response = self.session.get(url)
        response.raise_for_status()

        self.data = response.json()

        return self.data


    def filter_info(self):
        data_filter = {
            "razao_social": self.data.get("razao_social"),
            "cnpj": self.data.get("cnpj"),
            "cnae_principal": self.data.get("cnae_fiscal_descricao"),
            "cnaes_secundarios": [
                cnae.get("descricao")
                for cnae in self.data.get("cnaes_secundarios", [])
                ]
        }
        return data_filter
    
        # with open("cnae_filtrado.json", "w", encoding="utf-8") as file:
        #     json.dump(data_filter, file, indent=4, ensure_ascii=False)


empresa = CNPJClient()
empresa.get_cnpj('61889727000166')
empresa.filter_info()


# dados = {
#     "razao_social": cnpj_lido.get("razao_social"),
#     "cnpj": cnpj_lido.get("cnpj"),
#     "cnae_principal": cnpj_lido.get("cnae_fiscal_descricao"),
#     "cnaes_secundarios": [
#         cnae.get("descricao")
#         for cnae in cnpj_lido.get("cnaes_secundarios", [])
#     ]
# }

# with open("cnae_filtrado.json", "w", encoding="utf-8") as file:
#     json.dump(dados, file, indent=4, ensure_ascii=False)