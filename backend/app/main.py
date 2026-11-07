
# FastAPI application, which we connect after the RAG pipeline is ready.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.rag_chatbot import chat_with_model


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Portfolio AI Backend is running"
    }





# @app.post("/chat")
# def chat(request: ChatRequest):

#     return StreamingResponse(
#         stream_chat_response(request.message),
#         media_type="text/plain"
#     )

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    return {
        'answer':chat_with_model(request.question)}