from sentence_transformers import SentenceTransformer
from vector_memory import search_similar
import chromadb
import os

CHROMA_PATH = os.path.abspath("../chroma_store")  # go one level up
print("📁 Chroma persistent path:", CHROMA_PATH)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name="pricing_memory")


print("🔍 Stored Quotes Count:", collection.count())

# Search using query_texts
results = collection.query(
    query_texts=["install vanity marseille"],
    n_results=3
)

print("\n🔎 Vector Search using raw text:")
for i, doc in enumerate(results.get("documents", [[]])[0]):
    print(f"Result {i+1}: {doc}")
    print("Metadata:", results["metadatas"][0][i])

# Use the helper function to search semantically
print("\n🔎 Vector Search using search_similar():")
similar = search_similar("replace toilet", "marseille, small bathroom")
for i, doc in enumerate(similar.get("documents", [[]])[0]):
    print(f"Similar {i+1}: {doc}")
    print("Metadata:", similar["metadatas"][0][i])

# Confirm model is working
model = SentenceTransformer("all-MiniLM-L6-v2")
vec = model.encode("install vanity marseille small bathroom")
print("\n✅ Embedding dimension length:", len(vec))  # Should be 384
