import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch

load_dotenv()

# === OpenSearch Client ===
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "admin"),
    use_ssl=True,
    verify_certs=False
)

INDEX_NAME = "documents"


def search_documents(query, size=3):
    """
    Search chunks in OpenSearch with highlights.
    Returns top matching chunks with metadata.
    """
    response = client.search(
        index=INDEX_NAME,
        body={
            "size": size,
            "_source": ["content", "meta.chunk_id", "meta.total_chunks", "meta.doc_id", "meta.source"],
            "query": {"match": {"content": query}},
            "highlight": {
                "fields": {
                    "content": {"fragment_size": 150, "number_of_fragments": 2}
                }
            }
        }
    )
    return response["hits"]["hits"]


# Debug run
if __name__ == "__main__":
    query = "data science"
    results = search_documents(query, size=3)

    print(f"\n🔎 Query: {query}")
    print(f"Found {len(results)} matching chunks:\n")

    for r in results:
        meta = r["_source"].get("meta", {})
        chunk_id = meta.get("chunk_id")
        total_chunks = meta.get("total_chunks")
        doc_id = meta.get("doc_id")
        score = r["_score"]

        print(f"📄 Doc: {doc_id} | Chunk {chunk_id+1}/{total_chunks} | Score: {score:.2f}")
        if "highlight" in r:
            print("✨ Highlight:", " ... ".join(r["highlight"]["content"]))
        else:
            print("Preview:", r["_source"]["content"][:200])
        print("-" * 80)
