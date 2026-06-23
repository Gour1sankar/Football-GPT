from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "Cristiano is the greatest footballer of all time",
    "Lionel is the best player ever",
    "Ronaldo scored 50 goals in a season",
    "Cricket is a popular sport in India",
    "Pep Guardiola uses tiki taka tactic",
    "Manchester City plays attacking football"
]

embeddings = model.encode(sentences)

print(f"Number of sentences: {len(sentences)}")
print(f"Embedding shape: {embeddings.shape}")
print(f"First embedding (first 5 numbers): {embeddings[0][:5]}")

from sklearn.metrics.pairwise import cosine_similarity

pairs = [
    (0, 1),   
    (0, 3),  
    (4, 5),  
    (0, 3),  
]

print("\nSimilarity scores:")
for i, j in pairs:
    score = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
    print(f"  '{sentences[i][:40]}' vs '{sentences[j][:40]}' -> {score:.4f}")