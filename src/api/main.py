from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import BaseModel
from src.chunking import chunk_text, create_chunk_objects
from src.titan_embeddings import embed_chunk_objects
from src.opensearch_client import create_index, index_chunk_objects, search_vector


class DocumentRequest(BaseModel):
    text: str
    source: str

class QueryRequest(BaseModel):
    query: str
    k: int = 3  # number of top chunks to return


app = FastAPI(
    title="AWS GenAI RAG API",
    description="API to ingest and search documents using Bedrock + OpenSearch",
    version="0.1.0"
)



@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/add-document")
def add_document(doc: DocumentRequest):
    # 1. Chunk
    chunks = chunk_text(doc.text, chunk_size=100, overlap=30)
    chunk_objects = create_chunk_objects(chunks, source=doc.source)

    # 2. Embed
    embedded_chunks = embed_chunk_objects(chunk_objects)

    # 3. Index
    index_name = "rag-docs"
    create_index(index_name)
    index_chunk_objects(index_name, embedded_chunks)

    return {
        "message": "Document indexed successfully",
        "chunks_indexed": len(embedded_chunks)
    }

@app.post("/ask")
def ask_rag(query_req: QueryRequest):
    # 1️⃣ Embed the query
    query_vector = embed_chunk_objects([{"text": query_req.query}])[0]["embedding"]

    # 2️⃣ Search OpenSearch
    index_name = "rag-docs"
    results = search_vector(index_name, query_vector, k=query_req.k)

    # 3️⃣ Format results
    response = []
    for hit in results:
        source = hit["_source"]
        response.append({
            "text": source["text"],
            "source": source.get("metadata", {}).get("source"),
            "score": hit["_score"]
        })

    # 4️⃣ Return results
    return {
        "query": query_req.query,
        "results": response
    }
