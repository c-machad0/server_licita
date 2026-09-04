from app.notification.formatter import Formatter

def test_format_message():
    bid = {
        "licitacao": "Aquisição de equipamentos",
        "modalidade": "Pregão Eletrônico",
        "municipio": "Itajuípe",
        "unidade": "Prefeitura Municipal",
        "data_abertura": "01/09/2026",
        "data_encerramento": "04/09/2026",
        "link": "https://example.com",
        "atividades": [
            {
                "atividade": "Comércio de equipamentos",
                "similaridade": 87.5
            }
        ]
    }

    message = Formatter.format_message(bid)

    assert "Aquisição de equipamentos" in message
    assert "Pregão Eletrônico" in message
    assert "Itajuípe" in message
    assert "Prefeitura Municipal" in message
    assert "87,5%" in message


def test_format_message_without_activities():
    bid = {
        "licitacao": "Aquisição de materiais"
    }

    message = Formatter().format_message(bid)

    assert "Aquisição de materiais" in message


def test_format_message_without_link():
    bid = {
            "licitacao": "Aquisição de equipamentos",
        }

    message = Formatter.format_message(bid)
    
    assert "Aquisição de equipamentos" in message
    assert "Não informado" in message