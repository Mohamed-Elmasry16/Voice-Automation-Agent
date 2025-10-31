# 🎙️ Voice Booking Assistant

## Project Overview
The Voice Booking Assistant is a Python-based voice automation agent that allows users to interact using voice commands to manage their calendar. Users can:
- List upcoming calendar events.
- Book new appointments.
- Cancel existing appointments.

The assistant uses OpenAI GPT-5 for natural language understanding, Google Calendar API for scheduling, and speech recognition for voice input. It also provides a modern, interactive GUI built with CustomTkinter.

## Demo Video
Watch a short demonstration of the assistant in action:  
[Insert your 5-minute video link here](YOUR_VIDEO_LINK_HERE)

## Features
- Voice input with short recording window for responsiveness.
- Text-to-speech responses using gTTS and pygame.
- Google Calendar integration for managing real events.
- Dynamic GUI that shows conversation in a WhatsApp-style chat.
- Natural language understanding using GPT-5.
- Handles greetings, self-introduction, and exit commands.

## Example Voice Commands
- "Show my meetings for this week."
- "Book a meeting with John tomorrow at 10 AM."
- "Cancel my dentist appointment."
- "Who are you?"
- "Bye"

## Project structure

- `voice-automation-agent/`
  - `voice_booking_assistant.py` — GUI and voice interface
  - `model.py` — Voice processing & command handling
  - `analyzer.py` — GPT-5 command analyzer
  - `test_calendar.py` — Google Calendar integration
  - `credentials.json` — Google Calendar credentials
  - `token.json` — Generated OAuth token
  - `requirements.txt` — Python dependencies
  - `README.md` — Project documentation



