

class Formatter:

    def formatter_message(self, data):

            return f"""
            🔔 Nova oportunidade encontrada!

            📋 Licitação:
            {data.get('licitacao')}

            📌 Modalidade:
            {data.get('modalidade')}

            📍 Município:
            {data.get('municipio')}

            🎯 Similaridade:
            {data.get('similaridade')}
            """