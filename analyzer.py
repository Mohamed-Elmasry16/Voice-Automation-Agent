from openai import OpenAI
import json

client = OpenAI(
    api_key="openai key"
)

def analyze_command(user_text):
    """Analyze the user's text and decide which calendar action to perform."""
    user_text_lower = user_text.lower().strip()

    # --- Local quick checks (faster and cheaper than calling GPT) ---
    if any(q in user_text_lower for q in ["who are you", "what can you do", "introduce yourself"]):
        return {"action": "self_intro"}

    elif any(g in user_text_lower for g in ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]):
        return {"action": "greet"}

    elif any(x in user_text_lower for x in ["exit", "quit", "bye", "goodbye"]):
        return {"action": "exit"}

    # --- Otherwise, let GPT decide the structured intent ---
    prompt = f"""
    You are a smart voice assistant that helps manage Google Calendar events.
    Understand the user's text and decide what action to take.

    Possible actions:
      - greet
      - self_intro
      - list_events
      - add_event
      - cancel_event
      - exit

    Return ONLY JSON in this format:
    {{
      "action": "string",
      "summary": "string or null",
      "start": "ISO datetime or null",
      "end": "ISO datetime or null"
    }}

    Be concise and never include any explanation or natural text outside JSON.

    Examples:
    Input: "Book a meeting with John tomorrow at 10am"
    Output: {{"action": "add_event", "summary": "Meeting with John", "start": "2025-11-01T10:00:00", "end": "2025-11-01T11:00:00"}}

    Input: "Show my next meetings"
    Output: {{"action": "list_events"}}

    Input: "Cancel my dentist appointment"
    Output: {{"action": "cancel_event", "summary": "Dentist appointment"}}

    Input: "Exit"
    Output: {{"action": "exit"}}

    User said: "{user_text}"
    """

    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )

        result = response.output_text.strip()
        print("🧠 AI Output:", result)

        # Try to parse structured response
        parsed = json.loads(result)
        if "action" not in parsed:
            return {"action": "unknown"}
        return parsed

    except Exception as e:
        print("⚠️ Error in analyze_command:", e)
        return {"action": "unknown"}
