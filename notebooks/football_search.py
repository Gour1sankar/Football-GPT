from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

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

fact_embeddings = model.encode(football_facts)

def search(query, top_k=3):
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, fact_embeddings)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    print(f"\nQuery: {query}")
    print("Top results:")
    for idx in top_indices:
        print(f"  [{scores[idx]:.4f}] {football_facts[idx]}")

search("Who won the World Cup recently?")
search("Tell me about Guardiola's playing style")
search("fastest footballer")