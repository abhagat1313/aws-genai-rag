# RAG API — Project README

## Overview

The RAG (Retrieval-Augmented Generation) API is a **document search and question-answering service** built using **AWS Bedrock**, **OpenSearch**, and **Python/FastAPI**. It combines:

- **Embedding & chunking** for storing and indexing documents  
- **Vector search** in OpenSearch  
- **Generative AI** from Bedrock for natural language responses  

The API exposes endpoints for:

1. Uploading documents and indexing embeddings  
2. Querying documents using a RAG workflow  

This project is designed for **enterprise deployment**, including Dockerization and EKS deployment with secure AWS credentials via IRSA.

---

## Project Architecture

Client → FastAPI (RAG API)
│
├─ /add-doc → Chunk & embed document → Store in OpenSearch
│
└─ /ask → Embed query → Search OpenSearch → Generate answer using Bedrock


**Components:**

1. **Chunking & Embeddings**  
   - Documents are split into manageable chunks  
   - Each chunk is embedded into a vector using Titan embeddings (Bedrock)  
   - Embeddings are indexed in OpenSearch for semantic search  

2. **OpenSearch Vector Store**  
   - Stores embeddings with metadata  
   - Supports **k-NN search** to find the most relevant document chunks  
   - Each query searches for top-K relevant chunks  

3. **Bedrock LLM Client**  
   - Generates natural language answers using retrieved document chunks  
   - LLM prompt includes context from OpenSearch search results  

---

## API Endpoints

| Endpoint       | Method | Description |
|----------------|--------|-------------|
| `/add-doc`     | POST   | Upload a document for chunking, embedding, and indexing into OpenSearch |
| `/ask`         | POST   | Send a query; returns RAG answer based on semantic search + LLM generation |

**Example Usage:**

```bash
curl -X POST http://<api-url>/add-doc \
    -F "file=@document.pdf"

curl -X POST http://<api-url>/ask \
    -H "Content-Type: application/json" \
    -d '{"query": "What is the company policy on refunds?"}'
Data Flow (RAG Workflow)

Document ingestion

PDF, text, or other supported formats

Split into chunks (e.g., 500 words per chunk)

Embedding

Each chunk → vector representation using Bedrock embeddings

Indexing

Store embeddings in OpenSearch

Include metadata: document ID, chunk ID, text, timestamp

Query

Query is converted into embedding

k-NN search in OpenSearch returns top matching chunks

LLM Response

Retrieved chunks are sent as context to Bedrock

Bedrock generates a natural language answer

Tech Stack
Layer	Technology
API Framework	FastAPI (Python)
Embeddings	AWS Bedrock Titan Embeddings
Search / Vector DB	OpenSearch
Containerization	Docker
Deployment	AWS EKS, Helm, IRSA
Secrets / Config	AWS Systems Manager / IRSA
Deployment & AWS Integration

Local Development: Python + FastAPI

Docker: Containerized API for reproducible environments

EKS: Deployment using Kubernetes with Helm

IRSA (IAM Roles for Service Accounts):

Pods automatically assume IAM roles

Access Bedrock/OpenSearch securely without AWS keys in environment

Environment Variables

DOTNET_ENVIRONMENT – Environment setting

ApLib_Environment – Application environment

Secrets like DB connection strings, Kafka credentials are stored in AWS SSM or Secrets Manager

Future Enhancements

Support multiple document types (PDF, DOCX, CSV)

Multi-turn conversation support for RAG queries

Error handling, logging, and caching of frequent queries

Horizontal pod autoscaling based on CPU/memory or query volume

Testing

Local:
uvicorn main:app --reload
Docker:
docker build -t rag-api .
docker run -p 8000:8000 rag-api

Kubernetes: Deploy via Helm with ServiceAccount pointing to IAM role (IRSA)

Key Concepts for Enterprise

Chunking & Embeddings → Enable semantic search

Vector Search in OpenSearch → Fast retrieval of relevant chunks

LLM in Bedrock → Generates human-readable answers

IRSA + EKS + Helm → Secure and scalable deployment
