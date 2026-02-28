import requests


LEVEL_COLORS = {
    'critical': '#dc3545',
    'warning': '#ffc107',
    'info': '#28a745',
}


class SlackChannel:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, title, body, level):
        color = LEVEL_COLORS.get(level, '#6c757d')
        requests.post(self.webhook_url, json={
            'attachments': [{
                'color': color,
                'title': title,
                'text': body,
            }]
        }, timeout=10)
