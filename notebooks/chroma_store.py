import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./vectorstore")

collection = client.get_or_create_collection(name="football_knowledge")

football_facts = [
    "Lionel Messi won the 2022 FIFA World Cup with Argentina",
    "Cristiano Ronaldo has scored over 800 career goals",
    "Pep Guardiola is known for tiki-taka and high press tactics",
    "Real Madrid has won the Champions League 15 times",
    "Brazil has won the FIFA World Cup 5 times",
    "Mohamed Salah plays as a forward for Liverpool FC",
    "The Premier League was founded in 1992",
    "Zinedine Zidane scored a famous volley in the 2002 Champions League final",
    "Barcelona's famous tactic is positional play with short passes",
    "Kylian Mbappe is one of the fastest players in world football"
]

embeddings = model.encode(football_facts).tolist()

collection.add(
    documents=football_facts,
    embeddings=embeddings,
    ids=[f"fact_{i}" for i in range(len(football_facts))]
)

print(f"Stored {collection.count()} facts in ChromaDB")

query = "Who won the World Cup recently?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print(f"\nQuery: {query}")
print("Results:")
for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"  [{distance:.4f}] {doc}")