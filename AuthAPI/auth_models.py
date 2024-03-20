from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    password: str

    class Config:
        orm_mode = True

    def dict(self, *args, **kwargs):
        return {
            'id': self.id,
            'username': self.username,
            'hashed_password': self.password,
        }


class SignUpModel(BaseModel):
    message: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str
