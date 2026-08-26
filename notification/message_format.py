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

        activities = "\n".join(
            f"- {activity['atividade']} - "
            f"{activity['similaridade']}%"
            for activity in bid.get("atividades", [])
        )

        return f"""
        🔔 Nova oportunidade encontrada!

        📅 Data de busca: {today}

        📋 Objeto da Licitação:
        {bid.get('licitacao')}

        📌 Modalidade:
        {bid.get('modalidade')}

        📍 Município:
        {bid.get('municipio')}

        🎯 Atividades relacionadas:
        {activities}
        """.strip()