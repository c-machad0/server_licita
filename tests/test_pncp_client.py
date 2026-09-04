from app.pncp.client import PNCPClient

def test_configure_date_range():
    assert PNCPClient().start_date.endswith("T08:00:00")
    assert PNCPClient().end_date.endswith("T08:00:00")


def test_format_bids():
    data = {
        "data": [
            {
                "numeroControlePNCP": "123",
                "unidadeOrgao": {
                    "nomeUnidade": "Prefeitura",
                    "municipioNome": "Itajuípe"
                },
                "dataAberturaProposta": "2026-09-01",
                "dataEncerramentoProposta": "2026-09-04",
                "objetoCompra": "Aquisição de computadores",
                "modalidadeNome": "Pregão",
                "linkSistemaOrigem": "https://example.com"
            }
        ]
    }

    result = PNCPClient().format_bids(data)

    assert len(result) == 1
    assert result[0]["objetoCompra"] == "Aquisição de computadores"