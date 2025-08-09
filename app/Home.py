import streamlit as st

result_classes = []
bounding_boxes = []

st.title("Welcome to Posturai!")
st.markdown(
    """Have you ever started working and then unconsciously went into a more relaxed slouched position? This is normal and many people struggle with maintaining good posture."""
)

st.video("images/demo.mp4", autoplay=True, loop=True, muted=True)

if st.button("Start session ⌛", use_container_width=True):
    st.switch_page("pages/Recording.py")

if st.button("Learn more 📕", use_container_width=True):
    st.switch_page("pages/LearnMore.py")
