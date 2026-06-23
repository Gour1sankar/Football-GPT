import os
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./vectorstore")

try:
    client.delete_collection("football_knowledge")
    print("Cleared old collection")
except:
    pass

collection = client.get_or_create_collection(name="football_knowledge")

data_dir = "./data"
all_facts = []
sources = []

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(data_dir, filename)
        category = filename.replace(".txt", "")
        with open(filepath, "r") as f:
            lines = list(dict.fromkeys([line.strip() for line in f.readlines() if line.strip()]))
            all_facts.extend(lines)
            sources.extend([category] * len(lines))
            print(f"Loaded {len(lines)} facts from {filename}")

print(f"\nTotal facts: {len(all_facts)}")

batch_size = 500
for i in range(0, len(all_facts), batch_size):
    batch_facts = all_facts[i:i+batch_size]
    batch_sources = sources[i:i+batch_size]
    batch_ids = [f"fact_{i+j}" for j in range(len(batch_facts))]
    batch_embeddings = model.encode(batch_facts).tolist()

    collection.add(
        documents=batch_facts,
        embeddings=batch_embeddings,
        ids=batch_ids,
        metadatas=[{"source": s} for s in batch_sources]
    )
    print(f"Stored batch {i//batch_size + 1} ({len(batch_facts)} facts)")

print(f"\nDone. Total stored: {collection.count()}")