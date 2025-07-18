# View ChromaDB contents
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("restaurant_docs")

print(f"Total chunks: {collection.count()}")
print("\nFirst few chunks:")
results = collection.get(limit=5)
for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
    print(f"\n{i+1}. Source: {metadata['source']}")
    print(f"Text: {doc[:100]}...")