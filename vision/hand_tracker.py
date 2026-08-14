import cv2
import mediapipe as mp


def test_webcam_and_tracking():

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )

    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

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

        frame = cv2.flip(frame, 1)

        cv2.imshow("Vision Engine Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

test_webcam_and_tracking()




