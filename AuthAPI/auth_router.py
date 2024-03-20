from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db_entities.users import User
from local_databases import postgresql
from .auth_models import UserCreate, SignUpModel, TokenModel, UserInDB
from .auth_functions import get_password_hash, verify_password, create_access_token

router = APIRouter(
    prefix="/auth"
)


@router.post("/sign_up", response_model=SignUpModel)
def sign_up(user: UserCreate,
            session: Session = Depends(postgresql.get_db)):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    session.add(User(
        username=user.username,
        password=hashed_password
    ))
    session.commit()
    return SignUpModel(message=f"User {user.username} was signed up successfully!")


@router.post("/login", response_model=TokenModel)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               session: Session = Depends(postgresql.get_db)):
    db_user = session.query(User).filter(User.username == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = UserInDB.from_orm(db_user)
    if not verify_password(form_data.password, user_data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(user_data)
    return TokenModel(access_token=access_token, token_type="bearer")
