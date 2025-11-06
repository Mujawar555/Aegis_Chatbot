import json
import requests
from langchain.prompts import PromptTemplate
from retrieval import search_documents  # Import the base function directly

# --- RAG Prompt Template ---
RAG_PROMPT_TEMPLATE = """
You are an AI assistant that answers questions using only the retrieved documents.
If the retrieved documents don't contain relevant information, say:
"I'm not sure about that based on the available information."

### Instructions:
- Use only the provided context (retrieved docs).
- Keep answers clear, polite, concise and short.
- Do not invent information outside the context. 
- When useful, structure your response with bullet points or short lists.   

RETRIEVED DOCUMENTS:
{context}

USER QUESTION:
{question}

YOUR ANSWER:
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=RAG_PROMPT_TEMPLATE,
)

# --- Ollama Generation (local Deepseek model) ---
def generate_with_ollama(prompt_text, model_name="deepseek-r1:1.5b", stream=False):
    """Generate response using Ollama with Deepseek model"""
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": model_name,
            "prompt": prompt_text,
            "stream": stream,
            "options": {"temperature": 0.7},
        }

        if stream:
            response = requests.post(url, json=data, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        if "response" in chunk:
                            yield chunk["response"]
                    except json.JSONDecodeError:
                        continue
        else:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json().get("response", "No response generated")

    except Exception as e:
        error_msg = f"Error generating response with Ollama: {str(e)}"
        if stream:
            yield error_msg
        else:
            return error_msg

# --- RAG Pipeline ---
def generate_rag_response(query, top_k=5, stream=False):
    """
    Generate RAG response using retrieved chunks + Ollama.
    """
    try:
        # Step 1: Retrieve relevant chunks
        results = search_documents(query, size=top_k)

        if not results:
            message = "No relevant information found in the documents."
            if stream:
                yield message
                return
            else:
                return message

        # Step 2: Format retrieved contexts
        contexts = []
        for i, hit in enumerate(results):
            source = hit["_source"]
            content = source.get("content", "")
            context_entry = f"[Document {i+1}]\n{content}"
            contexts.append(context_entry)

        context_text = "\n\n---\n\n".join(contexts)
        prompt_text = prompt.format(context=context_text, question=query)

        # Step 3: Generate response with Ollama
        if stream:
            yield from generate_with_ollama(prompt_text, stream=True)
        else:
            return generate_with_ollama(prompt_text, stream=False)

    except Exception as e:
        error_message = f"Error in RAG process: {str(e)}"
        if stream:
            yield error_message
        else:
            return error_message

# --- Debug Run ---
if __name__ == "__main__":
    query = "Explain data science programs."
    print("Response:\n")
    for chunk in generate_rag_response(query, top_k=3, stream=True):
        print(chunk, end="", flush=True)