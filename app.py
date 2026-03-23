from fastapi import FastAPI
from pydantic import BaseModel
from model import chatbot
app=FastAPI()
class Message(BaseModel):
    message:str
@app.get("/")
def home():
    return{"message" : "API is running"}
@app.post("/chat")
def chat(data:Message):
    reply=chatbot(data.message)
    return{"reply" : reply}

