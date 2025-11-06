from retrieval import client, INDEX_NAME

def show_chunks(limit=5):
    resp = client.search(
        index=INDEX_NAME,
        body={
            "size": limit,
            "query": {"match_all": {}},
            "_source": ["content", "meta.chunk_id", "meta.total_chunks", "meta.doc_id"]
        }
    )

    print(f"📦 Showing {len(resp['hits']['hits'])} chunks:\n")
    for hit in resp["hits"]["hits"]:
        meta = hit["_source"]["meta"]
        print(f"📄 Doc: {meta.get('doc_id')} | Chunk {meta.get('chunk_id')+1}/{meta.get('total_chunks')}")
        print("Content Preview:", hit["_source"]["content"][:200].replace("\n", " "), "...\n")
        print("-" * 80)

if __name__ == "__main__":
    show_chunks(limit=5)
