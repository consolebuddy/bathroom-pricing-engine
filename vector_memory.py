import chromadb
import uuid
from sentence_transformers import SentenceTransformer
import os

CHROMA_PATH = os.path.abspath("chroma_store")
print(f"📁 Chroma persistent path: {CHROMA_PATH}")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="pricing_memory")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text):
    return model.encode(text).tolist()


def store_quote(task, context, margin, accepted):
    print(f"📝 Storing quote: task='{task}', context='{context}', margin={margin}, accepted={accepted}")

    vector = embed(task + " " + context)
    doc_id = f"{task}-{context}-{uuid.uuid4()}".replace(" ", "_")

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
    vector = embed(task + " " + context)
    return collection.query(query_embeddings=[vector], n_results=top_k)
