from PIL import Image
import streamlit as st

# CSS shenanigans
st.markdown(
    """
    <style>
    p {
      text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("About Posturai")

st.markdown(
    "<div>" "<h5>Good Posture has many Health Benefits including:</h5>" "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
<ul style="padding-left: 20px;">
  <li>Reduced neck and back pain</li>
  <li>Improved joint health</li>
  <li>Better breathing</li>
  <li>Enhanced digestion</li>
  <li>Increased core and muscle strength</li>
</ul>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """With Posturai, it will notify you when you have become more slouched or if you need to get up and move around a bit. To start, simply press Start Session"""
)

st.write("## Features")
st.markdown(
    "<div style='text-align: center;'>"
    "<h5>Posturai will turn red if you have bad posture.</h5>"
    "</div>",
    unsafe_allow_html=True,
)
image = Image.open("images/funnyface.png")
st.image(image, width=800)

st.markdown(
    "<div style='text-align: center;'>"
    "<h5>Posturai will remind you to take breaks.</h5>"
    "</div>",
    unsafe_allow_html=True,
)
break_image = Image.open("images/toast.png")
st.image(break_image, width=800)

st.markdown(
    "<div style='text-align: center;'>"
    "<h5>Posturai will give you statistics after each session.</h5>"
    "</div>",
    unsafe_allow_html=True,
)
stats_image = Image.open("images/statistics.png")
st.image(stats_image, width=800)

if st.button("⬅️ Homepage", use_container_width=True):
    st.switch_page("Home.py")
