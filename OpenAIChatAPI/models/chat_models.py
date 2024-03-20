from pydantic import BaseModel
from datetime import datetime


class BaseModelORM(BaseModel):
    class Config:
        orm_mode = True


class ChatInputModel(BaseModel):
    Message: str
    UserId: int
    ThreadId: str | None


class MessageModel(BaseModel):
    Message: str
    CreatedAt: datetime
    UserRole: str
