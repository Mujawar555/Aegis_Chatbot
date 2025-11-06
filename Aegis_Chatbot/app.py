import streamlit as st
from generation import generate_rag_response

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Aegis Chatbot ")
st.markdown("Ask me questions.")

# Keep chat history in Streamlit session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# User input
if query := st.chat_input("Ask me something about Aegis..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").write(query)

    # Step 1 + 2: Run full RAG pipeline (retrieval + LLM)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_text = ""

        for chunk in generate_rag_response(query, top_k=5, stream=True):
            response_text += chunk
            response_placeholder.markdown(response_text)

        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": response_text})