from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()

# DB Constants
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# API Constants
API_KEY = os.environ.get('API_KEY')
ASSISTANT_KEY = os.environ.get('ASSISTANT_KEY')
client = OpenAI(api_key=API_KEY)
ROLE = 'user'
