import requests
import streamlit as st
import os

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
SESSION_ID_DEFAULT = "default"
query = st.text_input("Ask for a player: ")

if st.button("Send question to AI scout") and query.strip() != "":
    response = requests.post(f"{BASE_URL}/rag/query", json={"query": query, "session_id": SESSION_ID_DEFAULT})
    data = response.json()

    llm_answer = data.get("answer")

    st.write("Our agent recommends this player")
    st.write(llm_answer)
