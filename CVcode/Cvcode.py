import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
arduino_connection = serial.Serial(port='COM3', baudrate=9600, timeout=1)
time.sleep(2)  # Allow Arduino to initialize

# Initialize Mediapipe
mp_hand_solution = mp.solutions.hands
hand_detector = mp_hand_solution.Hands()
mp_visualizer = mp.solutions.drawing_utils

# Function to detect individual fingers (1 for up, 0 for down)
def detect_finger_states(frame, hand_landmarks):
    fingertip_indices = [8, 12, 16, 20]  # Indexes for finger tips
    thumb_tip_index = 4
    finger_status = [0, 0, 0, 0, 0]  # Initialize finger states

    if hand_landmarks.landmark[thumb_tip_index].x < hand_landmarks.landmark[thumb_tip_index - 1].x:
        finger_status[0] = 1  # Thumb is up

    # Check the other fingers
    for i, tip_index in enumerate(fingertip_indices):
        if hand_landmarks.landmark[tip_index].y < hand_landmarks.landmark[tip_index - 2].y:
            finger_status[i + 1] = 1  # Finger is up

    return finger_status

video_stream = cv2.VideoCapture(0)

while video_stream.isOpened():
    success, frame = video_stream.read()
    if not success:
        break

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    detection_results = hand_detector.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Check for hand landmarks
    if detection_results.multi_hand_landmarks:
        for landmarks in detection_results.multi_hand_landmarks:
            mp_visualizer.draw_landmarks(frame, landmarks, mp_hand_solution.HAND_CONNECTIONS)
            detected_finger_states = detect_finger_states(frame, landmarks)
            
            # Send finger states to Arduino
            arduino_connection.write(bytes(detected_finger_states))
            print(f"Finger States: {detected_finger_states}")

    # Display the video feed
    cv2.imshow('Hand Gesture Tracker', frame)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release resources
video_stream.release()
cv2.destroyAllWindows()
arduino_connection.close()
