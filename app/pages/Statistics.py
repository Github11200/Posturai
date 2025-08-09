import streamlit as st

# CSS shenanigans
st.markdown(
    """
    <style>
    h1 {
        text-align: center;
    }

    p {
      font-size: x-large;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(f"Session Statistics")

percentage_spent_sitting = (
    sum(st.session_state.time_spent_sitting) / st.session_state.total_time
)
percentage_bad_posture = (
    st.session_state.time_in_bad_posture / st.session_state.total_time
)

with st.container(border=True):
    st.write(f"###### Session length: {(st.session_state.total_time):.1f} seconds")
    st.write(f"###### Number of breaks: {st.session_state.number_of_breaks}")

    if percentage_bad_posture * 100 < 20:
        st.balloons()
        st.toast(
            f"You had bad posture for only **{(percentage_bad_posture * 100):.1f}%** of the time!",
            icon="🥳",
        )
    st.progress(
        percentage_spent_sitting,
        text=f"Amount of time spent sitting **{(percentage_spent_sitting * 100):.1f}%**",
    )
    st.progress(
        percentage_bad_posture,
        text=f"Amount of time with bad posture **{(percentage_bad_posture * 100):.1f}%**",
    )

if st.button("⬅️ Return to the homepage", use_container_width=True):
    st.switch_page("Home.py")
if st.button("Start a new session ⌛", use_container_width=True):
    st.switch_page("pages/Recording.py")


# Add percent and number of seconds for statistics page
