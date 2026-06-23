import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_KEY = "footballgpt-secret-123"
HEADERS = {"X-API-Key": API_KEY}

RAPIDAPI_KEY = "42eb48becemsha59f57e6771f663p186aa4jsn55f3fed7467c"
RAPIDAPI_HOST = "free-api-live-football-data.p.rapidapi.com"
RAPIDAPI_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST,
    "Content-Type": "application/json"
}

st.set_page_config(
    page_title="FootballGPT",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background-image:
        linear-gradient(rgba(0,0,0,0.82), rgba(0,0,0,0.92)),
        url('https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=1920&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
            
.stButton button {
    pointer-events: auto !important;
}
            
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
}
.hero h1 {
    font-family: 'Oswald', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 40px rgba(59,130,246,0.5);
}
.hero h1 span { color: #3b82f6; }
.hero p {
    color: #94a3b8;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.trophy-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 1.2rem 0 1.5rem;
}
.trophy-bar img {
    height: 52px;
    object-fit: contain;
    filter: drop-shadow(0 0 8px rgba(250,204,21,0.4));
    transition: transform 0.2s;
}
.trophy-bar img:hover { transform: scale(1.1); }

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #3b82f6, transparent);
    margin: 0 2rem 2rem;
}

.chat-container {
    background: rgba(0,0,0,0.78);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    min-height: 440px;
    max-height: 520px;
    overflow-y: auto;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}
.msg-user .bubble {
    background: #1d4ed8;
    color: #ffffff;
    padding: 0.7rem 1.1rem;
    border-radius: 16px 16px 4px 16px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.msg-bot {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1rem;
    gap: 10px;
    align-items: flex-start;
}
.bot-avatar {
    width: 32px;
    height: 32px;
    background: #1e3a5f;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    border: 1px solid #3b82f6;
}
.msg-bot .bubble {
    background: rgba(17,24,39,0.95);
    color: #ffffff;
    padding: 0.7rem 1.1rem;
    border-radius: 16px 16px 16px 4px;
    max-width: 80%;
    font-size: 0.9rem;
    line-height: 1.6;
    border: 1px solid rgba(59,130,246,0.15);
}

.route-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.65rem;
    font-weight: 600;
    margin-top: 5px;
    letter-spacing: 0.5px;
}
.route-rag { background: #1e3a5f; color: #60a5fa; }
.route-live { background: #1a2e1a; color: #4ade80; }
.route-memory { background: #2e1a2e; color: #c084fc; }

.sidebar-card {
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(59,130,246,0.15);
    border-radius: 12px;
    padding: 1.2rem;
    backdrop-filter: blur(8px);
    margin-bottom: 1rem;
}
.sidebar-card h4 {
    color: #60a5fa;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0 0 0.8rem;
    font-weight: 500;
}

.match-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.match-teams {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    color: #e2e8f0;
    font-weight: 500;
}
.match-score {
    background: #1d4ed8;
    color: white;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 700;
    font-family: 'Oswald', sans-serif;
    letter-spacing: 1px;
}
.match-score.live {
    background: #dc2626;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
.match-league {
    font-size: 0.68rem;
    color: #475569;
    margin-top: 2px;
}
.live-dot {
    width: 7px;
    height: 7px;
    background: #4ade80;
    border-radius: 50%;
    display: inline-block;
    margin-right: 4px;
    animation: pulse 1s infinite;
}

.stButton button {
    background: rgba(17,24,39,0.8) !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    color: #94a3b8 !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    text-align: left !important;
    padding: 0.5rem 0.8rem !important;
    width: 100% !important;
}
.stButton button:hover {
    border-color: #3b82f6 !important;
    color: #ffffff !important;
    background: rgba(29,78,216,0.2) !important;
}

[data-testid="stChatInputContainer"] {
    background: rgba(0,0,0,0.7) !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInputContainer"] textarea {
    color: #ffffff !important;
    background: transparent !important;
}
.quote-bar {
    text-align: center;
    padding: 0.8rem 4rem 1.8rem;
    color: #64748b;
    font-size: 1rem;
    font-style: italic;
    letter-spacing: 0.5px;
    line-height: 1.6;
}
.quote-mark {
    color: #3b82f6;
    font-size: 1.4rem;
    font-style: normal;
    font-weight: 700;
}
.quote-author {
    color: #3b82f6;
    font-size: 0.75rem;
    font-style: normal;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>Football<span>GPT</span></h1>
    <p>AI-powered football intelligence</p>
</div>
<div class="quote-bar">
    <span class="quote-mark">"</span>
    Football is not just a game. It is a passion, a religion, a way of life.
    <span class="quote-mark">"</span>
    <div class="quote-author">— Zinedine Zidane</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


def get_live_matches():
    try:
        url = f"https://{RAPIDAPI_HOST}/football-get-all-livescores"
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=5)
        data = response.json()
        matches = data.get("response", {}).get("livescore", [])
        return matches[:6] if matches else []
    except:
        return []


def get_upcoming_fixtures():
    try:
        url = f"https://{RAPIDAPI_HOST}/football-get-all-upcoming-fixtures-by-league"
        params = {"leagueId": "EPL"}
        response = requests.get(url, headers=RAPIDAPI_HEADERS, params=params, timeout=5)
        data = response.json()
        return data.get("response", {}).get("fixtures", [])[:5]
    except:
        return []


left, right = st.columns([2.2, 1])

with right:
    live_matches = get_live_matches()
    upcoming = get_upcoming_fixtures()

    st.markdown('<div class="sidebar-card"><h4>⚡ Live & upcoming</h4>', unsafe_allow_html=True)

    if live_matches:
        for m in live_matches:
            home = m.get("homeName", "?")
            away = m.get("awayName", "?")
            score = m.get("score", "? - ?")
            st.markdown(f"""
            <div class="match-card">
                <div>
                    <div class="match-teams">{home} vs {away}</div>
                    <div class="match-league"><span class="live-dot"></span>LIVE</div>
                </div>
                <div class="match-score live">{score}</div>
            </div>""", unsafe_allow_html=True)
    elif upcoming:
        for f in upcoming[:4]:
            home = f.get("homeName", "?")
            away = f.get("awayName", "?")
            st.markdown(f"""
            <div class="match-card">
                <div>
                    <div class="match-teams">{home} vs {away}</div>
                    <div class="match-league">Premier League — Upcoming</div>
                </div>
                <div class="match-score">Soon</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#475569; font-size:0.8rem; padding:0.5rem 0;">No matches right now</div>',
                    unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-card"><h4>Ask me about</h4>', unsafe_allow_html=True)
    quick_questions = [
        "Who won the 2022 World Cup?",
        "Explain tiki-taka tactics",
        "Any live scores right now?",
        "Greatest manager of all time?",
        "Tell me about Mbappe",
        "Explain the offside rule",
    ]
    for q in quick_questions:
     if st.button(q, key=q, use_container_width=True):
        st.session_state["quick_input"] = q
        st.rerun()

with left:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_html = '<div class="chat-container">'
    if not st.session_state.messages:
        chat_html += """
        <div style="text-align:center; padding:3rem 1rem; color:#475569;">
            <div style="font-size:3rem; margin-bottom:1rem;">⚽</div>
            <div style="font-size:0.9rem; letter-spacing:1px;">Ask me anything about football</div>
        </div>"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_html += f'<div class="msg-user"><div class="bubble">{message["content"]}</div></div>'
        else:
            route = message.get("route", "rag")
            badge = f'<br><span class="route-badge route-{route}">{route.upper()}</span>'
            chat_html += f'''
            <div class="msg-bot">
                <div class="bot-avatar">⚽</div>
                <div class="bubble">{message["content"]}{badge}</div>
            </div>'''
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    quick = st.session_state.pop("quick_input", None)
    prompt = st.chat_input("Ask me anything about football...") or quick

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner(""):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": prompt},
                    headers=HEADERS,
                    timeout=60
                )
                data = response.json()
                answer = data["answer"]
                route = data["route"]
            except Exception as e:
                answer = f"Error: {str(e)}"
                route = "rag"
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "route": route
        })
        st.rerun()
