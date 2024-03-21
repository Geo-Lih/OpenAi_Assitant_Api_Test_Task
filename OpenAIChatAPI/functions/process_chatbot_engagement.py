import time

from OpenAIChatAPI.constants import RUN_STATUSES_TO_CHECK, RUN_STATUS_COMPLETED
from config import ASSISTANT_KEY, client
from OpenAIChatAPI.models.chat_models import ChatInputModel, MessageWithThreadModel
from OpenAIChatAPI.utils import create_message_payload
from db_entities.threads import Thread
from sqlalchemy.orm import Session


def process_chatbot_engagement(input_model: ChatInputModel,
                               user_id: int,
                               session: Session) -> list[MessageWithThreadModel]:

    assistant = client.beta.assistants.retrieve(ASSISTANT_KEY)
    if not input_model.ThreadId:
        input_model.ThreadId = client.beta.threads.create().id

        # insert new thread_id to db
        session.add(Thread(
            id=input_model.ThreadId,
            user_id=user_id
        ))
        session.commit()

    # current user's message
    message = client.beta.threads.messages.create(thread_id=input_model.ThreadId,
                                                  **create_message_payload(input_model.Message))

    run = client.beta.threads.runs.create(
        thread_id=input_model.ThreadId,
        assistant_id=assistant.id
    )

    while run.status in RUN_STATUSES_TO_CHECK:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=input_model.ThreadId,
            run_id=run.id
        )
    if run.status == RUN_STATUS_COMPLETED:
        assistant_response = client.beta.threads.messages.list(
            thread_id=input_model.ThreadId,
            before=message.id
            # limit=1, but the assistant's response can contain multiple messages (a long response that was split)
        )

    return [
        MessageWithThreadModel(
            Message=message.content[0].text.value,
            CreatedAt=message.created_at,
            UserRole=message.role,
            ThreadId=message.thread_id,
        ) for message in assistant_response.data if message.content
    ]
