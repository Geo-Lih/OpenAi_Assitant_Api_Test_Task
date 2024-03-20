from fastapi import APIRouter, HTTPException, status, Depends

from OpenAIChatAPI.functions.get_thread import get_thread_by_id
from OpenAIChatAPI.functions.process_chatbot_engagement import process_chatbot_engagement
from OpenAIChatAPI.logging import logger
from local_databases import postgresql
from OpenAIChatAPI.models.chat_models import ChatInputModel, MessageModel
from sqlalchemy.orm import Session

from db_entities.threads import Thread

router = APIRouter(
    prefix="/chat"
)


@router.post('/chatbot_dialogue_engage', response_model=MessageModel)
def chatbot_dialogue_engage(input_model: ChatInputModel):
    """
    Accepts a message from the user and an optional thread ID, creates a new thread if no ID is provided,
    saves the new thread ID in the database, processes the message through the chatbot (Assistant),
    and returns the chatbot's latest response.
    """
    try:
        return process_chatbot_engagement(input_model.Message, input_model.UserId, input_model.ThreadId)
    except Exception as e:
        logger.exception(f"Error processing chatbot engagement: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'error {e}'
        )


@router.get('/thread', response_model=list[MessageModel])
def get_thread(thread_id: str):
    """
    Retrieves all messages associated with a given thread ID
    and formats them into a list of MessageModels for client-side consumption
    """
    try:
        return get_thread_by_id(thread_id)
    except Exception as e:
        logger.exception(f"Error retrieving thread: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'error {e}'
        )


@router.get('/thread_ids', response_model=list[str])
def get_thread_ids(user_id: int,
                   session: Session = Depends(postgresql.get_db)):
    """
    Fetches a list of thread IDs associated with the given user ID.
    """
    try:
        thread_ids = session.query(Thread.id).filter(Thread.user_id == user_id).all()
        return [thread_id[0] for thread_id in thread_ids]

    except Exception as e:
        logger.exception(f"Error retrieving thread ids: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'error {e}'
        )
    finally:
        session.close()
