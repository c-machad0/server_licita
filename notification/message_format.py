# import json
# from pprint import pprint

# path = 'C:\\Users\\Christian\\Desktop\\Python\\Projetos\\server_licita\\match.json'

# with open(path, 'r', encoding='utf-8') as file:
#     file_read = json.load(file)

class Formatter:

    def __init__(self):
        pass


    def formatter_message(self, data):
        for licitacoes in data:

            text = f"""
            🔔 Nova oportunidade encontrada!

            🏢 Empresa:
            {licitacoes.get('empresa')}

            📋 Licitação:
            {licitacoes.get('licitacao')}

            📌 Modalidade:
            {licitacoes.get('modalidade')}

            📍 Município:
            {licitacoes.get('municipio')}

            🎯 Similaridade:
            {licitacoes.get('similaridade')}
            """

        return text