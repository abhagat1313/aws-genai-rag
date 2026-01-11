import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

region = os.getenv("AWS_REGION", "us-east-1")

bedrock = boto3.client("bedrock-runtime", region_name=region)

model_id = "amazon.titan-text-express-v1"

# **Correct body for Titan Text Express**
body = {
    "inputText": "Explain RAG (Retrieval-Augmented Generation) in one sentence."
}

# response = bedrock.invoke_model(
#     modelId=model_id,
#     body=json.dumps(body),   # must be a JSON string
#     contentType="application/json",
#     accept="application/json"
# )

# # Decode the response
# result = json.loads(response["body"].read())
# print("Response structure:", result)

# # Titan Express returns 'results' key with a list
# if "results" in result:
#     print(result["results"][0]["outputText"])
