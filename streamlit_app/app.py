import streamlit as st
import requests


st.title("Web search using LLMs")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask your query here?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    print("accessing http://localhost:5001/query with query", prompt)
    response = requests.post("http://localhost:5001/query", json={"query": prompt})
    answer = response.json().get('answer', "No answer received.")


    #response = f"Echo: {prompt}"

    with st.chat_message("assistant"):
        st.markdown(answer)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})