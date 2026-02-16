import json
import os
import threading

from pywebpush import webpush, WebPushException


class WebPushChannel:
    def __init__(self, vapid_private_key, vapid_claims):
        # If it's a file path, read the PEM content
        if os.path.isfile(vapid_private_key):
            with open(vapid_private_key, 'r') as f:
                self.vapid_private_key = f.read()
        else:
            self.vapid_private_key = vapid_private_key
        self.vapid_claims = vapid_claims
        self.subscriptions = []  # list of subscription_info dicts
        self._lock = threading.Lock()

    def add_subscription(self, subscription_info):
        with self._lock:
            # Avoid duplicates by endpoint
            for s in self.subscriptions:
                if s.get('endpoint') == subscription_info.get('endpoint'):
                    return
            self.subscriptions.append(subscription_info)

    def remove_subscription(self, endpoint):
        with self._lock:
            self.subscriptions = [s for s in self.subscriptions
                                  if s.get('endpoint') != endpoint]

    def send(self, title, body, level):
        payload = json.dumps({'title': title, 'body': body, 'level': level})
        expired = []

        with self._lock:
            subs = list(self.subscriptions)

        for sub in subs:
            try:
                webpush(
                    subscription_info=sub,
                    data=payload,
                    vapid_private_key=self.vapid_private_key,
                    vapid_claims=self.vapid_claims,
                )
            except WebPushException as e:
                if hasattr(e, 'response') and e.response is not None:
                    status = e.response.status_code
                    if status in (404, 410):
                        expired.append(sub.get('endpoint'))
                else:
                    print(f"WebPush error: {e}")
            except Exception as e:
                print(f"WebPush error: {e}")

        if expired:
            with self._lock:
                self.subscriptions = [s for s in self.subscriptions
                                      if s.get('endpoint') not in expired]
