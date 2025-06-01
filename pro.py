import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Define the gesture detection function
def detect_sign(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]
    wrist = hand_landmarks.landmark[0]

    # Sign "A": Thumb and index finger close
    if abs(thumb_tip.x - index_tip.x) < 0.05:
        return "A"

    # Sign "B": All fingers above wrist, thumb across palm
    if (index_tip.y < wrist.y and
        middle_tip.y < wrist.y and
        ring_tip.y < wrist.y and
        pinky_tip.y < wrist.y and
        thumb_tip.x < index_tip.x):
        return "B"

    # Sign "C": Moderate thumb-index distance, fingers curve
    if (0.08 < abs(thumb_tip.x - index_tip.x) < 0.15 and
        abs(index_tip.y - pinky_tip.y) < 0.1):
        return "C"

    return "?"

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect sign
            sign = detect_sign(hand_landmarks)

            # Display sign on screen
            cv2.putText(img, sign, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

    cv2.imshow("Hand Sign Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
