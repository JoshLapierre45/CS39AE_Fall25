import streamlit as st

st.title("👋 My Bio")

# ---------- TODO: Replace with your own info ----------
NAME = "Josh Lapierre"
PROGRAM = "Bachelors of Science/ Data Science Machine Learning/ Minors in Computer Science and Mathematics/ University of Connecticut"
INTRO = (
    "One project that I am particularly proud of is being part of a team that helps the SDA TAP Lab that also works with the United States Space Force. Our main goal is to create a benchmark dataset for satellite imagery that can be used to train machine learning models to identify and classify objects in space. This project is exciting because it combines my interests in data science, machine learning, and space exploration. "
    "What excites me about data science and machine learning is how they merge logic, creativity, and innovation. Through my work in projects like the SDA TAP Lab and space domain awareness research, I’ve seen how ML can make sense of massive tracking data and enhance space operations."
)
FUN_FACTS = [
    "I love hunting and shooting sports. I find the precision and discipline required in these activities to be both challenging and rewarding. Firearms encorporate a multitude of different fields of study including physics, engineering, and even psychology. I enjoy learning about the mechanics of different firearms and the history behind them.",
    "I’m learning Data Visualizations and how to create compelling stories with data. I believe that effective visualizations can make complex information more accessible and engaging, which is crucial in today’s data-driven world.",
    "I want to build some kind of app that uses machine learning dictate the best ballistics for long-range shooting based on environmental factors like wind, humidity, and temperature. This would be a fun way to combine my interests in data science and shooting sports.",
]
PHOTO_PATH = "C:\Users\joshl\OneDrive\Desktop\CS3250\ConsoleGameHub\ConsoleGameHub\CS39AE_Fall25\streamlit_CS\assets"  # Put a file in repo root or set a URL

# ---------- Layout ----------
col1, col2 = st.columns([1, 2], vertical_alignment="center")

with col1:
    try:
        st.image(PHOTO_PATH, caption=NAME, use_container_width=True)
    except Exception:
        st.info("Add a photo named `your_photo.jpg` to the repo root, or change PHOTO_PATH.")
with col2:
    st.subheader(NAME)
    st.write(PROGRAM)
    st.write(INTRO)

st.markdown("### Fun facts")
for i, f in enumerate(FUN_FACTS, start=1):
    st.write(f"- {f}")

st.divider()
st.caption("Edit `pages/1_Bio.py` to customize this page.")
