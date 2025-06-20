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
    if states == [0, 0, 1, 1, 1]:
        return "Beautiful"
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
