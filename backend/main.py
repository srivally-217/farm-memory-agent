from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from hindsight_service import generate_farm_response, store_farm_event

load_dotenv()

app = FastAPI(title="Farm Memory Agent")


# Allow frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FarmerMessage(BaseModel):
    message: str


class FarmEvent(BaseModel):
    event: str


@app.get("/")
def home():
    return {
        "message": "Farm Memory Agent is running!"
    }


@app.get("/config-test")
def config_test():
    return {
        "hindsight_key_loaded": bool(os.getenv("HINDSIGHT_API_KEY")),
        "hindsight_url": os.getenv("HINDSIGHT_BASE_URL"),
        "groq_key_loaded": bool(os.getenv("GROQ_API_KEY"))
    }


@app.post("/farm-response")
def farm_response(data: FarmerMessage):

    response = generate_farm_response(data.message)

    return {
        "response": response
    }


@app.post("/farm-event")
def farm_event(data: FarmEvent):

    store_farm_event(data.event)

    return {
        "message": "Farm event stored successfully!"
    }