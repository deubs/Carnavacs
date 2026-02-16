import requests


class TelegramChannel:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self._url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, title, body, level):
        text = f"*{title}*\n{body}"
        requests.post(self._url, json={
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'Markdown',
        }, timeout=10)
