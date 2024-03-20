import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from AuthAPI import auth_router
from OpenAIChatAPI.routes import chatbot
import logging

app = FastAPI()


app.add_middleware(
    CORSMiddleware)

api_router = APIRouter(prefix="/api/v0")
api_router.include_router(chatbot.router)
api_router.include_router(auth_router.router)
app.include_router(api_router)

# logging
logging.basicConfig(filename='app_exceptions.log', level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8050, log_level="info", reload=True)
