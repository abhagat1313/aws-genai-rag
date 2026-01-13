# src/embeddings_test.py

from src.titan_embeddings import get_embedding

vector = get_embedding("OpenSearch is a search engine")

print(len(vector))
print(vector[:5])
