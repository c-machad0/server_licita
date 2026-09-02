from matcher.matcher import Matcher

def test_cosine_similarity_identical_vectors():

    result = Matcher.cosine_similarity(
        [1, 0, 0],
        [1, 0, 0]
    )

    assert result == 1.0


def test_cosine_similarity_orthogonal_vectors():

    result = Matcher.cosine_similarity(
        [1, 0],
        [0, 1]
    )

    assert result == 0.0


def test_cosine_similarity_zero_vector():
    result = Matcher.cosine_similarity(
        [0, 0],
        [1, 2]
    )

    assert result == 0.0


def test_find_matching_bids():
    company = {
        "embedding": [
            {
                "atividade": "Comércio de equipamentos",
                "embedding": [1, 0]
            }
        ]
    }

    bids = [
        {
            "objeto": "Compra de equipamentos",
            "modalidade": "Pregão",
            "unidade": "Prefeitura",
            "municipio": "Itajuípe",
            "data_abertura": "2026-09-01",
            "data_encerramento": "2026-09-04",
            "link": "https://example.com",
            "embedding": [1, 0]
        }
    ]

    matcher = Matcher()

    result = matcher.find_matching_bids(company, bids)

    assert len(result) == 1
    assert result[0]["licitacao"] == "Compra de equipamentos"