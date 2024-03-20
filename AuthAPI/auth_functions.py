from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends

from AuthAPI.auth_models import UserInDB
from config import pwd_context, SECRET_KEY, ALGORITHM, oauth2_scheme


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    trimmed_hashed_password = hashed_password.strip()
    return pwd_context.verify(plain_password, trimmed_hashed_password)


def create_access_token(user_data: UserInDB) -> str:
    to_encode = user_data.dict()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"expire_at": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_expire_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is expired!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        expire_at = payload.get('expire_at')
        if username is None or expire_at is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    expire_at = datetime.fromisoformat(expire_at)
    if datetime.today() > expire_at:
        raise token_expire_exception

    payload['password'] = payload.pop('hashed_password')
    return UserInDB(**payload)
