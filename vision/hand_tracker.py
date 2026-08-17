import cv2
import mediapipe as mp
import math
import pyautogui
import time
from actions.controller import toggle_play_pause, volume_up, volume_down, next_track, previous_track   


def test_webcam_and_tracking():

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )

    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)


    is_music_playing = True
    last_action_time = 0
    cooldown_seconds = 1.5
    pinch_threshold = 0.05

    is_pinched = False
    reference_y = 0
    volume_sensitivity = 0.00001

    is_pointing = False
    swipe_anchor_x = 0
    swipe_sensitivity = 0.040


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

                fingers_folded = [
                    hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y,
                    hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y,
                    hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y,
                    hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
                ]

                is_fist = all(fingers_folded)
                is_palm = not any(fingers_folded)

                is_index_pointing = (not fingers_folded[0]) and all(fingers_folded[1:])

                current_time = time.time()


                if is_fist and is_music_playing:
                    if (current_time - last_action_time) > cooldown_seconds:
                        print("FIST DETECTED: Pausing Music...")
                        toggle_play_pause()
                        is_music_playing = False
                        last_action_time = current_time
                elif is_palm and not is_music_playing:
                    if (current_time - last_action_time) > cooldown_seconds:
                        print("PALM DETECTED: Playing Music...")
                        toggle_play_pause()
                        is_music_playing = True
                        last_action_time = current_time

                elif distance < pinch_threshold:
                    if not is_pinched:
                        is_pinched = True
                        reference_y = index_y
                        print("JOYSTICK: pinch detected")
                    else: 
                        if index_y < (reference_y - volume_sensitivity):
                            volume_up()
                            reference_y = index_y

                        elif index_y > (reference_y + volume_sensitivity):
                            volume_down()
                            reference_y = index_y
                elif is_index_pointing:
                    if not is_pointing:
                        is_pointing = True
                        swipe_anchor_x = index_x
                        print("\nSWIPE: Point locked. Swipe left or right...")
                    else:
                        if index_x < (swipe_anchor_x - swipe_sensitivity):
                            if (current_time - last_action_time) > cooldown_seconds:
                                next_track()
                                swipe_anchor_x = index_x 
                                last_action_time = current_time

                        elif index_x > (swipe_anchor_x + swipe_sensitivity):
                            if (current_time - last_action_time) > cooldown_seconds:
                                previous_track()
                                swipe_anchor_x = index_x 
                                last_action_time = current_time
                            


                else:
                    if is_pinched:
                        print("Joystick pinch release")
                    is_pinched = False

                    if is_pointing:
                        print("\nSWIPE: Point released.")
                    is_pointing = False
        


        frame = cv2.flip(frame, 1)
        cv2.waitKey(10)

        '''
        cv2.imshow("Vision Engine Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        '''



    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    test_webcam_and_tracking()



