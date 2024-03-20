from config import ASSISTANT_KEY, client
from OpenAIChatAPI.models.chat_models import MessageModel, ChatInputModel, MessageWithThreadModel
from OpenAIChatAPI.utils import EventHandler, create_message_payload
from db_entities.threads import Thread
from sqlalchemy.orm import Session


def process_chatbot_engagement(input_model: ChatInputModel,
                               user_id: int,
                               session: Session) -> MessageModel:

    assistant = client.beta.assistants.retrieve(ASSISTANT_KEY)
    event_handler = EventHandler()

    if input_model.ThreadId:
        client.beta.threads.messages.create(thread_id=input_model.ThreadId,
                                            **create_message_payload(input_model.Message))
    else:
        created_thread = client.beta.threads.create(messages=[create_message_payload(input_model.Message)])
        input_model.ThreadId = created_thread.id

        # insert new thread_id to db
        session.add(Thread(
            id=input_model.ThreadId,
            user_id=user_id
        ))
        session.commit()

    with client.beta.threads.runs.create_and_stream(
            thread_id=input_model.ThreadId,
            assistant_id=assistant.id,
            event_handler=event_handler,
    ) as stream:
        stream.until_done()

    # filling output model
    return MessageWithThreadModel(
        Message=event_handler.message,
        CreatedAt=event_handler.created_at,
        UserRole=event_handler.user_role,
        ThreadId=input_model.ThreadId
    )
