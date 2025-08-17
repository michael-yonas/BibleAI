from BibleRag import run_llm
import streamlit as st

st.header("Bible Helper Bot")

# Initialize chat history as a list of (role, message) tuples
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Prompt input
prompt = st.text_input("Prompt", placeholder="Enter your prompt here..")

if prompt:
    with st.spinner("Generating response..."):
        # Save user message
        st.session_state.chat_history.append(("user", prompt))

        # Get AI response
        generated_response = run_llm(query=prompt)
        result_text = generated_response.get("result", "No result returned.")

        # Save assistant message
        st.session_state.chat_history.append(("assistant", result_text))

# Render chat history
for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)
