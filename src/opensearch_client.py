# opensearch_client.py
from titan_embeddings import get_embedding
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS config from .env
region = os.getenv("AWS_REGION", "us-east-1")
service = "es"  # OpenSearch service
host = os.getenv("OPENSEARCH_ENDPOINT")  # e.g. search-my-domain-xxxxxx.us-east-1.es.amazonaws.com

# Get AWS credentials from environment (or IAM role if running on EKS)
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token)

# OpenSearch client
client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=30
)

# ------------------------
# Functions
# ------------------------
def create_index(index_name: str):
    """Create an index with shard/replica and k-NN vector mapping"""
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name, ignore=[400, 404])
        print(f"Deleted old index '{index_name}'.")

    body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1,
            "index": {
                "knn": True
            }
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "embedding": {"type": "knn_vector", "dimension": 1024},
                "metadata": {"type": "object"}
            }
        }
    }

    client.indices.create(index=index_name, body=body)
    print(f"Index '{index_name}' created with k-NN enabled.")



def index_document(index_name: str, doc_id: str, text: str, embedding, metadata={}):
    """Index a single document with its embedding and metadata"""
    doc = {
        "text": text,
        "embedding": embedding,
        "metadata": metadata
    }
    client.index(index=index_name, id=doc_id, body=doc)
    print(f"Document '{doc_id}' indexed in '{index_name}'.")

def index_text(index_name: str, doc_id: str, text: str, metadata: dict = None):
    """
    Generate embedding for text and index into OpenSearch
    """
    embedding = get_embedding(text)

    index_document(
        index_name=index_name,
        doc_id=doc_id,
        text=text,
        embedding=embedding,
        metadata=metadata or {}
    )


def search_vector(index_name: str, query_vector, k=3):
    """Perform k-NN search on embeddings"""
    body = {
        "size": k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": k
                }
            }
        }
    }
    response = client.search(index=index_name, body=body)
    return response["hits"]["hits"]

def search_text(index_name: str, query: str, k: int = 3):
    """
    Semantic search using text query
    """
    query_vector = get_embedding(query)
    return search_vector(
        index_name=index_name,
        query_vector=query_vector,
        k=k
    )

