import chromadb
from sentence_transformers import SentenceTransformer

# Initialize Chroma client and collection
client = chromadb.Client()
collection = client.get_or_create_collection(name="pricing_memory")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return model.encode(text).tolist()

def store_quote(task, context, margin, accepted):
    """
    Stores a quote in vector memory.
    - task: str (e.g., "install vanity")
    - context: str (e.g., "Marseille, small bathroom")
    - margin: float
    - accepted: bool
    """
    vector = embed(task + " " + context)
    doc_id = f"{task}-{context}".replace(" ", "_")
    collection.add(
        documents=[task],
        metadatas=[{
            "context": context,
            "margin": margin,
            "accepted": accepted
        }],
        embeddings=[vector],
        ids=[doc_id]
    )

def search_similar(task, context, top_k=3):
    """
    Returns top_k similar past tasks based on vector similarity.
    """
    vector = embed(task + " " + context)
    results = collection.query(query_embeddings=[vector], n_results=top_k)
    return results
