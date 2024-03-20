from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordBearer
from openai import OpenAI
from passlib.context import CryptContext

load_dotenv()

# DB config
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# API config
API_KEY = os.environ.get('API_KEY')
ASSISTANT_KEY = os.environ.get('ASSISTANT_KEY')
client = OpenAI(api_key=API_KEY)
ROLE = 'user'

# AUTH config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v0/auth/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b1a9563b93f7099f6f0f4caa6cf63b88e8d3e8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
