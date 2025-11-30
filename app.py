import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests

# --- Page Config ---
st.set_page_config(page_title="Student Future Predictor", page_icon="🎓", layout="wide")

# --- Gradient Background & Stylish Content ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #4CAF50, #81C784, #AED581, #C8E6C9);
        color: #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stContainer {
        background-color: rgba(255,255,255,0.95);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
    }

    .stButton>button {
        background-color: #2196F3;
        color: white;
        border-radius: 12px;
        height: 45px;
        width: 100%;
        font-size: 16px;
        font-weight: bold;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stSlider>div>div>div>div>input {
        accent-color: #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State ---
if 'start' not in st.session_state:
    st.session_state.start = False

# --- Load Lottie safely ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {}

# Only the single welcome animation
lottie_main = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_touohxv0.json")  # trophy

# --- Welcome Page ---
if not st.session_state.start:
    st.title("🎉 Welcome to Student Future Predictor!")

    if lottie_main:
        st_lottie(lottie_main, speed=0.5, height=300, key="main")

    name = st.text_input("Enter your name ✏️")
    if st.button("Start Your Journey 🚀") and name.strip() != "":
        st.session_state.start = True
        st.session_state.name = name
        st.balloons()  # 🎊 Confetti

# --- Main App ---
else:
    st.markdown(f"<h2 style='color:b'>Hello, {st.session_state.name}! 🎓 Let's explore your future.</h2>", unsafe_allow_html=True)

    # --- Sidebar Branch Selection ---
    branch = st.selectbox(
        "Select your branch",
        ("AIML", "CSE", "ECE", "MECH", "EEE", "MME", "CHEMICAL", "CIVIL")
    )

    # --- Load Dataset ---
    try:
        df = pd.read_csv(f"data/{branch.lower()}.csv")
        df.columns = df.columns.str.strip()
        subjects = ["Math", "Programming", "Physics_BE", "Engineering_Drawing", "English"]
        df = df[subjects]
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

    short_labels = ["Math", "Prog", "Phys_BE", "Eng_Draw", "Eng"]

    # --- Student Input ---
    st.subheader("✏️ Enter Your Marks")
    student_marks = {}
    for sub in subjects:
        student_marks[sub] = st.slider(f"{sub} Marks", 0, 100, 50)
    student_marks_df = pd.DataFrame([student_marks])

    # --- Branch average & percentiles ---
    branch_avg = df.mean(numeric_only=True)
    percentiles = {sub: (df[sub] < student_marks[sub]).mean()*100 for sub in subjects}

    # --- Weak subjects for Study Guide ---
    study_tips = {
        "Math": "Practice problem-solving daily. Focus on algebra, calculus, and statistics.",
        "Programming": "Work on small projects and coding exercises. Learn algorithms and data structures.",
        "Physics_BE": "Revise core concepts and solve previous years’ questions. Focus on practical applications.",
        "Engineering_Drawing": "Practice drawing diagrams, reading blueprints, and CAD exercises.",
        "English": "Read technical articles, practice writing, and improve vocabulary."
    }

    weak_subjects = []
    threshold = 60
    for sub in subjects:
        if student_marks[sub] < branch_avg[sub] or student_marks[sub] < threshold:
            weak_subjects.append(sub)

    # --- Career Suggestions ---
    career_suggestions = {
        "Math": ["AI/ML Engineer 🤖", "Data Scientist 📊", "Control Systems ⚙️", "Structural Engineer 🏗️"],
        "Programming": ["Software Developer 💻", "Web Developer 🌐", "AI Engineer 🤖", "Cybersecurity Specialist 🔒"],
        "Physics_BE": ["Electronics Engineer ⚡", "Electrical Design 💡", "Robotics Engineer 🤖", "Embedded Systems 🛠️"],
        "Engineering_Drawing": ["Mechanical Designer ⚙️", "Civil Drafting 🏗️", "CAD Engineer 💻", "Product Designer 🖌️"],
        "English": ["Management 📈", "Technical Writing ✍️", "Public Relations 📢", "Business Analyst 💼"]
    }

    # --- Prepare Charts ---
    fig, ax = plt.subplots(figsize=(8,5))
    x = np.arange(len(subjects))
    width = 0.35
    ax.bar(x - width/2, student_marks_df.T[0], width, label='Your Marks', color="#4CAF50")
    ax.bar(x + width/2, branch_avg, width, label=f'{branch} Avg', color="#2196F3")
    ax.set_xticks(x)
    ax.set_xticklabels(short_labels, rotation=30, ha='right')
    ax.set_ylim(0, 100)
    ax.set_ylabel("Marks")
    ax.set_title("Your Marks vs Branch Average")
    ax.legend()

    values = list(student_marks.values())
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(subjects), endpoint=False).tolist()
    angles += angles[:1]

    fig2, ax2 = plt.subplots(figsize=(4.5,4.5), subplot_kw=dict(polar=True))
    ax2.plot(angles, values, 'o-', linewidth=2, label='Your Marks', color="#FF5722")
    ax2.fill(angles, values, alpha=0.25, color="#FF5722")
    ax2.set_thetagrids(np.degrees(angles[:-1]), short_labels)
    ax2.set_ylim(0, 100)
    ax2.set_title("Strengths Radar Chart", fontsize=12)

    # --- Buttons ---
    st.markdown("### Click to reveal sections")
    col1, col2, col3, col4 = st.columns(4)
    with col1: show_comparison = st.button("📊 Comparison")
    with col2: show_percentile = st.button("📈 Percentiles")
    with col3: show_bar = st.button("📊 Bar Chart")
    with col4: show_radar = st.button("🕸️ Radar Chart")
    col5, col6, col7 = st.columns(3)
    with col5: show_career = st.button("💡 Career Suggestions")
    with col6: show_study = st.button("📘 Study Guide")
    with col7: show_pred = st.button("🔮 Predicted Trend")

    # --- Display Sections ---
    if show_comparison:
        comparison_df = pd.DataFrame({
            "Your Marks": student_marks_df.T[0],
            "Branch Average": branch_avg
        })
        st.dataframe(comparison_df)

    if show_percentile:
        st.dataframe(pd.DataFrame(percentiles, index=["Percentile"]))

    if show_bar:
        st.pyplot(fig)

    if show_radar:
        st.pyplot(fig2)

    if show_career:
        strongest_subj = max(student_marks, key=student_marks.get)
        st.success(f"🌟 Your strongest subject is **{strongest_subj}**")
        st.markdown("**Recommended Career Paths:**")
        for career in career_suggestions[strongest_subj]:
            st.markdown(f"- {career}")

    if show_study:
        if weak_subjects:
            st.warning("⚠️ You should focus on improving these subjects:")
            for sub in weak_subjects:
                st.markdown(f"**{sub}**: {study_tips[sub]}")
        else:
            st.success("🎉 Great job! You are performing above average in all subjects")

    if show_pred:
        current_percentile = np.mean(list(percentiles.values()))
        predicted_percentile = min(current_percentile + np.random.randint(5,11), 100)
        st.metric("📈 Predicted Next Semester Percentile", f"{predicted_percentile:.1f}%")
