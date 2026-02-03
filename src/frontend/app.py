import requests
import streamlit as st
import os

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
SESSION_ID_DEFAULT = "default"
query = st.text_input("Ask for a player: ")


if st.button("Search players") and query.strip():
    response = requests.post(f"{BASE_URL}/retrieve_random_player", json={"query": query})
    data = response.json()

    players = data.get("players", [])

    if not players:
        st.warning("No players found.")
    else:
        st.subheader("Search results")
        for p in players:
            st.markdown(f"### {p['player_name']} 🇪🇸" if p.get("nationality") == "Spain" else f"### {p['player_name']}")
            st.write(
                f"Age: {p.get('age', '-')}, "
                f"Position: {p.get('position', '-')}, "
                f"Nationality: {p.get('nationality', '-')}, "
                f"Club: {p.get('current_club', '-')}"
            )
            st.write(f"Asking price: {p.get('asking_price', '-')}")
            st.progress(min(max(int(p.get("match_percent", 0)), 0), 100))
            st.write(f"Match: {p.get('match_percent', 0)}%")
            st.divider()


# if st.button("Send question to AI scout") and query.strip() != "":
#     response = requests.post(f"{BASE_URL}/rag/query", json={"query": query, "session_id": SESSION_ID_DEFAULT})
#     data = response.json()

#     llm_answer = data.get("answer")

#     st.write("Our agent recommends this player")
#     st.write(llm_answer)