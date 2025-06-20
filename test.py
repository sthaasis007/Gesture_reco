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

# def detect_word(landmarks):
#     states = get_finger_states(landmarks)

#     print(f"Finger States: {states}")
#     print(f"Wrist Y: {landmarks[0].y:.2f}, Index Y: {landmarks[8].y:.2f}")
#     print(f"Thumb tip X: {landmarks[4].x:.2f}, Thumb joint X: {landmarks[3].x:.2f}")

#     # STOP
#     if states == [1, 1, 1, 1, 1]:
#         return "Stop"

#     # YES
#     if states == [1, 0, 0, 0, 0]:
#         return "Yes"

#     # NO
#     if states == [0, 1, 0, 0, 0]:
#         return "No"

#     # HELLO = Open palm, thumb slightly spread
#     if states == [1, 1, 1, 1, 1] and abs(landmarks[4].x - landmarks[3].x) > 0.015:
#         return "Hello"

#     # THANKS = Hand raised (index finger above wrist)
#     if states == [1, 1, 1, 1, 1] and landmarks[8].y < landmarks[0].y:
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



# import cv2
# import mediapipe as mp
# import pyttsx3
# import time
# from collections import deque

# # Initialize
# engine = pyttsx3.init()
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_draw = mp.solutions.drawing_utils

# # History buffer for wrist X positions
# motion_history = deque(maxlen=15)  # store last 15 frames
# last_spoken_time = time.time()
# prev_word = ""
# sentence = ""

# cap = cv2.VideoCapture(0)

# # Add this in place of or inside detect_motion_gesture()

# def detect_motion_gesture(motion_history):
#     if len(motion_history) < 15:
#         return None

#     x_positions = [pos[0] for pos in motion_history]
#     y_positions = [pos[1] for pos in motion_history]

#     x_diff = max(x_positions) - min(x_positions)
#     y_diff = max(y_positions) - min(y_positions)

#     # Waving → Hello
#     if x_diff > 0.10:
#         return "Hello"

#     # Upward move → Thanks
#     if y_positions[0] - y_positions[-1] > 0.1:
#         return "Thanks"

#     return None


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

#             wrist = hand_landmarks.landmark[0]
#             motion_history.append((wrist.x, wrist.y))

#             gesture = detect_motion_gesture(motion_history)

#             if gesture and gesture != prev_word and time.time() - last_spoken_time > 2:
#                 prev_word = gesture
#                 sentence += gesture + " "
#                 last_spoken_time = time.time()
#                 engine.say(gesture)
#                 engine.runAndWait()

#             cv2.putText(img, gesture if gesture else "?", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

#     # Show sentence
#     cv2.putText(img, sentence.strip(), (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
#     cv2.imshow("Motion-Based Gesture Recognition", img)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# import cv2
# import mediapipe as mp
# import pyttsx3
# import time
# from collections import deque

# # Initialize TTS engine
# engine = pyttsx3.init()

# # Initialize MediaPipe
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# mp_draw = mp.solutions.drawing_utils

# # History buffer for wrist movement (X, Y)
# motion_history = deque(maxlen=15)

# # Finger state detection (1 = up, 0 = down)
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

# # Detect static gestures based on finger states
# def detect_finger_based_word(landmarks):
#     states = get_finger_states(landmarks)

#     if states == [1, 1, 1, 1, 1]:
#         return "Stop"
#     if states == [1, 0, 0, 0, 0]:
#         return "Yes"
#     if states == [0, 1, 0, 0, 0]:
#         return "No"

#     return None

# # Detect motion-based gestures
# def detect_motion_based_word(history):
#     if len(history) < 15:
#         return None

#     x_positions = [pos[0] for pos in history]
#     y_positions = [pos[1] for pos in history]

#     x_diff = max(x_positions) - min(x_positions)
#     y_diff = y_positions[0] - y_positions[-1]

#     if x_diff > 0.15:
#         return "Hello"
#     if y_diff > 0.1:
#         return "Thanks"

#     return None

# # Initialize camera
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
#     word = "?"

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:
#             mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             wrist = hand_landmarks.landmark[0]
#             motion_history.append((wrist.x, wrist.y))

#             # First try static finger-based
#             word = detect_finger_based_word(hand_landmarks.landmark)

