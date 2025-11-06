import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch
from pdfminer.high_level import extract_text

load_dotenv()

# === OpenSearch Setup ===
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "admin"),   # default creds in Docker OpenSearch
    use_ssl=True,
    verify_certs=False
)

INDEX_NAME = "documents"


def create_index():
    """
    Create index if it doesn't exist.
    """
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(
            index=INDEX_NAME,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "content": {"type": "text"},
                        "meta": {
                            "properties": {
                                "doc_id": {"type": "keyword"},
                                "chunk_id": {"type": "integer"},
                                "total_chunks": {"type": "integer"},
                                "source": {"type": "keyword"}
                            }
                        }
                    }
                }
            }
        )
        print(f"✅ Created index: {INDEX_NAME}")
    else:
        print(f"ℹ️ Index already exists: {INDEX_NAME}")


def extract_pdf_text(pdf_path):
    """
    Extract text from PDF using pdfminer.
    """
    return extract_text(pdf_path)


def chunk_text(text, chunk_size=1000, overlap=150):
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(n, start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = end - overlap  # move with overlap
    return chunks


def index_document(doc_id, content, chunk_id, total_chunks, source):
    """
    Index one chunk with metadata.
    """
    body = {
        "content": content,
        "meta": {
            "doc_id": doc_id,
            "chunk_id": chunk_id,
            "total_chunks": total_chunks,
            "source": source
        }
    }
    client.index(index=INDEX_NAME, id=f"{doc_id}-{chunk_id}", body=body)


if __name__ == "__main__":
    create_index()

    # 👉 Replace with your actual PDF filename
    pdf_path = "data/Aegis.pdf"
    doc_id = "aegis-pdf"

    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
    else:
        # Step 1: Extract
        full_text = extract_pdf_text(pdf_path)

        # Step 2: Chunk
        chunks = chunk_text(full_text, chunk_size=500, overlap=100)
        total_chunks = len(chunks)
        print(f"📄 Splitting {pdf_path} into {total_chunks} chunks...")

        # Step 3: Index each chunk
        for i, chunk in enumerate(chunks):
            index_document(doc_id, chunk, i, total_chunks, pdf_path)

        print(f"✅ Indexed {total_chunks} chunks into {INDEX_NAME}")
