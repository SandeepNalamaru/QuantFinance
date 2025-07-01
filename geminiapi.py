import streamlit as st
import google.generativeai as genai
import re

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Gemini Persona Chatbot",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- API Key Configuration ---
# It's best practice to use Streamlit's secrets management for API keys.
# Create a .streamlit/secrets.toml file with:
# GEMINI_API_KEY="YOUR_API_KEY"
# Or set it as an environment variable before running Streamlit.
api_key = "AIzaSyCAslLfUroiBQAjKCKda8b9kUe7NEhfsuE"

if not api_key:
    st.error("Gemini API Key not found. Please set the 'GEMINI_API_KEY' environment variable or add it to `.streamlit/secrets.toml`.")
    st.stop() # Stop the app if no API key is available

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop() # Stop the app if API configuration fails

# --- Model Configuration ---
MODEL_NAME = 'gemini-1.5-flash-latest'

# Define your system instruction dictionary
system_instructions_dict = {
    "world_cup": "You are a football quiz master who specializes in FIFA World Cup history. Ask challenging multiple-choice questions about World Cup matches, players, and records.",
    "champions_league": "You are an expert in UEFA Champions League trivia. Ask questions about historic games, winning teams, top scorers, and famous moments.",
    "premier_league": "You are a quiz host with deep knowledge of the English Premier League. Ask about clubs, players, managers, and stats.",
    "transfers": "You are a football transfer guru. Ask questions about record signings, player movements between clubs, and notable transfer windows."
    }


def get_quiz_prompt(category):
    return f"""
Generate one football trivia question in the '{category}' category with 4 options (A, B, C, D). Only one should be correct.
Respond in this format strictly:
Question: <your question>
A. <option>
B. <option>
C. <option>
D. <option>
Answer: <Correct option letter only, like 'A'>
"""

# --- Model Initialization ---
@st.cache_resource
def get_generative_model(model_name: str, system_instruction: str):
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction
        )
        st.success(f"Model '{model_name}' initialized")
        return model
    except Exception as e:
        st.error(f"Error initializing generative model: {e}")
        st.stop()

def generate_text(model_instance, prompt: str) -> str:
    try:
        with st.spinner("Generating response... Ahoy, wait for it!"):
            response = model_instance.generate_content(prompt)
            if response.prompt_feedback.block_reason:
                return f"Content blocked: {response.prompt_feedback.block_reason_message}"
            return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def generate_question(model, category):
    prompt = get_quiz_prompt(category)
    raw = generate_text(model, prompt)

    question_match = re.search(r"Question:\s*(.*?)\n", raw)
    options = re.findall(r"[A-D]\.\s*(.*?)\n", raw)
    answer_match = re.search(r"Answer:\s*([A-D])", raw)

    if question_match and options and answer_match:
        return {
            "question": question_match.group(1),
            "options": options,
            "answer": answer_match.group(1)
        }
    else:
        return {"error": "Could not parse question. Output was:\n" + raw}

# --- UI ---
st.title("⚽ SportsHalf Quiz")
st.markdown("Test your football knowledge! Choose a category and try to get all 10 questions right.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.subheader("Quiz Category")
    selected_persona_key = st.selectbox(
        "Choose Category:",
        options=list(system_instructions_dict.keys()),
        index=list(system_instructions_dict.keys()).index("world_cup"),
        help="Pick a category for your quiz questions."
    )
    current_system_instruction = system_instructions_dict[selected_persona_key]
    st.info(f"Current AI instruction: '{current_system_instruction}'")
    st.markdown("---")

# --- Init session state ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "current_qna" not in st.session_state:
    st.session_state.current_qna = {}
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "show_submit" not in st.session_state:
    st.session_state.show_submit = False

# --- Start New Quiz ---
if st.button("Start New Quiz"):
    st.session_state.score = 0
    st.session_state.questions_answered = 0
    st.session_state.question_count = 0
    st.session_state.current_qna = {}
    st.session_state.selected_answer = None
    st.session_state.show_submit = False

# --- Load model ---
model = get_generative_model(MODEL_NAME, current_system_instruction)

# --- Quiz Logic ---
if st.session_state.questions_answered < 10:
    if st.button("Generate Question"):
        qna = generate_question(model, selected_persona_key)
        if "error" not in qna:
            st.session_state.current_qna = qna
            st.session_state.selected_answer = None
            st.session_state.show_submit = True
        else:
            st.error(qna["error"])

    current = st.session_state.current_qna
    if current and "question" in current:
        st.subheader(f"Question {st.session_state.questions_answered + 1}:")
        st.write(current["question"])
        options = current.get("options", [])
        option_labels = [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)]
        selected = st.radio("Choose your answer:", option_labels, key="answer_radio")

        if selected:
            st.session_state.selected_answer = selected.split('.')[0]

        if st.session_state.show_submit and st.button("Submit Answer"):
            st.session_state.show_submit = False
            if st.session_state.selected_answer == current["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer was: {current['answer']}")
            st.session_state.questions_answered += 1

    st.info(f"Score: {st.session_state.score}/{st.session_state.questions_answered}")
    st.progress(st.session_state.questions_answered / 10)
else:
    st.success(f"🎉 Quiz complete! Final score: {st.session_state.score}/10")
    
# test 