import streamlit as st
from agent import (
    chat, save_note, log_mood,
    get_affirmation, get_journal_prompt, get_grounding_exercise
)
from datetime import datetime
import plotly.graph_objects as go

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Reflect — Your Wellness Companion",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ── CALM, SERENE STYLING ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

    /* ── Base ── */
    html, body, .stApp, .main {
        background-color: #f0ede8;
        font-family: 'DM Sans', sans-serif;
        color: #2d2d2d;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #e8e2d9 0%, #ddd5c8 100%);
        border-right: 1px solid #c9bfb0;
    }
    [data-testid="stSidebar"] * { color: #4a4035 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #3a332a !important;
    }

    /* ── Header ── */
    .reflect-header {
        text-align: center;
        padding: 2rem 0 0.5rem;
    }
    .reflect-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        color: #3a332a;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .reflect-subtitle {
        font-size: 0.95rem;
        color: #8a7d6e;
        font-weight: 300;
        margin-top: 0.2rem;
        letter-spacing: 0.3px;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1.5px solid #c9bfb0;
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.88rem;
        color: #a09282;
        background: transparent;
        border-radius: 8px 8px 0 0;
        padding: 8px 18px;
        letter-spacing: 0.3px;
    }
    .stTabs [aria-selected="true"] {
        color: #3a332a !important;
        background: #ede7de !important;
        border-bottom: 2px solid #7c6a52 !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #faf8f5;
        border: 1.5px solid #cfc5b5;
        border-radius: 12px;
        color: #2d2d2d;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.93rem;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #9b8b78;
        box-shadow: 0 0 0 3px rgba(155, 139, 120, 0.15);
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] textarea {
        background: #faf8f5 !important;
        border: 1.5px solid #cfc5b5 !important;
        border-radius: 24px !important;
        font-family: 'DM Sans', sans-serif !important;
        color: #2d2d2d !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: #7c6a52;
        color: #faf8f5;
        border: none;
        border-radius: 24px;
        padding: 9px 22px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.88rem;
        letter-spacing: 0.3px;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(124, 106, 82, 0.2);
    }
    .stButton > button:hover {
        background: #6b5a43;
        box-shadow: 0 4px 16px rgba(124, 106, 82, 0.3);
        transform: translateY(-1px);
    }

    /* ── Mood buttons ── */
    .mood-row .stButton > button {
        background: #faf8f5;
        color: #4a4035;
        border: 1.5px solid #cfc5b5;
        border-radius: 16px;
        font-size: 1.3rem;
        padding: 12px 8px;
        width: 100%;
    }
    .mood-row .stButton > button:hover {
        background: #ede7de;
        border-color: #9b8b78;
        transform: translateY(-2px);
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        background: #faf8f5;
        border-radius: 16px;
        border: 1px solid #e0d9cf;
        margin: 6px 0;
        padding: 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    [data-testid="stChatMessage"] p {
        color: #2d2d2d;
        font-size: 0.95rem;
        line-height: 1.65;
    }

    /* ── Memory box ── */
    .memory-box {
        background: #faf8f5;
        border-left: 3px solid #9b8b78;
        padding: 9px 14px;
        border-radius: 8px;
        margin: 5px 0;
        font-size: 0.82rem;
        color: #6b5a43;
        font-family: 'DM Sans', sans-serif;
        line-height: 1.5;
    }

    /* ── Timestamp ── */
    .timestamp {
        color: #bdb3a7;
        font-size: 0.72rem;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Cards ── */
    .calm-card {
        background: #faf8f5;
        border: 1px solid #e0d9cf;
        border-radius: 16px;
        padding: 18px 22px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .calm-card h4 {
        font-family: 'DM Serif Display', serif;
        color: #3a332a;
        margin: 0 0 8px;
        font-size: 1.05rem;
    }
    .calm-card p, .calm-card li {
        color: #5a5048;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 4px 0;
    }

    /* ── Affirmation card ── */
    .affirmation-card {
        background: linear-gradient(135deg, #e8e2d9 0%, #ddd5c8 100%);
        border: 1px solid #c9bfb0;
        border-radius: 20px;
        padding: 24px 28px;
        text-align: center;
        margin: 12px 0;
    }
    .affirmation-card p {
        font-family: 'DM Serif Display', serif;
        font-style: italic;
        font-size: 1.15rem;
        color: #3a332a;
        line-height: 1.6;
        margin: 0;
    }

    /* ── Crisis banner ── */
    .crisis-banner {
        background: #fff5f0;
        border: 1.5px solid #e8a090;
        border-radius: 14px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .crisis-banner p { color: #7a3a2a; font-size: 0.9rem; margin: 3px 0; }

    /* ── Grounding card ── */
    .grounding-card {
        background: #f5f2ee;
        border: 1px solid #d9d0c4;
        border-radius: 16px;
        padding: 20px 24px;
        margin: 10px 0;
    }
    .grounding-step {
        background: #faf8f5;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #4a4035;
        font-size: 0.9rem;
        line-height: 1.5;
        border: 1px solid #e0d9cf;
    }

    /* ── Divider ── */
    hr { border-color: #e0d9cf; }

    /* ── Section headers ── */
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #3a332a !important;
    }
    h4, h5, h6, label, p {
        font-family: 'DM Sans', sans-serif;
        color: #4a4035;
    }

    /* ── Metrics ── */
    [data-testid="stMetric"] {
        background: #faf8f5;
        border: 1px solid #e0d9cf;
        border-radius: 12px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] { color: #8a7d6e !important; font-size: 0.8rem !important; }
    [data-testid="stMetricValue"] { color: #3a332a !important; font-family: 'DM Serif Display', serif !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #9b8b78 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #faf8f5 !important;
        border: 1px solid #e0d9cf !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        color: #4a4035 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0ede8; }
    ::-webkit-scrollbar-thumb { background: #c9bfb0; border-radius: 10px; }

    /* ── Hide Streamlit branding ── */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello, I'm Reflect 🌿 I'm here to listen — without judgment, without rush. I'll remember what you share with me over time, so you never have to start from scratch. How are you feeling today?",
        "time": datetime.now().strftime("%H:%M")
    }]

for key in ["notes", "mood_logs"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "mood_checked" not in st.session_state:
    st.session_state.mood_checked = False

if "affirmation" not in st.session_state:
    st.session_state.affirmation = get_affirmation()

if "journal_prompt" not in st.session_state:
    st.session_state.journal_prompt = get_journal_prompt()

if "grounding_type" not in st.session_state:
    st.session_state.grounding_type = "box-breathing"

# ── HEADER ──
st.markdown("""
<div class="reflect-header">
    <p class="reflect-title">🌿 Reflect</p>
    <p class="reflect-subtitle">Your calm, remembering wellness companion</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── MOOD CHECK-IN ──
if not st.session_state.mood_checked:
    st.markdown("### How are you feeling right now?")
    st.markdown("<p style='color:#8a7d6e; font-size:0.9rem; margin-bottom:12px;'>Take a moment. There's no right answer.</p>", unsafe_allow_html=True)
    moods = [("😊", "Happy"), ("😐", "Neutral"), ("😔", "Sad"), ("😤", "Frustrated"), ("😰", "Anxious")]
    cols = st.columns(5)
    st.markdown('<div class="mood-row">', unsafe_allow_html=True)
    for i, (emoji, label) in enumerate(moods):
        with cols[i]:
            if st.button(f"{emoji}\n{label}", key=f"mood_{label}"):
                log_mood(label)
                st.session_state.mood_logs.append({
                    "mood": label, "emoji": emoji,
                    "time": datetime.now().strftime("%b %d, %H:%M")
                })
                st.session_state.mood_checked = True
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 🌿 Reflect")
    st.divider()

    # Daily affirmation
    st.markdown("#### ✨ Today's Affirmation")
    st.markdown(f"""
    <div class="affirmation-card">
        <p>{st.session_state.affirmation}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("New affirmation", key="new_aff"):
        st.session_state.affirmation = get_affirmation()
        st.rerun()

    st.divider()

    # Memories
    st.markdown("#### 🧠 What I Remember")
    st.markdown("<p style='font-size:0.82rem; color:#8a7d6e;'>Memories from our conversations</p>", unsafe_allow_html=True)
    memory_placeholder = st.empty()

    st.divider()

    # Quick grounding
    st.markdown("#### 🫁 Quick Grounding")
    grounding_choice = st.selectbox(
        "Choose an exercise",
        options=["box-breathing", "5-4-3-2-1", "body-scan"],
        format_func=lambda x: {"box-breathing": "Box Breathing", "5-4-3-2-1": "5-4-3-2-1 Senses", "body-scan": "Body Scan"}[x],
        key="ground_select"
    )
    if st.button("Show exercise", key="show_ground"):
        st.session_state.grounding_type = grounding_choice

    if st.session_state.grounding_type:
        ex = get_grounding_exercise(st.session_state.grounding_type)
        st.markdown(f"**{ex['title']}**")
        for step in ex["steps"]:
            st.markdown(f"<div class='grounding-step'>{step}</div>", unsafe_allow_html=True)

# ── TABS ──
chat_tab, journal_tab, notes_tab, mood_tab, tools_tab = st.tabs([
    "💬 Chat", "📓 Journal", "📝 Notes", "📊 Mood", "🛠 Tools"
])

# ── CHAT TAB ──
with chat_tab:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            st.markdown(f"<span class='timestamp'>{msg.get('time', '')}</span>", unsafe_allow_html=True)

    if prompt := st.chat_input("Share what's on your mind…"):
        st.session_state.messages.append({
            "role": "user", "content": prompt,
            "time": datetime.now().strftime("%H:%M")
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Reflect is with you…"):
                reply, memories, flags = chat(prompt)

            # Crisis support banner
            if flags.get("is_crisis"):
                st.markdown("""
                <div class="crisis-banner">
                    <p>💛 <b>You're not alone.</b> If you're in crisis, please reach out:</p>
                    <p>📞 <b>Crisis Helpline:</b> 988 (US) · 116 123 (UK) · 8888 (Pakistan)</p>
                    <p>💬 <b>Crisis Text Line:</b> Text HOME to 741741</p>
                </div>
                """, unsafe_allow_html=True)

            # Grounding suggestion
            if flags.get("needs_grounding"):
                st.markdown("""
                <div class="calm-card" style="margin-bottom:8px;">
                    <p>🫁 <b>It sounds like you might benefit from a grounding exercise.</b> Try the Box Breathing exercise in the sidebar — it only takes 2 minutes. 🌿</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(reply)
            st.markdown(f"<span class='timestamp'>{datetime.now().strftime('%H:%M')}</span>", unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant", "content": reply,
            "time": datetime.now().strftime("%H:%M")
        })

        # Update sidebar memories
        with memory_placeholder.container():
            if memories:
                results = memories.get("results", memories)
                if results:
                    for m in results:
                        txt = m.get("memory", "")
                        if txt:
                            st.markdown(f"<div class='memory-box'>💭 {txt}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='font-size:0.82rem; color:#8a7d6e;'>Keep chatting — memories will appear here 🌿</p>", unsafe_allow_html=True)

# ── JOURNAL TAB ──
with journal_tab:
    st.markdown("### 📓 Reflective Journal")
    st.markdown("<p style='color:#8a7d6e;'>Writing helps you process. Your words are safe here.</p>", unsafe_allow_html=True)
    st.divider()

    # Journal prompt
    st.markdown(f"""
    <div class="affirmation-card">
        <p style="font-size:1rem;">✍️ {st.session_state.journal_prompt}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("New prompt", key="new_prompt"):
            st.session_state.journal_prompt = get_journal_prompt()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    journal_content = st.text_area(
        "Your thoughts",
        placeholder="Let it flow — no judgment here…",
        height=220,
        key="journal_area"
    )

    if st.button("💾 Save to Reflect's memory", key="save_journal"):
        if journal_content.strip():
            save_note("Journal entry", journal_content)
            st.session_state.notes.append({
                "heading": f"Journal — {datetime.now().strftime('%b %d')}",
                "content": journal_content,
                "time": datetime.now().strftime("%b %d, %H:%M")
            })
            st.success("Saved 🌿 Reflect will carry this with you.")
        else:
            st.warning("Write something first — even a single sentence counts.")

# ── NOTES TAB ──
with notes_tab:
    st.markdown("### 📝 Personal Notes")
    st.markdown("<p style='color:#8a7d6e;'>Notes help Reflect understand you better over time.</p>", unsafe_allow_html=True)
    st.divider()

    heading = st.text_input("Note title", placeholder="e.g. What helps me feel calm")
    content = st.text_area(
        "Your note",
        placeholder="Feelings, patterns, things you've noticed about yourself…",
        height=160
    )

    if st.button("💾 Save Note"):
        if heading.strip() and content.strip():
            save_note(heading, content)
            st.session_state.notes.append({
                "heading": heading, "content": content,
                "time": datetime.now().strftime("%b %d, %H:%M")
            })
            st.success("Note saved — Reflect will remember this 🌿")
        else:
            st.warning("Please add both a title and content.")

    if st.session_state.notes:
        st.divider()
        st.markdown("#### Saved Notes")
        for note in reversed(st.session_state.notes):
            with st.expander(f"📌 {note['heading']} — {note['time']}"):
                st.markdown(f"<p style='color:#4a4035; line-height:1.7;'>{note['content']}</p>", unsafe_allow_html=True)

# ── MOOD TAB ──
with mood_tab:
    st.markdown("### 📊 Your Mood Journey")
    st.markdown("<p style='color:#8a7d6e;'>Patterns become visible over time. Be patient with yourself.</p>", unsafe_allow_html=True)
    st.divider()

    if not st.session_state.mood_logs:
        st.markdown("""
        <div class="calm-card" style="text-align:center; padding: 40px;">
            <p style="font-size:2rem;">🌱</p>
            <p>No mood data yet. Check in each day and watch your journey unfold.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        mood_scores = {"Happy": 5, "Neutral": 3, "Sad": 1, "Frustrated": 2, "Anxious": 2}
        mood_colors = {
            "Happy": "#7c9b78", "Neutral": "#9b8b78",
            "Sad": "#7a8fa0", "Frustrated": "#b07a6a", "Anxious": "#a09070"
        }

        times  = [m["time"]  for m in st.session_state.mood_logs]
        scores = [mood_scores.get(m["mood"], 3) for m in st.session_state.mood_logs]
        emojis = [m["emoji"] for m in st.session_state.mood_logs]
        moods  = [m["mood"]  for m in st.session_state.mood_logs]
        colors = [mood_colors.get(m["mood"], "#9b8b78") for m in st.session_state.mood_logs]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times, y=scores,
            fill="tozeroy",
            fillcolor="rgba(155, 139, 120, 0.12)",
            line=dict(color="#9b8b78", width=2.5),
            mode="lines+markers+text",
            marker=dict(size=15, color=colors, line=dict(color="#faf8f5", width=2)),
            text=emojis,
            textposition="top center",
            hovertemplate="<b>%{customdata}</b><br>%{x}<extra></extra>",
            customdata=moods
        ))
        fig.update_layout(
            paper_bgcolor="#f0ede8",
            plot_bgcolor="#f0ede8",
            font=dict(color="#4a4035", family="DM Sans"),
            xaxis=dict(showgrid=False, color="#bdb3a7", title=""),
            yaxis=dict(
                showgrid=True, gridcolor="#e0d9cf", color="#bdb3a7",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["😔 Sad", "😤 Low", "😐 Neutral", "🙂 Good", "😊 Happy"],
                range=[0, 6]
            ),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False, height=320
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        col1, col2, col3 = st.columns(3)
        most_common = max(set(moods), key=moods.count)
        latest = st.session_state.mood_logs[-1]
        with col1:
            st.metric("Check-ins", f"{len(moods)}")
        with col2:
            st.metric("Most Common", most_common)
        with col3:
            st.metric("Latest", f"{latest['emoji']} {latest['mood']}")

        st.divider()
        st.markdown("#### History")
        for entry in reversed(st.session_state.mood_logs):
            st.markdown(
                f"<div class='memory-box'>{entry['emoji']} <b>{entry['mood']}</b> — <span style='color:#bdb3a7;'>{entry['time']}</span></div>",
                unsafe_allow_html=True
            )

# ── TOOLS TAB ──
with tools_tab:
    st.markdown("### 🛠 Wellness Tools")
    st.markdown("<p style='color:#8a7d6e;'>Simple practices to help you feel more grounded.</p>", unsafe_allow_html=True)
    st.divider()

    # Breathing exercises
    st.markdown("#### 🫁 Breathing & Grounding")
    ex_type = st.radio(
        "Choose a practice",
        options=["box-breathing", "5-4-3-2-1", "body-scan"],
        format_func=lambda x: {"box-breathing": "📦 Box Breathing", "5-4-3-2-1": "🖐 5-4-3-2-1 Grounding", "body-scan": "🧘 Body Scan"}[x],
        horizontal=True,
        key="tools_ground_radio"
    )
    ex = get_grounding_exercise(ex_type)
    st.markdown(f"""<div class="grounding-card"><h4>🌿 {ex['title']}</h4>""", unsafe_allow_html=True)
    for i, step in enumerate(ex["steps"], 1):
        st.markdown(f"<div class='grounding-step'><b>{i}.</b> {step}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Affirmations
    st.markdown("#### ✨ Daily Affirmations")
    st.markdown(f"""
    <div class="affirmation-card">
        <p>{st.session_state.affirmation}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Refresh affirmation ✨", key="tools_aff"):
        st.session_state.affirmation = get_affirmation()
        st.rerun()

    st.divider()

    # Crisis resources
    st.markdown("#### 💛 Crisis Resources")
    st.markdown("""
    <div class="crisis-banner">
        <p>If you or someone you know is in crisis, please reach out:</p>
        <p>📞 <b>988 Suicide & Crisis Lifeline</b> — Call or text 988 (US)</p>
        <p>💬 <b>Crisis Text Line</b> — Text HOME to 741741</p>
        <p>📞 <b>Samaritans</b> — 116 123 (UK & Ireland)</p>
        <p>📞 <b>Umang Pakistan</b> — 0317-4288665</p>
        <p style="margin-top:8px; font-style:italic;">You are not alone. Help is always available. 💛</p>
    </div>
    """, unsafe_allow_html=True)