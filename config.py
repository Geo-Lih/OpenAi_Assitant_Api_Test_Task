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
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
