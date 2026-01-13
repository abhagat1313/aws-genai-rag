from src.chunking import chunk_text, create_chunk_objects
from src.titan_embeddings import embed_chunk_objects, get_embedding
from src.opensearch_client import create_index, index_chunk_objects, search_text

# ----------------------------
# 1. Prepare Document
# ----------------------------
text = (
    "AWS Bedrock is a fully managed service that provides access to foundation models. "
    "It allows developers to build generative AI applications without managing infrastructure. "
    "Bedrock integrates with services like OpenSearch to enable Retrieval Augmented Generation. "
    "Chunking is a critical step because embeddings work best on focused, smaller pieces of text."
)

# ----------------------------
# 2. Chunk Document
# ----------------------------
chunks = chunk_text(text, chunk_size=100, overlap=30)
chunk_objects = create_chunk_objects(chunks, source="aws_bedrock_intro")
print(f"{len(chunk_objects)} chunk objects created.")

# ----------------------------
# 3. Embed Chunks
# ----------------------------
embedded_chunks = embed_chunk_objects(chunk_objects)
print(f"Chunks embedded. First embedding length: {len(embedded_chunks[0]['embedding'])}")

# ----------------------------
# 4. Create Index
# ----------------------------
index_name = "rag-docs"
create_index(index_name)

# ----------------------------
# 5. Index Chunks
# ----------------------------
index_chunk_objects(index_name, embedded_chunks)
print("All chunks indexed into OpenSearch.")

# ----------------------------
# 6. Test Semantic Search
# ----------------------------
query = "What is AWS Bedrock?"
results = search_text(index_name, query, k=2)

print("\nSearch results:")
for hit in results:
    source = hit["_source"]
    print(f"Chunk ID: {source.get('metadata', {}).get('source')} | Score: {hit['_score']}")
    print(f"Text: {source['text']}\n")
