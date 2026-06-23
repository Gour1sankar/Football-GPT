import os
from dotenv import load_dotenv
from typing import TypedDict, Literal
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from football_api import search_player, get_livescores, get_fixtures

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./vectorstore")
collection = chroma_client.get_or_create_collection(name="football_knowledge")

user_memory = {}

class AgentState(TypedDict):
    question: str
    route: str
    context: str
    answer: str
    memory: dict

def router_node(state: AgentState) -> AgentState:
    question = state["question"].lower()
    
    live_keywords = ["today", "tonight", "live","latest", "fixture", "standings","this week"]
    memory_keywords = ["my favorite", "i support", "my club", "remember that",
                       "my team", "i like"]
    
    if any(word in question for word in live_keywords):
        route = "live"
    elif any(word in question for word in memory_keywords):
        route = "memory"
    else:
        route = "rag"
    
    print(f"Router decision: {route}")
    return {**state, "route": route}

def rag_node(state: AgentState) -> AgentState:
    query_embedding = embedding_model.encode([state["question"]]).tolist()
    results = collection.query(
    query_embeddings=query_embedding,
    n_results=5
    )
    facts = results["documents"][0]
    context = "\n".join([f"- {fact}" for fact in facts])
    return {**state, "context": context}

def live_node(state: AgentState) -> AgentState:
    question = state["question"].lower()

    if any(word in question for word in ["score", "live", "playing now"]):
        context = get_livescores()
    elif any(word in question for word in ["fixture", "upcoming", "next match", "schedule"]):
        context = get_fixtures()
    else:
        words = question.split()
        for i, word in enumerate(words):
            if word in ["is", "playing", "about"] and i + 1 < len(words):
                player_name = words[i + 1]
                context = search_player(player_name)
                break
        else:
            context = get_livescores()

    return {**state, "context": context}

def memory_node(state: AgentState) -> AgentState:
    question = state["question"]
    
    if "my favorite" in question.lower() or "i support" in question.lower():
        words = question.lower().split()
        for i, word in enumerate(words):
            if word in ["is", "are"] and i + 1 < len(words):
                user_memory["favorite_club"] = words[i + 1].title()
        context = f"User memory updated. Current memory: {user_memory}"
    else:
        context = f"User memory: {user_memory}"
    
    return {**state, "context": context, "memory": user_memory}

def answer_node(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=f"""You are FootballGPT, an expert football assistant.
Answer the user's question using the context below.
Be concise and accurate.

Context:
{state['context']}
"""),
        HumanMessage(content=state["question"])
    ]
    response = llm.invoke(messages)
    return {**state, "answer": response.content}

def route_decision(state: AgentState) -> Literal["rag_node", "live_node", "memory_node"]:
    return f"{state['route']}_node"

graph = StateGraph(AgentState)

graph.add_node("router_node", router_node)
graph.add_node("rag_node", rag_node)
graph.add_node("live_node", live_node)
graph.add_node("memory_node", memory_node)
graph.add_node("answer_node", answer_node)

graph.set_entry_point("router_node")

graph.add_conditional_edges("router_node", route_decision)

graph.add_edge("rag_node", "answer_node")
graph.add_edge("live_node", "answer_node")
graph.add_edge("memory_node", "answer_node")
graph.add_edge("answer_node", END)

footballgpt = graph.compile()

def ask(question):
    print(f"\nQuestion: {question}")
    result = footballgpt.invoke({
        "question": question,
        "route": "",
        "context": "",
        "answer": "",
        "memory": user_memory
    })
    print(f"Answer: {result['answer']}")
    print("-" * 50)
