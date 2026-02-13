import streamlit as st
import numpy as np

st.set_page_config(page_title="AI Adaptive Learning", page_icon="🎓", layout="centered")

st.title("🎓 AI Adaptive Learning System")
st.write("Mini-test → AI finds weak topics → gives a personal learning plan.")

# --- Question bank (быстро расширяется) ---
QUESTIONS = [
    # Arithmetic
    {"topic": "Arithmetic", "q": "2 + 7 = ?", "options": ["8", "9", "10"], "ans": 1},
    {"topic": "Arithmetic", "q": "15 - 6 = ?", "options": ["7", "8", "9"], "ans": 2},
    # Algebra
    {"topic": "Algebra", "q": "5x = 20, x = ?", "options": ["2", "4", "5"], "ans": 1},
    {"topic": "Algebra", "q": "x + 3 = 11, x = ?", "options": ["8", "9", "10"], "ans": 0},
    # Geometry
    {"topic": "Geometry", "q": "Area of square with side 4?", "options": ["8", "12", "16"], "ans": 2},
    {"topic": "Geometry", "q": "Sum of angles in a triangle?", "options": ["90°", "180°", "360°"], "ans": 1},
    # Logic
    {"topic": "Logic", "q": "If all A are B and all B are C, then all A are C?", "options": ["Yes", "No"], "ans": 0},
    {"topic": "Logic", "q": "Which is always true? (A and B) implies A", "options": ["True", "False"], "ans": 0},
]

TOPICS = sorted(list({q["topic"] for q in QUESTIONS}))

# --- UI ---
st.header("📝 Mini Test")

user_answers = []
topic_total = {t: 0 for t in TOPICS}
topic_correct = {t: 0 for t in TOPICS}

for i, q in enumerate(QUESTIONS):
    st.markdown(f"**{i+1}. ({q['topic']}) {q['q']}**")
    pick = st.radio("Choose one:", q["options"], key=f"q{i}")
    user_answers.append(q["options"].index(pick))
    topic_total[q["topic"]] += 1
    st.divider()

def build_plan(weakest_topic: str):
    plans = {
        "Arithmetic": [
            "Practice mental math (addition/subtraction) 10 min/day",
            "Do 20 easy arithmetic problems",
            "Do 10 medium word problems",
        ],
        "Algebra": [
            "Review linear equations and substitutions",
            "Solve 15 equations (easy→medium)",
            "Solve 5 word problems with equations",
        ],
        "Geometry": [
            "Review area/perimeter formulas",
            "Solve 10 problems on triangles/quadrilaterals",
            "Solve 5 mixed geometry problems",
        ],
        "Logic": [
            "Practice implications and basic proofs",
            "Solve 10 true/false reasoning questions",
            "Solve 5 olympiad-style logic puzzles",
        ],
    }
    return plans.get(weakest_topic, ["Practice basics and repeat the test."])

if st.button("✅ Submit & Get AI Plan"):
    # score
    for i, q in enumerate(QUESTIONS):
        if user_answers[i] == q["ans"]:
            topic_correct[q["topic"]] += 1

    acc = {t: (topic_correct[t] / max(1, topic_total[t])) for t in TOPICS}
    weakest = min(acc, key=acc.get)

    st.success("Results calculated!")
    st.subheader("📊 Accuracy by topic")
    st.bar_chart(acc)

    st.subheader("🤖 AI Recommendation")
    st.write(f"**Weakest topic detected:** `{weakest}`")
    st.write("**Personal learning plan (next 3 steps):**")
    for step in build_plan(weakest):
        st.write(f"- {step}")

    st.info("For the финал: add more questions, save user progress, and train a real ML model on user histories.")
