<img width="1280" height="720" alt="Posturai Github" src="https://github.com/user-attachments/assets/b39aa511-6279-48f1-804a-47c03163c663" />

## Features
- Ability to detect a good or bad posture
- Reminders for taking breaks
- Session statistics at the end of each session
<img width="345" height="103" alt="Reminders for taking breaks toast" src="https://github.com/user-attachments/assets/631824b4-75e8-4cd0-b47f-05b968e04377" />
<img width="717" height="223" alt="Session statistics" src="https://github.com/user-attachments/assets/e8822dc4-3688-4ad7-8a92-af14d3faa8b6" />
<img width="685" height="530" alt="Posture detection, the image has red dots so it is showing bad posture" src="https://github.com/user-attachments/assets/5534aff5-b1a7-4221-99b3-ad147c6c36bb" />

## Setup
1) Download the GitHub repository and extract the folder.
2) Make sure you have Conda installed.
5) `cd` into whereever you cloned the repository and once you're inside `Hackathon-Project` cd into `app`.
6) Once inside `app`, run the following command, `conda env create -f environment.yml`.
7) Then run `conda activate app` since this is the environment with all the packages.
9) Now, inside the same `app` folder run `streamlit run Home.py`.
10) This should then boot up the app on localhost and you should be able to access it.

## Notes
- You will find that the `data` folder is empty and this is just because we wanted to maintain privacy of the several images that we had taken of oursevles during the course of the project.
- **From our testing the project only builds on Windows and not Mac due to several Windows specific packages.**
- If the project isn't building then it may be possible to follow the steps below to try and run it:
  1) Create a new environment with `conda create -n app` and then run `conda activate app`.
  2) Make sure you're inside the `app` folder of `Hackathon-Project` and then install the following packages:
     - PyTorch
     - Mediapipe
     - OpenCV
     - Strealit
     - Pandas
     - Numpy
   3) Once done, you should be able to run `streamlit run Home.py` from the `app` folder and see the app running on localhost.
- Please make sure you're in a well lit environment and your upperbody is visible in order for the model to be able to detect the points.
- Have your speakers on in order to be able to listen to the ringing sound.
- If the app is not running or you're not able to set up the environment for whatever reason please reach out to us via any of the following contact methods:
  - Emails: jinayunity22@gmail.com, nimidfish@hotmail.com
  - Discords: `aperson3370`, `kfcruan`

## Demo Video
https://www.youtube.com/watch?v=SVa9-QafC50
