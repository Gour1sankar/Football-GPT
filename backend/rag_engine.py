import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(name="football_knowledge")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def ask_footballgpt(question):
    query_embedding = model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    retrieved_facts = results["documents"][0]
    context = "\n".join([f"- {fact}" for fact in retrieved_facts])

    messages = [
        SystemMessage(content=f"""You are FootballGPT, an expert football assistant.
Answer the user's question using ONLY the facts provided below.
If the facts do not contain enough information, say so honestly.

Facts:
{context}
"""),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    
    print(f"\nQuestion: {question}")
    print(f"\nRetrieved facts:")
    for fact in retrieved_facts:
        print(f"  -> {fact}")
    print(f"\nAnswer: {response.content}")

ask_footballgpt("Who is the greatest manager of all time?")
ask_footballgpt("Explain the offside rule")
ask_footballgpt("Which country has won the most World Cups?")