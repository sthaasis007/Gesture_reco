# import cv2
# import mediapipe as mp

# #run camera until 'q' is pressed
# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert the frame to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Process the frame with MediaPipe Hands
#     hands = mp.solutions.hands.Hands()
#     results = hands.process(rgb_frame)

#     # Draw hand landmarks on the frame
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

#     # Display the frame
#     cv2.imshow('Hand Detection', frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp
# import pyttsx3
# import time

# # Initialize TTS engine
# engine = pyttsx3.init()

# # Initialize MediaPipe
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_draw = mp.solutions.drawing_utils

# # Detect finger states (1 = up, 0 = down)
# def get_finger_states(landmarks):
#     tips = [4, 8, 12, 16, 20]
#     states = []

#     # Thumb
#     if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
#         states.append(1)
#     else:
#         states.append(0)

#     # Other fingers
#     for i in range(1, 5):
#         if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
#             states.append(1)
#         else:
#             states.append(0)
#     return states

# # Detect word from gestures
# def detect_word(landmarks):
#     states = get_finger_states(landmarks)

#     # Print live values to debug
#     print(f"Finger States: {states}")
#     print(f"Wrist Y: {landmarks[0].y:.2f}, Index Y: {landmarks[8].y:.2f}")
#     print(f"Thumb tip X: {landmarks[4].x:.2f}, Thumb joint X: {landmarks[3].x:.2f}")

#     if states == [1, 1, 1, 1, 1]:
#         return "Stop"

#     if states == [1, 0, 0, 0, 0]:
#         return "Yes"

#     if states == [0, 1, 0, 0, 0]:
#         return "No"

#     # HELLO = palm facing camera
#     if states == [1, 1, 1, 1, 1] and abs(landmarks[4].x - landmarks[3].x) > 0.03:
#         return "Hello"


#     # THANKS = all fingers up, hand raised
#     if states == [1, 1, 1, 1, 1] and landmarks[8].y < landmarks[0].y - 0.1:
#         return "Thanks"


#     return "?"



# # Open webcam (smooth + reliable)
# cap = cv2.VideoCapture(0)
# prev_word = ""
# sentence = ""
# last_spoken_time = time.time()

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     img = cv2.flip(img, 1)
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     result = hands.process(img_rgb)

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:
#             mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             word = detect_word(hand_landmarks.landmark)

#             if word != "?" and word != prev_word and time.time() - last_spoken_time > 2:
#                 sentence += word + " "
#                 prev_word = word
#                 last_spoken_time = time.time()

#                 # Speak the word
#                 engine.say(word)
#                 engine.runAndWait()

#             cv2.putText(img, word, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

#     # Show full sentence
#     cv2.putText(img, sentence.strip(), (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#     cv2.imshow("Word Gesture Detection", img)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
