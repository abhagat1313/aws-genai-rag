from opensearch_client import create_index, index_text, search_text

index_name = "my-docs"
create_index(index_name)

index_text(index_name, "doc1", "Amazon Bedrock provides foundation models")
index_text(index_name, "doc2", "OpenSearch enables vector similarity search")
index_text(index_name, "doc3", "RAG improves LLM answers using retrieval")

results = search_text(
    index_name,
    "Which AWS service helps with generative AI?",
    k=2
)

print("\n🔍 Search Results:")
for hit in results:
    print(hit["_source"]["text"])
