from collections import deque

class TranscriptionHistory:
    def __init__(self, max_items=5):
        self.history = deque(maxlen=max_items)

    def add(self, text):
        self.history.append(text)

    def get_recent(self):
        return list(reversed(self.history))

    def get_preview(self, text, max_length=30):
        """Returns truncated preview of text for menu display"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..." 