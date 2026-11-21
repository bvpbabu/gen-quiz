import streamlit as st
import google.generativeai as genai

# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Quiz Auto-Generator", page_icon="🧠", layout="centered")
st.title("🧠 Quiz Auto-Generator")
st.write("Paste a topic or a paragraph. Get 5 ready-to-use MCQs with answers and explanations.")

# ── Sidebar: API key ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Setup")
    api_key = st.text_input("Your Gemini API key", type="password",
                            help="Get a free key at https://aistudio.google.com/app/apikey")
    st.markdown("[Get a free key →](https://aistudio.google.com/app/apikey)")

# ── Main input ───────────────────────────────────────────────
user_input = st.text_area(
    "Topic or paragraph:",
    placeholder="e.g.  'Prompt engineering for beginners'  or paste any paragraph from your training material.",
    height=200
)

difficulty = st.selectbox("Difficulty level", ["Easy", "Medium", "Hard"])

# ── Generate ─────────────────────────────────────────────────
if st.button("Generate Quiz ✨", use_container_width=True):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not user_input.strip():
        st.warning("Please enter a topic or paragraph first.")
    else:
        with st.spinner("Generating your quiz…"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt = f"""
You are a corporate training content designer.
Based on the input below, generate exactly 5 multiple-choice questions at {difficulty} level.

Rules:
- Each question must test a distinct idea from the input.
- Give exactly 4 options labelled A, B, C, D.
- Only one option is correct.
- Write one clear sentence explaining why the correct answer is right.
- Do not repeat the same concept twice.

Format every question EXACTLY like this (no extra text before Q1):

Q1. [Question text]
A. ...
B. ...
C. ...
D. ...
Answer: [Letter]
Explanation: [One sentence]

Input:
{user_input}
"""
                response = model.generate_content(prompt)
                st.success("Quiz ready!")
                st.markdown("---")
                st.markdown("### 📋 Your Quiz")
                st.markdown(response.text)

                # Download button
                st.download_button(
                    label="⬇️ Download as .txt",
                    data=response.text,
                    file_name="quiz.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
