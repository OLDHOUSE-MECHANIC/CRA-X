import os
import json
import time
import openai
import speech_recognition as sr
import pyttsx3
from pathlib import Path

# --------------------------- Configuration ---------------------------
KEYWORDS_FILE = Path("keywords.json")
PREDEFINED_KEYWORDS = [
    "music", "video", "volume", "pause", "play",
    "lights", "temperature", "fan", "lock", "alarm",
    "appliances", "open app", "shutdown", "screenshot", "search",
    "file", "reminder", "calendar", "email", "message", "note",
    "weather", "news", "time", "date", "joke", "trivia", "quote",
    "game", "conversation", "goodbye", "status"
]

# Make sure you set your OpenAI API key in the environment
openai.api_key = os.getenv("2344321")
if not openai.api_key:
    raise RuntimeError("Please set OPENAI_API_KEY environment variable before running.")

# TTS Engine
tts_engine = pyttsx3.init()

# Speech recognizer
recognizer = sr.Recognizer()

# --------------------------- Keyword Storage ---------------------------

def load_keywords():
    keywords = set(k.lower() for k in PREDEFINED_KEYWORDS)
    if KEYWORDS_FILE.exists():
        try:
            with KEYWORDS_FILE.open("r", encoding="utf-8") as f:
                saved = json.load(f)
                for k in saved:
                    keywords.add(k.lower())
        except Exception as e:
            print(f"Warning: couldn't read {KEYWORDS_FILE}: {e}")
    return keywords


def save_new_keyword(keyword):
    """Append a newly discovered keyword to disk (if it's not already present)."""
    keyword = keyword.strip().lower()
    if not keyword:
        return

    data = []
    if KEYWORDS_FILE.exists():
        try:
            with KEYWORDS_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

    if keyword not in (k.lower() for k in data):
        data.append(keyword)
        with KEYWORDS_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved new keyword: {keyword}")

# --------------------------- Helpers: TTS & Speech ---------------------------

def speak(text, wait=True):
    """Speak text via pyttsx3."""
    if not text:
        return
    tts_engine.say(text)
    if wait:
        tts_engine.runAndWait()


def recognize_speech(timeout=None, phrase_time_limit=None):
    """Listen on the default microphone and return recognized text (or None).

    Args:
        timeout: seconds to wait for phrase to start
        phrase_time_limit: seconds of maximum phrase length
    """
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return None

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Heard: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, couldn't understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition service error: {e}")
        return None

# --------------------------- OpenAI Interaction ---------------------------

def build_prompt_for_keyword_extraction(user_text, current_keywords):
    """Build a focused prompt listing known keywords and asking the model to return one.

    The prompt instructs the model to return exactly one of the known keywords if it matches
    or to propose a short single-word new keyword using the format: NEW:<keyword>
    """
    known = ", ".join(sorted(current_keywords))
    prompt = (
        "You are an intent extraction assistant.\n"
        "Below is a list of known command keywords:\n"
        f"{known}\n\n"
        "Given the user's command, return **exactly one** token:":
        "either one of the known keywords (exactly) if the user's intent matches it,\n"
        "or if no known keyword applies, suggest a concise new keyword using the exact format: NEW:<single_word_keyword>.\n"
        "Do not include any extra words, explanation, or punctuation. Always respond in lowercase.\n\n"
        f"User command: {user_text}\n"
        "Return:" 
    )
    return prompt


def get_keyword_from_gpt(user_text, current_keywords, max_tokens=10):
    """Call OpenAI to extract or suggest a keyword."""
    prompt = build_prompt_for_keyword_extraction(user_text, current_keywords)

    try:
        resp = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.0,
            n=1,
            stop=None
        )
        raw = resp.choices[0].text.strip().lower()
        print(f"OpenAI returned: '{raw}'")

        if raw.startswith("new:"):
            suggestion = raw.split("new:", 1)[1].strip()
            # sanitize suggestion to a single word
            suggestion = suggestion.split()[0]
            return ("new", suggestion)
        else:
            # assume it's a known keyword (or something close). Normalize whitespace
            return ("known", raw)

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return ("error", None)


def get_dynamic_response_for_keyword(keyword):
    """Ask OpenAI for a short friendly line to say after performing a keyword action."""
    prompt = f"Say a short friendly line when the assistant performs '{keyword}'. Keep it under 12 words."
    try:
        resp = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=20,
            temperature=0.7,
            n=1
        )
        return resp.choices[0].text.strip()
    except Exception as e:
        print(f"Error getting dynamic response: {e}")
        return "Done."

# --------------------------- Action Mapping ---------------------------

# Define placeholder action functions — replace bodies with your implementation

def action_music(command_text=None):
    print("(placeholder) action: play music")
    # TODO: implement actual music-playing logic (e.g., call Spotify API, launch player, etc.)


def action_video(command_text=None):
    print("(placeholder) action: play video")


def action_volume(command_text=None):
    print("(placeholder) action: change volume")


def action_unknown(command_text=None):
    print("(placeholder) action: unknown task — no action executed")

# Map keywords to functions
ACTION_MAP = {
    "music": action_music,
    "video": action_video,
    "volume": action_volume,
    # add more mappings here
}

# --------------------------- Main Loop ---------------------------

def main(listen_timeout=None, phrase_time_limit=8):
    keywords = load_keywords()
    print(f"Loaded keywords ({len(keywords)}): {sorted(list(keywords))}")

    speak("CRA-X ready. Say a command or say 'stop listening' to quit.")

    try:
        while True:
            user_text = recognize_speech(timeout=listen_timeout, phrase_time_limit=phrase_time_limit)
            if not user_text:
                # nothing recognized — continue
                continue

            lower = user_text.strip().lower()
            if any(term in lower for term in ("stop listening", "stop", "exit", "quit")):
                speak("Goodbye!")
                print("Exiting main loop.")
                break

            # Query OpenAI for a keyword
            mode, result = get_keyword_from_gpt(user_text, keywords)
            if mode == "error":
                speak("I had trouble understanding. Try again.")
                continue

            if mode == "new" and result:
                # add to keywords and save
                print(f"Discovered new keyword suggestion: {result}")
                keywords.add(result)
                save_new_keyword(result)
                # After saving a new keyword, treat it as known and proceed
                keyword = result
            else:
                keyword = result

            if not keyword:
                speak("Sorry, I couldn't determine the task.")
                continue

            # Perform the mapped action if available
            action = ACTION_MAP.get(keyword, action_unknown)
            try:
                action(user_text)
            except Exception as e:
                print(f"Error executing action for '{keyword}': {e}")

            # Get a short dynamic line for the user and speak it
            line = get_dynamic_response_for_keyword(keyword)
            print(f"Assistant: {line}")
            speak(line)

            # Small delay to avoid immediate re-triggering
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Interrupted by user — exiting.")
        speak("Shutting down. Goodbye.")


if __name__ == "__main__":
    main()
