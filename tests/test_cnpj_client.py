from unittest.mock import Mock

from app.cnpj.client import CNPJClient

def test_get_company_info():

    client = CNPJClient("12345678000199")

    fake_response = Mock()

    fake_response.json.return_value = {
        "razao_social": "CHICO MOEDAS INC.",
        "cnpj": "12345678000199",
        "cnae_fiscal_descricao": "Aplicação de recursos em títulos e valores mobiliários.",
        "cnaes_secundarios": [
            {
                "descricao": "Gestão de recursos e patrimônio financeiro de terceiros"
            }
        ]
    }

    client.session.get = Mock(return_value=fake_response)

    result = client.get_company_info()

    assert result["razao_social"] == "CHICO MOEDAS INC."
    assert result["cnpj"] == "12345678000199"


def test_get_company_info_without_cnae_secundarios():

    client = CNPJClient("12345678000199")

    fake_response = Mock()

    fake_response.json.return_value = {
        "razao_social": "CHICO MOEDAS INC.",
        "cnpj": "12345678000199",
        "cnae_fiscal_descricao": "Aplicação de recursos em títulos e valores mobiliários.",
    }

    client.session.get = Mock(return_value=fake_response)

    result = client.get_company_info()

    assert result["cnaes_secundarios"] == []