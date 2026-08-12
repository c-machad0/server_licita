import os

from .message_format import Formatter

from matcher.matcher import Matcher

from telegram import Bot


class Notify:

    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

        self.bot = Bot(token=self.token)

        self.message_formatter = Formatter()
        matcher = Matcher()
        self.matcher = matcher.match_company_bid(threshold=0.50)


    async def send_message(self):
        text_formatted = self.message_formatter.formatter_message(self.matcher)
        
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text_formatted
        )