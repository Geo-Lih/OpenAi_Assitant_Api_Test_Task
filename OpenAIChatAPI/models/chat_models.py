from pydantic import BaseModel
from datetime import datetime


class ChatInputModel(BaseModel):
    Message: str
    ThreadId: str | None


class MessageModel(BaseModel):
    Message: str
    CreatedAt: datetime
    UserRole: str


class MessageWithThreadModel(MessageModel):
    ThreadId: str


class ThreadModel(BaseModel):
    Id: str
    CreatedAt: datetime

    @classmethod
    def from_thread(cls, thread) -> "ThreadModel":
        return cls(Id=thread.id, CreatedAt=thread.created_at)

