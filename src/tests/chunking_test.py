from src.chunking import chunk_text

text = (
    "AWS Bedrock is a fully managed service that provides access to foundation models. "
    "It allows developers to build generative AI applications without managing infrastructure. "
    "Bedrock integrates with services like OpenSearch to enable Retrieval Augmented Generation. "
    "Chunking is a critical step because embeddings work best on focused, smaller pieces of text."
)

chunks = chunk_text(text, chunk_size=100, overlap=30)

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i} ---")
    print(chunk)
from chunking import chunk_text, create_chunk_objects

text = (
    "AWS Bedrock is a fully managed service that provides access to foundation models. "
    "It allows developers to build generative AI applications without managing infrastructure. "
    "Bedrock integrates with services like OpenSearch to enable Retrieval Augmented Generation. "
    "Chunking is a critical step because embeddings work best on focused, smaller pieces of text."
)

chunks = chunk_text(text, chunk_size=100, overlap=30)
chunk_objects = create_chunk_objects(chunks, source="aws_bedrock_intro")

for obj in chunk_objects:
    print(obj)
