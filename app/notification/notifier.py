import os

from telegram import Bot
from telegram.error import TelegramError

from .formatter import Formatter
from logging_config import get_logger


class Notify:

    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        self.bot = Bot(token=self.telegram_token)

        self.message_formatter = Formatter()

        self.logger = get_logger(__name__)


    async def send_message(self, matches):
        """
        Envia uma mensagem no Telegram para cada licitação compatível. 
        
        Cada licitação é formatada individualmente antes do envio. Caso não 
        existam licitações compatíveis, nenhuma mensagem é enviada. 
        
        Args: 
            matches: Lista de licitações compatíveis com a empresa. 
            
        Raises: 
            TelegramError: Se ocorrer uma falha durante o envio da mensagem para o Telegram.
        """

        try:

            if matches:
                for bid in matches:

                    text_formatted = self.message_formatter.format_message(bid)
                    
                    await self.bot.send_message(
                        chat_id=self.chat_id,
                        text=text_formatted
                    )

                self.logger.info("Mensagens enviadas com sucesso!")
            else:
                self.logger.info("Sem novas mensagens a serem enviadas.")

        except TelegramError:
            self.logger.exception("Falha no envio das mensagens.")
            raise