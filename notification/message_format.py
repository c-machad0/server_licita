from datetime import datetime


class Formatter:

    def format_message(self, bid: dict) -> str:
        """
        Formata uma licitação compatível em uma mensagem para envio
        pelo Telegram.

        Args:
            bid: Dados da licitação e sua respectiva similaridade.

        Returns:
            str: Mensagem formatada para o usuário.
        """

        today = datetime.today().strftime("%d/%m/%Y")

        return f"""
        🔔 Nova oportunidade encontrada!

        📅 Data de busca: {today}

        📋 Objeto da Licitação:
        {bid.get('licitacao')}

        📌 Modalidade:
        {bid.get('modalidade')}

        📍 Município:
        {bid.get('municipio')}

        🎯 Similaridade:
        {bid.get('similaridade')}
        """.strip()