# FootballGPT

An AI-powered football intelligence assistant built with RAG, LangGraph agents, and live match data.

## Features

- Ask anything about football — players, clubs, tactics, history
- RAG pipeline over 5500+ curated football facts
- LangGraph agent that routes questions intelligently
- Live match scores and fixtures via RapidAPI
- User memory — remember your favorite club
- FastAPI backend with API key authentication
- Streamlit frontend with stadium UI
- Fully Dockerized

## Tech Stack

| Layer - Technology |
| LLM - Gemini 2.5 Flash |
| Framework - LangChain + LangGraph |
| Vector DB - ChromaDB |
| Embeddings - sentence-transformers/all-MiniLM-L6-v2 |
| Backend - FastAPI |
| Frontend - Streamlit |
| Deployment - Docker |

## Project Structure
ootballgpt/

├── backend/
│   ├── agent.py          # LangGraph agent with router
│   ├── main.py           # FastAPI endpoints
│   ├── rag_engine.py     # RAG pipeline
│   ├── football_api.py   # Live data integration
│   └── load_knowledge.py # ChromaDB loader
├── frontend/
│   └── app.py            # Streamlit UI
├── data/                 # 5500+ football facts
├── vectorstore/          # ChromaDB storage
├── Dockerfile
└── docker-compose.yml

## Setup

1. Clone the repo
2. Create `.env` file:
3. Run with Docker
   docker compose up --build
4. Open `http://localhost:8501`
