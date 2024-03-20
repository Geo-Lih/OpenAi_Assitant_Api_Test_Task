from typing_extensions import override
from datetime import datetime
from openai.types.beta.threads import Message
from openai import AssistantEventHandler

from config import ROLE


class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.message = ""
        self.created_at = None
        self.user_role = None

    @override
    def on_text_delta(self, delta, snapshot):
        self.message += delta.value

    @override
    def on_message_created(self, message: Message):
        self.created_at = datetime.utcfromtimestamp(message.created_at)
        self.user_role = message.role


def create_message_payload(message: str, role: str = ROLE) -> dict:
    return {"role": role, "content": message}
