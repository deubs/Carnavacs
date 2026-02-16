import threading
import time
from datetime import datetime, timedelta


# Event level mapping
EVENT_LEVELS = {
    'device_offline': 'critical',
    'device_online': 'info',
    'server_offline': 'critical',
    'server_online': 'info',
    'scanner_disconnected': 'warning',
    'scanner_reconnected': 'info',
}

# Emoji per level for message formatting
LEVEL_EMOJI = {
    'critical': '\U0001F534',  # red circle
    'warning': '\U0001F7E0',   # orange circle
    'info': '\U0001F7E2',      # green circle
}

# Human-readable event labels
EVENT_LABELS = {
    'device_offline': 'Device Offline',
    'device_online': 'Device Online',
    'server_offline': 'Server Offline',
    'server_online': 'Server Online',
    'scanner_disconnected': 'Scanner Disconnected',
    'scanner_reconnected': 'Scanner Reconnected',
}

DEBOUNCE_SECONDS = 300  # 5 minutes
FLUSH_INTERVAL = 5      # seconds


class NotificationDispatcher:
    def __init__(self, channels):
        self.channels = channels
        self._queue = []              # list of (event_type, target_name, timestamp)
        self._lock = threading.Lock()
        self._debounce = {}           # (event_type, target_name) -> last_sent datetime

        if self.channels:
            t = threading.Thread(target=self._flush_loop, daemon=True,
                                 name="NotificationDispatcher")
            t.start()

    def queue_event(self, event_type, target_name):
        if not self.channels:
            return

        now = datetime.now()
        key = (event_type, target_name)

        with self._lock:
            last_sent = self._debounce.get(key)
            if last_sent and (now - last_sent) < timedelta(seconds=DEBOUNCE_SECONDS):
                return
            self._queue.append((event_type, target_name, now))

    def _flush_loop(self):
        while True:
            time.sleep(FLUSH_INTERVAL)
            self._flush()

    def _flush(self):
        with self._lock:
            if not self._queue:
                return
            batch = list(self._queue)
            self._queue.clear()

        # Group events by type
        groups = {}
        for event_type, target_name, ts in batch:
            groups.setdefault(event_type, []).append(target_name)

        now = datetime.now()
        for event_type, targets in groups.items():
            # Update debounce for each target
            with self._lock:
                for t in targets:
                    self._debounce[(event_type, t)] = now

            title, body, level = self._format_message(event_type, targets)
            for channel in self.channels:
                try:
                    channel.send(title, body, level)
                except Exception as e:
                    print(f"Notification channel {channel.__class__.__name__} error: {e}")

    @staticmethod
    def _format_message(event_type, targets):
        level = EVENT_LEVELS.get(event_type, 'info')
        emoji = LEVEL_EMOJI.get(level, '')
        label = EVENT_LABELS.get(event_type, event_type)

        if len(targets) == 1:
            title = f"{emoji} {label}"
            body = targets[0]
        else:
            title = f"{emoji} {len(targets)} {label}"
            body = ', '.join(targets)

        return title, body, level
