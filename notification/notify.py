import os

from .message_format import Formatter

from telegram import Bot

from dotenv import load_dotenv

load_dotenv()


class Notify:

    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        self.bot = Bot(token=self.token)

        self.message_formatter = Formatter()


    async def send_message(self, matcher):
        for bid in matcher:

            text_formatted = self.message_formatter.formatter_message(bid)
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text_formatted
            )