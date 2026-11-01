import streamlit as st
from appp import DataHandler
from responsegeneration import build_prompt, get_ollama_response
st.set_page_config(page_title="Fitness Passport Agent")
st.title("Fitness Support Agent")

# Cache the database so it only loads once per session
@st.cache_resource
def load_db():
    return DataHandler()

handler = load_db()

# Maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            docs, metas = handler.retrieve(prompt)
            final_prompt = build_prompt(prompt, docs)
            response = get_ollama_response(final_prompt, metas)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})

