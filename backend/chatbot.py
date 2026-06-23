import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

conversation_history = [
    SystemMessage(content="You are FootballGPT, an expert football assistant. Be concise and accurate.")
]

print("FootballGPT (type 'quit' to exit)\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        break
    
    conversation_history.append(HumanMessage(content=user_input))
    response = llm.invoke(conversation_history)
    conversation_history.append(AIMessage(content=response.content))
    
    print(f"FootballGPT: {response.content}\n")