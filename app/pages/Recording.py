import streamlit as st
import pandas as pd
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import processors
from mediapipe.tasks.python import vision
import torch
import time

# in seconds
TIME_BETWEEN_TOASTS = 60  # 1 minute
TIME_BETWEEN_BREAKS = 600  # 10 minutes

is_recording = True
col1, col2 = st.columns(2)

if not "time_sat_down" in st.session_state:
    st.session_state.time_sat_down = None
if not "start_time" in st.session_state or st.session_state.start_time == 0:
    st.start_time = time.time()
if not "total_time" in st.session_state:
    st.session_state.total_time = 0
if not "time_in_bad_posture" in st.session_state:
    st.session_state.time_in_bad_posture = 0
if not "time_spent_sitting" in st.session_state:
    st.session_state.time_spent_sitting = [0]
if not "number_of_breaks" in st.session_state:
    st.session_state.number_of_breaks = 0

is_person_there = True
previous_is_person_there = True
time_since_previous_toast = None


def getLabel(results):
    X_test = [[]]
    for i, landmark in enumerate(results.pose_landmarks.landmark):
        X_test[0].append(landmark.x)
        X_test[0].append(landmark.y)
        X_test[0].append(landmark.z)
        X_test[0].append(landmark.visibility)

    model = torch.load("../models/model_0.pth", weights_only=False)
    model.eval()
    X_test = torch.tensor(X_test, dtype=torch.float).to(device="cuda")
    with torch.inference_mode():
        y_logits = model(X_test)

    y_preds_probs = torch.softmax(y_logits, dim=1)
    return torch.argmax(y_preds_probs)


def stop_recording():
    global is_recording
    is_recording = False


def start_recording():
    global is_recording, is_person_there, time_since_previous_toast

    with st.spinner("Loading..." if is_recording else "Exiting..."):
        # Initialize MediaPipe Pose Detection
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        mp_drawing = mp.solutions.drawing_utils
        # Open webcam
        cap = cv2.VideoCapture(0)

    start_time_in_bad_posture = None
    if st.button("Stop Session ❌", use_container_width=True):
        print(f"START time: {start_time_in_bad_posture}")
        stop_recording()
        st.switch_page("pages/Statistics.py")
        return

    img_display = st.empty()
    timer_text = st.empty()

    is_recording = True

    st.session_state.time_in_bad_posture = 0
    st.session_state.time_spent_sitting = [0]
    st.session_state.number_of_breaks = 0
    st.session_state.time_sat_down = time.time()
    st.session_state.start_time = time.time()

    last_break_time = time.time()
    bad_posture_time_recorded = False

    while cap.isOpened() and is_recording:

        # If the user has been sitting for too long and there's been time since the previous toast then show another one
        if (time.time() - last_break_time) >= TIME_BETWEEN_BREAKS and (
            time_since_previous_toast == None
            or (time.time() - time_since_previous_toast) >= TIME_BETWEEN_TOASTS
        ):
            st.toast("Take a break, you've been sitting for too long!", icon="⚠️")
            time_since_previous_toast = time.time()

        ######################################### Pose Landmarks #########################################
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a mirrored view
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        results = pose.process(rgb_frame)

        if results.pose_landmarks == None:
            blank_frame = np.zeros(frame.shape, dtype=np.uint8)
            img_display.image(blank_frame, channels="BGR")
            is_person_there = False
            if is_person_there != previous_is_person_there:
                st.session_state.number_of_breaks += 1
                last_break_time = (
                    time.time()  # if the person goes to take a break then reset the timer
                )
            previous_is_person_there = is_person_there
            # timer_text.text(f"Current time: {(time.time() - start_time):.2f}")
            st.session_state.total_time = time.time() - st.session_state.start_time
            time.sleep(0.2)
            continue
        else:
            # if there wasn't a person there cause they got up, then reset the time to the current time since they just sat down
            if not is_person_there:
                st.session_state.time_sat_down = time.time()
                st.session_state.time_spent_sitting.append(0)

            is_person_there = True
            previous_is_person_there = True
            st.session_state.time_spent_sitting[-1] = (
                time.time() - st.session_state.time_sat_down
            )

        label = getLabel(results)
        color = (
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255))
            if label == 0
            else mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0))
        )

        if label == 0:
            if not bad_posture_time_recorded:
                start_time_in_bad_posture = time.time()
                bad_posture_time_recorded = True
            audio_url = "https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3"
            audio_html = f"""
            <audio autoplay hidden>
              <source src="{audio_url}" type="audio/mp3">
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        else:
            if start_time_in_bad_posture != None:
                st.session_state.time_in_bad_posture += (
                    time.time() - start_time_in_bad_posture
                )
                start_time_in_bad_posture = None
                bad_posture_time_recorded = False

        # Draw pose landmarks if detected
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=color,
            )

        # Display the frame
        img_display.image(frame, channels="BGR", use_container_width=True)

        timer_text.text(
            f"Current time: {(time.time() - st.session_state.start_time):.2f}"
        )
        st.session_state.total_time = time.time() - st.session_state.start_time
        time.sleep(0.2)

    # Release resources
    pose.close()
    cap.release()
    cv2.destroyAllWindows()


start_recording()
