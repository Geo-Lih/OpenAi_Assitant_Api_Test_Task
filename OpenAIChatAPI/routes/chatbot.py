from fastapi import APIRouter, HTTPException, status, Depends

from AuthAPI.auth_functions import get_current_user
from AuthAPI.auth_models import UserInDB
from OpenAIChatAPI.functions.get_thread import get_thread_by_id
from OpenAIChatAPI.functions.process_chatbot_engagement import process_chatbot_engagement
from OpenAIChatAPI.logging import logger
from local_databases import postgresql
from OpenAIChatAPI.models.chat_models import ChatInputModel, MessageModel, MessageWithThreadModel, ThreadModel
from sqlalchemy.orm import Session

from db_entities.threads import Thread

router = APIRouter(
    prefix="/chat",
    dependencies=[Depends(get_current_user)]
)


@router.post('/chatbot_dialogue_engage', response_model=MessageWithThreadModel)
def chatbot_dialogue_engage(input_model: ChatInputModel,
                            user: UserInDB = Depends(get_current_user),
                            session: Session = Depends(postgresql.get_db)):
    """
    Accepts a message from the user and an optional thread ID, creates a new thread if no ID is provided,
    saves the new thread ID in the database, processes the message through the chatbot (Assistant),
    and returns the chatbot's latest response.
    """
    try:
        return process_chatbot_engagement(input_model, user.id, session)
    except Exception as e:
        logger.exception(f"Error processing chatbot engagement: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'error {e}'
        )


@router.get('/thread', response_model=list[MessageModel])
def get_thread(thread_id: str,
               user: UserInDB = Depends(get_current_user),
               session: Session = Depends(postgresql.get_db)):
    """
    Retrieves all messages associated with a given thread ID
    and formats them into a list of MessageModels for client-side consumption
    """
    try:
        # Verify if the user has access to the specified thread
        thread_access = session.query(Thread).filter(Thread.id == thread_id, Thread.user_id == user.id).first()
        if not thread_access:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thread not found or access denied."
            )
        return get_thread_by_id(thread_id)
    except Exception as e:
        logger.exception(f"Error retrieving thread: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'error {e}'
        )


@router.get('/thread_ids', response_model=list[ThreadModel])
def get_thread_ids(user: UserInDB = Depends(get_current_user),
                   session: Session = Depends(postgresql.get_db)):
    """
    Fetches a list of thread IDs associated with the given user ID.
    """
    try:
        threads = session.query(Thread).filter(Thread.user_id == user.id).all()
        return [ThreadModel.from_thread(thread) for thread in threads]

    except Exception as e:
        logger.exception(f"Error retrieving thread ids: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'error {e}'
        )
