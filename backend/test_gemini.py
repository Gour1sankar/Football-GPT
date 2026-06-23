import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

messages = [
    SystemMessage(content="You are FootballGPT, an expert football assistant. Answer clearly and concisely."),
    HumanMessage(content="Who won the 2006 FIFA World Cup and who scored the winning penalty?")
]

response = llm.invoke(messages)

print(response.content)