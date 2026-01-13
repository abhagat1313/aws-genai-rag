from src.chunking import chunk_text, create_chunk_objects
from src.titan_embeddings import embed_chunk_objects

text = (
    "AWS Bedrock is a fully managed service that provides access to foundation models. "
    "It allows developers to build generative AI applications without managing infrastructure."
)

chunks = chunk_text(text, chunk_size=100, overlap=20)
chunk_objects = create_chunk_objects(chunks, source="aws_bedrock_intro")

embedded_chunks = embed_chunk_objects(chunk_objects)

for chunk in embedded_chunks:
    print("\nChunk ID:", chunk["chunk_id"])
    print("Embedding length:", len(chunk["embedding"]))
    print("First 3 values:", chunk["embedding"][:3])
