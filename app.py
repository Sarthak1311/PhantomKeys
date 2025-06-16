import streamlit as st
import subprocess

st.set_page_config(page_title="Phantom Keys", layout="centered")

st.title("🎹🖱️ PhantomKeys - Hand Controlled Mouse & Piano")
st.markdown("Control your computer and music using just your hand gestures.")

option = st.selectbox(
    "Choose an Application to Launch:",
    ("-- Select --", "🖱️ Virtual Mouse", "🎹 Virtual Piano")
)

if option != "-- Select --":
    st.markdown("### 📌 Instructions")

    if option == "🖱️ Virtual Mouse":
        st.write("- Use **Index + Middle finger** close together to left-click.")
        st.write("- Use **Thumb + Index finger** close together to right-click.")
        st.write("- Use all three fingers to drag.")
        st.write("- Press `Esc` to quit.")
        if st.button("▶️ Start Virtual Mouse"):
            subprocess.Popen(["python", "handpointer.py"])

    elif option == "🎹 Virtual Piano":
        st.write("- Hold your fingers above the screen to play notes.")
        st.write("- Make sure the piano script handles sound & visuals.")
        st.write("- Press `Esc` to quit.")
        if st.button("▶️ Start Virtual Piano"):
            subprocess.Popen(["python", "virtualPiano.py"])
