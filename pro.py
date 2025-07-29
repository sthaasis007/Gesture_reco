import cv2
import mediapipe as mp
import pyttsx3
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.font as font

# Initialize TTS engine
engine = pyttsx3.init()

def speak(word):
    def run():
        engine.say(word)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# MediaPipe init
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # ✅ allow two hands
mp_draw = mp.solutions.drawing_utils

def get_finger_states(landmarks):
    """
    Return list of finger states for one hand:
    Thumb, Index, Middle, Ring, Pinky (1=open, 0=closed)
    """
    tips = [4, 8, 12, 16, 20]
    states = []
    # Thumb: check x direction
    if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
        states.append(1)
    else:
        states.append(0)
    # Fingers: check y direction
    for i in range(1, 5):
        if landmarks[tips[i]].y < landmarks[tips[i] - 2].y:
            states.append(1)
        else:
            states.append(0)
    return states

def detect_word(states):
    """
    Map finger states to words.
    You can add more gestures here by defining unique patterns.
    """
    # Example dictionary of gestures
    if states == [0,0,0,0,0]: return "Stop"
    if states == [1,0,0,0,0]: return "Yes"
    if states == [0,1,0,0,0]: return "No"
    if states == [1,1,1,1,1]: return "Hello"
    if states == [0,1,1,1,0]: return "Thanks"
    if states == [0,0,1,0,0]: return "Goodbye"
    if states == [1,1,0,0,0]: return "You"
    if states == [1,0,0,0,1]: return "Are"
    if states == [0,1,0,0,1]: return "Fine"
    if states == [0,0,1,1,1]: return "Beautiful"
    if states == [1,1,0,1,0]: return "Love"
    if states == [0,1,1,0,0]: return "Happy"
    if states == [1,0,1,0,0]: return "Sad"
    if states == [1,1,1,0,0]: return "Run"
    if states == [1,1,0,1,1]: return "Walk"
    if states == [0,1,1,1,1]: return "Eat"
    if states == [1,0,1,1,1]: return "Drink"
    if states == [0,0,1,0,1]: return "Play"
    if states == [0,1,0,1,0]: return "Friend"
    if states == [1,0,1,0,1]: return "Home"
    return "?"

class GestureApp:
    def __init__(self, root):
        self.root = root
        root.title("Gesture Recognition")
        root.configure(bg='#eaf6fb')

        self.video_running = False
        self.prev_word = ""
        self.last_added_word = ""
        self.sentence = ""
        self.last_spoken_time = 0
        self.detected_consistently = 0
        self.required_consistency = 10

        self.custom_font = font.Font(family='Verdana', size=12)
        self.header_font = font.Font(family='Poppins', size=20, weight='bold')
        self.label_font = font.Font(family='Poppins', size=14)

        tab_control = ttk.Notebook(root)
        self.gesture_tab = tk.Frame(tab_control, bg='#eaf6fb')
        tab_control.add(self.gesture_tab, text="Gesture Recognition")
        tab_control.pack(expand=1, fill='both')

        header = tk.Label(self.gesture_tab, text="Sign Language to Speech Translator",
                          font=self.header_font, bg='#eaf6fb', fg='#013243')
        header.pack(pady=10)

        self.start_btn = tk.Button(self.gesture_tab, text="Start Recognition", command=self.start_video,
                                   bg="#2ecc71", fg="white", font=self.custom_font, relief="flat", padx=10, pady=5)
        self.start_btn.pack(pady=10)

        self.video_frame = tk.Frame(self.gesture_tab, bg='black', highlightbackground="gray", highlightthickness=1)
        self.video_frame.pack(pady=5)
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480)
        self.canvas.pack()

        self.word_label = tk.Label(self.gesture_tab, text="Current Word: ?", font=self.label_font,
                                   bg='#eaf6fb', fg='#34495e')
        self.word_label.pack(pady=5)

        self.sentence_label = tk.Label(self.gesture_tab, text="Sentence:", font=self.label_font,
                                       bg='#eaf6fb', fg='#34495e')
        self.sentence_label.pack(pady=5)

        self.clear_btn = tk.Button(self.gesture_tab, text="Clear Sentence", command=self.clear_sentence,
                                   bg="#e74c3c", fg="white", font=self.custom_font, relief="flat", padx=10, pady=5)
        self.clear_btn.pack(pady=10)

        self.cap = None

    def clear_sentence(self):
        self.sentence = ""
        self.sentence_label.config(text="Sentence:")

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
            combined_states = []
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                states = get_finger_states(hand_landmarks.landmark)
                w = detect_word(states)
                if w != "?":
                    combined_states.append(w)

            # Combine detected words from both hands if needed
            if len(combined_states) == 2:
                # Example of special two-hand gesture:
                if ("Hello" in combined_states and "Hello" in combined_states):
                    word = "Namaste"
                else:
                    # else just take first detected
                    word = combined_states[0]
            elif len(combined_states) == 1:
                word = combined_states[0]

            # Sentence construction
            if word != "?" and word != self.last_added_word:
                if word == self.prev_word:
                    self.detected_consistently += 1
                else:
                    self.detected_consistently = 1
                    self.prev_word = word

                if self.detected_consistently == self.required_consistency:
                    self.sentence += word + " "
                    speak(word)
                    self.last_added_word = word
                    self.detected_consistently = 0
            elif word == "?":
                self.prev_word = ""
                self.detected_consistently = 0

        self.word_label.config(text=f"Current Word: {word}")
        self.sentence_label.config(text=f"Sentence: {self.sentence.strip()}")

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor='nw', image=imgtk)

        self.root.after(30, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()
