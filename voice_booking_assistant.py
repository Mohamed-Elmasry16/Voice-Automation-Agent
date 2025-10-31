import customtkinter as ctk
from customtkinter import CTkScrollableFrame
import threading
from model import process_voice_command  # your voice assistant model

# ---------- GUI Setup ----------
ctk.set_appearance_mode("System")  # "Dark" or "Light"
ctk.set_default_color_theme("blue")  # or any built-in theme

class VoiceAssistantUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎙️ Voice Booking Assistant")
        self.geometry("500x600")
        self.resizable(False, False)

        # Header
        self.header = ctk.CTkLabel(self, text="Voice Booking Assistant", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.pack(pady=10)

        # Chat frame
        self.chat_frame = CTkScrollableFrame(self, width=480, height=450)
        self.chat_frame.pack(padx=10, pady=10)

        # Speak button
        self.record_btn = ctk.CTkButton(self, text="🎤 Speak Now", font=ctk.CTkFont(size=14),
                                        command=self.start_recording)
        self.record_btn.pack(pady=10)

    # ---------- Add message ----------
    def add_message(self, sender, text):
        """Add a message bubble to the chat."""
        bubble_color = "#4CAF50" if sender == "You" else "#1e90ff"
        text_color = "white"
        justify = "right" if sender == "You" else "left"
        anchor = "e" if sender == "You" else "w"

        msg_label = ctk.CTkLabel(self.chat_frame, text=text, wraplength=350,
                                 fg_color=bubble_color, text_color=text_color,
                                 corner_radius=15, anchor="w", justify=justify,
                                 font=ctk.CTkFont(size=12))
        msg_label.pack(padx=10, pady=5, anchor=anchor)

        # Scroll to bottom
        self.chat_frame.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    # ---------- Handle button ----------
    def start_recording(self):
        self.add_message("You", "🎙️ Listening...")
        threading.Thread(target=self.handle_command, daemon=True).start()

    def handle_command(self):
        response = process_voice_command()  # this calls your model.py
        self.add_message("Assistant", response)


if __name__ == "__main__":
    app = VoiceAssistantUI()
    app.mainloop()
