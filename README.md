# 🗣️ Aegis Chatbot

A chatbot application powered by AI and retrieval-augmented generation (RAG) that enables interactive and context-aware conversations using your custom data. Built for speed, relevance and local deployment.

---

## 🚀 Features

- Natural language conversation with a knowledge-base (your documents / web data)  
- Local LLM / cloud LLM support (e.g., Llama, Qwen, etc.)  
- Vector store for retrieval (e.g., Qdrant)  
- Simple front-end (e.g., Streamlit interface or web UI)  
- Fast response, minimal latency, designed for deployment  

---

## 🧰 Tech Stack

| Component           | Technology / Library                          |
|----------------------|----------------------------------------------|
| Front-end            | Streamlit                   |
| Backend / Server     | FastAPI / Python                      |
| LLM                  | Local model (e.g. Qwen2-4B) or cloud LLM     |
| Vector storage       | Qdrant                                       |
| Embeddings           | SentenceTransformers (e.g., `all-MiniLM-L12-v2`) |
| RAG Pipeline         | Embeddings → Vector Search → LLM Answering   |

