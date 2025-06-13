import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Gesture history
last_sign = ""
sentence = ""
last_time = 0

# Function to detect word-level gesture
def detect_word(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    wrist = hand_landmarks.landmark[0]

    # WORD: "Hello" (open palm)
    if (index_tip.y < wrist.y and
        middle_tip.y < wrist.y and
        ring_tip.y < wrist.y and
        pinky_tip.y < wrist.y and
        thumb_tip.x < index_tip.x):
        return "Hello"

    # WORD: "Yes" (fist)
    if (abs(thumb_tip.x - index_tip.x) < 0.05 and
        abs(thumb_tip.x - middle_tip.x) < 0.05):
        return "Yes"

    # WORD: "No" (thumb and index making L shape)
    if (abs(thumb_tip.y - index_tip.y) < 0.05 and
        abs(index_tip.x - middle_tip.x) < 0.03):
        return "No"

    return None

# Start Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    current_time = time.time()

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            word = detect_word(hand_landmarks)

            # Confirm gesture is stable for 2 seconds before adding
            if word and word != last_sign:
                last_sign = word
                last_time = current_time
            elif word == last_sign and (current_time - last_time > 1.5):
                sentence += word + " "
                last_sign = ""  # reset so it doesn't repeat

    # Display the sentence
    cv2.putText(img, "Output: " + sentence, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Word-Based Gesture Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