#             # If not found, try motion-based
#             if not word:
#                 word = detect_motion_based_word(motion_history)

#             # Speak and record word
#             if word and word != prev_word and time.time() - last_spoken_time > 2:
#                 sentence += word + " "
#                 prev_word = word
#                 last_spoken_time = time.time()

#                 engine.say(word)
#                 engine.runAndWait()

#             cv2.putText(img, word, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

#     # Show sentence
#     cv2.putText(img, sentence.strip(), (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

#     cv2.imshow("Hybrid Gesture Recognition", img)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp
import pyttsx3
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize TTS engine
engine = pyttsx3.init()

def speak(word):
    def run():
        engine.say(word)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# MediaPipe init
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Detect finger states (1 = up, 0 = down)
def get_finger_states(landmarks):
    tips = [4, 8, 12, 16, 20]
    states = []
    # Thumb
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        states.append(1)
    else:
        states.append(0)
    # Other fingers
    for i in range(1, 5):
        if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
            states.append(1)
        else:
            states.append(0)
    return states

# Detect word from gesture
def detect_word(landmarks):
    states = get_finger_states(landmarks)
    if states == [0, 0, 0, 0, 0]:
        return "Stop"
    if states == [1, 0, 0, 0, 0]:
        return "Yes"
    if states == [0, 1, 0, 0, 0]:
        return "No"
    if states == [1, 1, 1, 1, 1]:
        return "Hello"
    if states == [0, 1, 1, 1, 0]:
        return "Thanks"
    if states == [0, 0, 1, 0, 0]:
        return "Goodbye"
    if states == [1, 1, 0, 0, 0]:
        return "You"
    if states == [1, 0, 0, 0, 1]:
        return "Are"
    if states == [0, 1, 0, 0, 1]:
        return "Fine"
    return "?"

class GestureApp:
    def __init__(self, root):
        self.root = root
        root.title("Gesture Recognition")

        self.video_running = False
        self.prev_word = ""
        self.sentence = ""
        self.last_spoken_time = 0

        # Tabs
        tab_control = ttk.Notebook(root)
        self.gesture_tab = ttk.Frame(tab_control)
        tab_control.add(self.gesture_tab, text="Gesture Recognition")
        tab_control.pack(expand=1, fill='both')

        # Start button
        self.start_btn = ttk.Button(self.gesture_tab, text="Start Recognition", command=self.start_video)
        self.start_btn.pack(pady=10)

        # Canvas for camera feed
        self.canvas = tk.Canvas(self.gesture_tab, width=640, height=480)
        self.canvas.pack()

        # Recognized word label
        self.word_label = ttk.Label(self.gesture_tab, text="Current Word: ", font=("Helvetica", 16))
        self.word_label.pack(pady=5)

        # Sentence label
        self.sentence_label = ttk.Label(self.gesture_tab, text="Sentence: ", font=("Helvetica", 14))
        self.sentence_label.pack(pady=5)

        # Clear sentence button
        self.clear_btn = ttk.Button(self.gesture_tab, text="Clear Sentence", command=self.clear_sentence)
        self.clear_btn.pack(pady=10)

        self.cap = None

    def clear_sentence(self):
        self.sentence = ""
        self.sentence_label.config(text="Sentence: ")

    def start_video(self):
        if not self.video_running:
            self.cap = cv2.VideoCapture(0)
            self.video_running = True
            self.start_btn.config(state='disabled')
            self.update_frame()

    def update_frame(self):
        if not self.video_running:
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            self.cap.release()
            self.video_running = False
            self.start_btn.config(state='normal')
            return

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        word = "?"
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                word = detect_word(hand_landmarks.landmark)

                if word != "?" and word != self.prev_word and (time.time() - self.last_spoken_time) > 2:
                    self.sentence += word + " "
                    self.prev_word = word
                    self.last_spoken_time = time.time()
                    speak(word)

        # Update GUI elements
        self.word_label.config(text=f"Current Word: {word}")
        self.sentence_label.config(text=f"Sentence: {self.sentence.strip()}")

        # Convert to ImageTk for displaying in Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor='nw', image=imgtk)

        # Repeat every 30 ms (~33 FPS)
        self.root.after(30, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()
