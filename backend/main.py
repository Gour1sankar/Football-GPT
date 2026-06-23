import sys
import os
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import footballgpt, user_memory
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from functools import lru_cache
import hashlib

response_cache = {}

API_KEY = os.getenv("FOOTBALLGPT_API_KEY", "footballgpt-secret-123")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key

app = FastAPI(title="FootballGPT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    route: str

@app.get("/")
def root():
    return {"message": "FootballGPT API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cache/stats")
def cache_stats():
    return {
        "cached_questions": len(response_cache),
        "questions": list(response_cache.keys())[:10]
    }

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest, key: str = Security(verify_api_key)):
    cache_key = hashlib.md5(request.question.lower().strip().encode()).hexdigest()

    if cache_key in response_cache:
        cached = response_cache[cache_key]
        return AnswerResponse(
            question=request.question,
            answer=cached["answer"],
            route=cached["route"]
        )
    try:
        result = footballgpt.invoke({
            "question": request.question,
            "route": "",
            "context": "",
            "answer": "",
            "memory": user_memory
        })
        response_cache[cache_key] = {
            "answer": result["answer"],
            "route": result["route"]
        }
        return AnswerResponse(
            question=request.question,
            answer=result["answer"],
            route=result["route"]
        )
    except Exception as e:
        return AnswerResponse(
            question=request.question,
            answer="Gemini is currently busy. Please try again in a few seconds.",
            route="error"
        )