import requests
import streamlit as st
import os

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
SESSION_ID_DEFAULT = "default"

st.set_page_config(page_title="AI Tactical Scout", page_icon="⚽", layout="centered")

# --- Small styling (simple CSS) ---
st.markdown("""
<style>
/* Page background + spacing */
.block-container { padding-top: 2rem; max-width: 980px; }

/* "Card" look */
.player-card {
  background: white;
  border: 1px solid #e6e6e6;
  border-radius: 14px;
  padding: 14px 14px;
  margin: 12px 0;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* Tiny labels */
.meta {
  color: #555;
  font-size: 0.95rem;
  margin-top: 2px;
}
.small {
  color: #666;
  font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Joakim", "Jonathan"])

with tab1:
    # --- Header like the mockup ---
    st.markdown("<h2 style='text-align:center; margin-bottom: 0.3rem;'>Sök efter spelare</h2>", unsafe_allow_html=True)
    st.markdown("<div class='small' style='text-align:center; margin-bottom: 1.2rem;'>Skriv en prompt och få 5 bästa matchningar</div>", unsafe_allow_html=True)

    # --- Search bar + button in one row ---
    col_a, col_b = st.columns([5, 1])
    with col_a:
        query = st.text_input(" ", placeholder="T.ex. Jag söker en mittfältare som är bra på tacklingar...", label_visibility="collapsed")
    with col_b:
        search_clicked = st.button("Sök", use_container_width=True)

    # Default image (put a file in frontend folder)
    DEFAULT_IMG = os.path.join(os.path.dirname(__file__), "default_player.png")

    if search_clicked and query.strip():
        response = requests.post(f"{BASE_URL}/list_five_players", json={"query": query})
        # If backend fails, show readable message
        # if not response.headers.get("content-type", "").startswith("application/json"):
        #     st.error(f"Backend did not return JSON. Status: {response.status_code}")
        #     st.text(response.text[:500])
        #     st.stop()
        print(response.text)
        print(response.status_code)
        data = response.json()
        players = data.get("players", [])

        if not players:
            st.warning("No players found.")
        else:
            st.markdown("### Sökresultat")

            for i, p in enumerate(players):
                name = p.get("player_name", "-")
                age = p.get("age", "-")
                pos = p.get("position", "-")
                nat = p.get("nationality", "-")
                club = p.get("current_club", "-")
                price = p.get("asking_price", "-")
                mp = float(p.get("match_percent", 0) or 0)

                # --- Card wrapper (HTML only for the card box) ---
                st.markdown("<div class='player-card'>", unsafe_allow_html=True)

                left, mid, right = st.columns([1.2, 4.2, 1.4], vertical_alignment="center")

                with left:
                    if os.path.exists(DEFAULT_IMG):
                        st.image(DEFAULT_IMG, width=90)
                    else:
                        # If image file is missing, show a simple placeholder
                        st.markdown("🧑‍💼", unsafe_allow_html=True)

                with mid:
                    st.markdown(f"#### {name}")
                    st.markdown(
                        f"<div class='meta'>Ålder: <b>{age}</b> &nbsp;|&nbsp; Position: <b>{pos}</b> &nbsp;|&nbsp; Nationalitet: <b>{nat}</b></div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div class='meta'>Klubb: <b>{club}</b> &nbsp;|&nbsp; Pris: <b>{price}</b></div>",
                        unsafe_allow_html=True
                    )
                    st.progress(min(max(int(mp), 0), 100))
                    st.markdown(f"<div class='small'>Match: <b>{mp:.1f}%</b></div>", unsafe_allow_html=True)

                with right:
                    # Button does nothing yet, but is ready for later
                    st.button("Se profil", key=f"profile_{i}", use_container_width=True)

                st.markdown("</div>", unsafe_allow_html=True)

<<<<<<< HEAD
with tab2:
    if st.button("Send question to AI scout") and query.strip() != "":
        response = requests.post(f"{BASE_URL}/rag/query", json={"query": query, "session_id": SESSION_ID_DEFAULT})
        data = response.json()

        llm_answer = data.get("answer")

        st.write("Our agent recommends this player")
        st.write(llm_answer)

=======
# if st.button("Send question to AI scout") and query.strip() != "":
#     response = requests.post(f"{BASE_URL}/rag/query", json={"query": query, "session_id": SESSION_ID_DEFAULT})
#     data = response.json()

#     llm_answer = data.get("answer")

#     st.write("Our agent recommends this player")
#     st.write(llm_answer)
>>>>>>> 36209425fe9b599c07f0efb5bb380b478b94ad93
