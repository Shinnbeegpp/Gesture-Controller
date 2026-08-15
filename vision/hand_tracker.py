import cv2
import mediapipe as mp
import math
import pyautogui
from actions.controller import toggle_play_pause    


def test_webcam_and_tracking():

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )

    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    is_pinched = False
    pinch_threshold = 0.05

    print('Starting Vision Engine... Press Q in the Video window to quit.')

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to grab a Frame. Check your Webcam.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                thumb_x = hand_landmarks.landmark[4].x
                thumb_y = hand_landmarks.landmark[4].y

                index_x = hand_landmarks.landmark[8].x
                index_y = hand_landmarks.landmark[8].y

                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

                if distance < pinch_threshold and not is_pinched:
                    print("PINCH TRIGGERED! Toggling PLay/Pause...")
                    toggle_play_pause()
                    is_pinched = True
                elif distance > pinch_threshold and is_pinched:
                    print("Pinch release. Ready for next command")
                    is_pinched = False


        frame = cv2.flip(frame, 1)

        cv2.imshow("Vision Engine Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



test_webcam_and_tracking()




