from config import client
from OpenAIChatAPI.models.chat_models import MessageModel


def get_thread_by_id(thread_id: str) -> list[MessageModel]:
    thread_response = client.beta.threads.messages.list(thread_id=thread_id)

    return [
        MessageModel(
            Message=message.content[0].text.value,
            CreatedAt=message.created_at,
            UserRole=message.role
        ) for message in thread_response.data if message.content
    ]
