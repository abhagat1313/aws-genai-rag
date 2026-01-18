# src/titan_embeddings.py
import boto3
import json
import os

MODEL_ID = "amazon.titan-embed-text-v2:0"
region = os.getenv("AWS_REGION", "us-east-1")
def get_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for the given text using Titan Embeddings.
    """

    bedrock = boto3.client("bedrock-runtime", region_name=region)

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "inputText": text
        })
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]

def embed_chunk_objects(chunk_objects: list) -> list:
    """
    Attaches embeddings to each chunk object.

    :param chunk_objects: List of chunk dictionaries (with text)
    :return: Same list with embeddings added
    """

    for chunk in chunk_objects:
        embedding = get_embedding(chunk["text"])
        chunk["embedding"] = embedding

    return chunk_objects

