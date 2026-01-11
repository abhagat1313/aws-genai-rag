# src/embeddings_test.py

from titan_embeddings import get_embedding

vector = get_embedding("OpenSearch is a search engine")

print(len(vector))
print(vector[:5])
