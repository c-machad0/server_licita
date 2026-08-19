import os

from dotenv import load_dotenv
from telegram import Bot

from .message_format import Formatter

load_dotenv()


class Notify:

    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        self.bot = Bot(token=self.telegram_token)

        self.message_formatter = Formatter()


    async def send_message(self, matches):
        """
        Envia uma notificação no Telegram para cada licitação compatível.

        Args:
            matches: Lista de licitações compatíveis com a empresa.
        """
        
        for bid in matches:

            text_formatted = self.message_formatter.format_message(bid)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text_formatted
            )