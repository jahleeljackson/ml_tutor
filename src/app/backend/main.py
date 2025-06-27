from fastapi import FastAPI
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from postgres_api.database import engine
from postgres_api import models
from routers import context
from chatbot.chatbot import Chatbot 
from pipeline import main

scheduler = BackgroundScheduler()

#defining cron job to run for duration of app's "lifespan"
@asynccontextmanager 
async def lifespan(app: FastAPI):
    scheduler.add_job(main,  'cron', day_of_week='mon', hour=3, minute=0)
    scheduler.start()
    print("Web scraping pipeline scheduled to run every Friday at midnight.")
    yield 
    scheduler.shutdown(wait=False)


# Initialize the chatbot, FastAPI app, and APScheduler
# scheduler = BackgroundScheduler()
mistral_bot = Chatbot()
deepseek_bot = Chatbot(model="deepseek-r1")
app = FastAPI(lifespan=lifespan)

models.Base.metadata.create_all(bind=engine)
app.include_router(context.router)


class PromptRequest(BaseModel):
    prompt: str

@app.get('/')
def read_root():
    return {"message": "Welcome to the Machine Learning Tutor API!"}

# Define the endpoint for generating casual responses
@app.post('/generate-response')
def generate_response(request: PromptRequest):
    response = mistral_bot.invoke(request.prompt)
    return {"response": response}

# Define the endpoint for generating complex responses using the deepseek-r1 model
@app.post('/generate-complex-response')
def generate_complex_response(request: PromptRequest):
    response = deepseek_bot.invoke(request.prompt)
    # Remove the initial "<think>" tag from the response
    substring = "</think>"
    response = response[response.find(substring) + len(substring):]
    return {"response": response}


