# src/titan_embeddings.py

import json
from bedrock_client import bedrock

MODEL_ID = "amazon.titan-embed-text-v2:0"

def get_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for the given text using Titan Embeddings.
    """

    body = {
        "inputText": text
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]
