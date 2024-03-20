from fastapi import HTTPException, status

from OpenAIChatAPI.constants import ASSISTANT_KEY, client
from OpenAIChatAPI.logging import logger
from OpenAIChatAPI.models.chat_models import MessageModel
from OpenAIChatAPI.utils import EventHandler, create_message_payload
from db_entities.threads import Thread
from sqlalchemy.orm import Session

from local_databases import postgresql


@postgresql.connected_to_db
def process_chatbot_engagement(message: str,
                               user_id: int,
                               thread_id: str,
                               session: Session) -> MessageModel:

    assistant = client.beta.assistants.retrieve(ASSISTANT_KEY)
    event_handler = EventHandler()

    if thread_id:
        client.beta.threads.messages.create(thread_id=thread_id, **create_message_payload(message))
    else:
        created_thread = client.beta.threads.create(messages=[create_message_payload(message)])
        thread_id = created_thread.id

        # insert new thread_id to db
        try:
            session.add(Thread(
                id=thread_id,
                user_id=user_id
            ))
            session.commit()
        except Exception as e:
            logger.exception(f"Failed to process database insert: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'data base insert error: {e}'
            )

    with client.beta.threads.runs.create_and_stream(
            thread_id=thread_id,
            assistant_id=assistant.id,
            event_handler=event_handler,
    ) as stream:
        stream.until_done()

    # filling output model
    chat_response = MessageModel(
        Message=event_handler.message,
        CreatedAt=event_handler.created_at,
        UserRole=event_handler.user_role
    )

    return chat_response

