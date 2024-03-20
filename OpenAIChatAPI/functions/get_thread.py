from OpenAIChatAPI.constants import client
from OpenAIChatAPI.models.chat_models import MessageModel


def get_thread_by_id(thread_id: str) -> list[MessageModel]:
    thread_response = client.beta.threads.messages.list(thread_id=thread_id)

    messages_list = [
        MessageModel(
            Message=message.content[0].text.value if message.content else "",
            CreatedAt=message.created_at,
            UserRole=message.role
        ) for message in thread_response.data if message.content
    ]

    return messages_list
