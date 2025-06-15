
import cv2
from deepface import DeepFace
import pygame
import tkinter as tk
from tkinter import messagebox
import threading

# Emotion to music mapping
emotion_music_map = {
    'happy': 'music/happy_song.mp3',
    'sad': 'music/sad_song.mp3',
    'angry': 'music/angry_song.mp3',
    'neutral': 'music/neutral_song.mp3',
    'surprise': 'music/surprise_song.mp3',
    'fear': 'music/fear_song.mp3',
    'disgust': 'music/disgust_song.mp3'
}

# Initialize pygame mixer
pygame.mixer.init()

def detect_emotion_and_play():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Failed to capture image from webcam.")
        return

    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        messagebox.showinfo("Detected Emotion", f"Emotion: {dominant_emotion}")

        music_file = emotion_music_map.get(dominant_emotion, emotion_music_map['neutral'])
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

    except Exception as e:
        messagebox.showerror("Error", f"Emotion detection failed: {str(e)}")

def stop_music():
    pygame.mixer.music.stop()

# GUI setup
app = tk.Tk()
app.title("Mood-Based Music Recommender")
app.geometry("300x200")

start_btn = tk.Button(app, text="Detect Mood & Play Music", command=lambda: threading.Thread(target=detect_emotion_and_play).start())
start_btn.pack(pady=20)

stop_btn = tk.Button(app, text="Stop Music", command=stop_music)
stop_btn.pack(pady=10)

app.mainloop()
