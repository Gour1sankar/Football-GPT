import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(name="football_knowledge")

print(f"Facts in database: {collection.count()}")

query = "Tell me about Mbappe"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print(f"\nQuery: {query}")
for doc in results["documents"][0]:
    print(f"  -> {doc}")