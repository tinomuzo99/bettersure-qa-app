import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# --- Load .env for OPENAI_API_KEY ---
load_dotenv()

# --- Page config / theming ---
st.set_page_config(
    page_title="BetterSure – Insurance Q&A",
    page_icon="💬",
    layout="centered",
)

PRIMARY = "#214B61"  # BetterSure dark blue
ACCENT = "#F58220"   # BetterSure orange

st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #ffffff; }}
      .bs-title {{ color: {PRIMARY}; font-weight: 700; font-size: 1.6rem; }}
      .bs-subtitle {{ color: #6C8CA1; }}
      .bs-tip b {{ color: {ACCENT}; }}
      .stTextInput > div > div > input::placeholder {{ color: #8aa2b3; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="bs-title">BetterSure – Ask about insurance 💬</div>', unsafe_allow_html=True)
st.markdown('<div class="bs-subtitle">Plain-English answers for consumers. Powered by OpenAI.</div>', unsafe_allow_html=True)
st.divider()
st.markdown(
    f"""
    <style>
      .stApp {{ background-color: #ffffff; }}
      .bs-title {{ color: {PRIMARY}; font-weight: 700; font-size: 1.6rem; }}
      .bs-subtitle {{ color: #6C8CA1; }}
      .bs-tip b {{ color: {ACCENT}; }}
      .stTextInput > div > div > input::placeholder {{ color: #8aa2b3; }}

      /* Ensure Q&A answers render in a visible colour */
      .stMarkdown p {{ color: #222222 !important; font-size: 1rem; }}

      /* Style the small grey caption at the bottom */
      .stCaption, .st-emotion-cache-1aehpvj p {{ color: #444444 !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
      /* Overall app background */
      .stApp {{ background-color: #f9f9f9; }}

      /* Titles and subtitles */
      .bs-title {{ color: {PRIMARY}; font-weight: 700; font-size: 1.6rem; }}
      .bs-subtitle {{ color: #6C8CA1; }}

      /* Make **Tip:** orange */
      .bs-tip b {{ color: {ACCENT}; }}

      /* Input placeholder text */
      .stTextInput > div > div > input::placeholder {{ color: #8aa2b3; }}

      /* Ensure Q&A answers are clearly visible */
      .stMarkdown p {{ color: #222222 !important; font-size: 1rem; }}

      /* Style the small grey caption */
      .stCaption, .st-emotion-cache-1aehpvj p {{ color: #444444 !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)



# --- Safety: check key ---
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found. Add it to a .env file or your environment.")
    st.stop()

client = OpenAI()

# --- Sidebar controls ---
st.sidebar.subheader("Settings")
model = st.sidebar.selectbox(
    "Model",
    ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
    index=0,
)
max_words = st.sidebar.slider("Max words", 60, 180, 120, step=10)
temp = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.7, step=0.1)

# --- Prompting aids ---
placeholder = "e.g. What does ‘excess’ mean? or How are claims processed?"
question = st.text_input("Your question", placeholder=placeholder)

def build_messages(q: str, max_words: int):
    system_prompt = (
        "You are a helpful South African insurance guide. Use plain, friendly language for consumers. "
        "Keep answers concise and practical. Avoid jargon. If a term is essential, define it briefly. "
        f"Target about {max_words} words. If relevant, start a brief tip with **Tip:**"
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": q},
    ]

def render_markdown(answer: str):
    # Convert common markdown (**bold**, *italics*) is already supported by Streamlit.
    # Ensure Tip label stands out with brand accent when rendered.
    answer = answer.replace("**Tip:**", f"**<span style='color:{ACCENT}'>Tip:</span>**")
    st.markdown(answer, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    run = st.button("Get answer", type="primary", use_container_width=True, disabled=not question.strip())
with col2:
    clear = st.button("Clear", use_container_width=True)

if clear:
    st.session_state.pop("last_answer", None)
    st.experimental_rerun()

if run:
    try:
        with st.spinner("Thinking…"):
            messages = build_messages(question, max_words)
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temp,
            )
            answer = resp.choices[0].message.content.strip()
            st.session_state["last_answer"] = answer
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# Show last answer (if any)
if "last_answer" in st.session_state:
    st.subheader("Answer")
    render_markdown(st.session_state["last_answer"])

st.divider()
st.caption(
    "These responses are general information, not advice. For policy specifics, "
    "please check your policy wording or speak to a licensed adviser."
)
