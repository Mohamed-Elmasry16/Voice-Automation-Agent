import speech_recognition as sr
from gtts import gTTS
import pygame, os, time
from analyzer import analyze_command
from test_calendar import get_upcoming_events, add_event, delete_event
import sounddevice as sd
import numpy as np

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        file = "tmp.mp3"
        tts.save(file)

        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.5)

        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(file)
    except Exception as e:
        print("Audio playback error:", e)
        if os.path.exists("tmp.mp3"):
            os.remove("tmp.mp3")



def listen():
    """Capture voice input using sounddevice instead of PyAudio."""
    recognizer = sr.Recognizer()

    # Record audio from the default microphone
    duration = 7 # seconds to record
    sample_rate = 16000  # sample rate for recording

    print("🎤 Listening... (please speak now)")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    # Convert the raw audio data into a format that SpeechRecognition can use
    audio = sr.AudioData(audio_data.tobytes(), sample_rate, 2)

    try:
        # Use Google’s free speech recognition API
        text = recognizer.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn’t understand your speech.")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
        return ""


def process_voice_command():
    command = listen()
    data = analyze_command(command)
    action = data.get("action")

    if action == "list_events":
        events = get_upcoming_events()
        speak(events)
        return events

    elif action == "add_event":
        if data.get("summary") and data.get("start") and data.get("end"):
            msg = add_event(data["summary"], data["start"], data["end"])
            speak(msg)
            return msg
        else:
            msg = "I need more details to book that event."
            speak(msg)
            return msg

    elif action == "cancel_event":
        summary = data.get("summary")
        if summary:
            msg = delete_event(summary)
            speak(msg)
            return msg
        else:
            msg = "Please tell me which event to cancel."
            speak(msg)
            return msg

    elif action == "self_intro":
        intro = ("I am your Booking Assistant. "
                 "I can list, book, and cancel events for you.")
        speak(intro)
        return intro

    elif action == "greet":
        greeting = "Hi! How can I help you today?"
        speak(greeting)
        return greeting

    elif action == "exit":
        bye = "Goodbye!"
        speak(bye)
        return bye

    else:
        msg = "Sorry, I didn’t understand."
        speak(msg)
        return msg
