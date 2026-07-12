from datetime import datetime
import time

import pyttsx3
import speech_recognition as sr
import wikipedia

from apps import open_app, get_app_name
from folders import open_folder
from websites import open_website
from data import websites, folders, apps, app_commands
from system_info import (
    get_battery_status,
    get_cpu_usage,
    get_ram_usage,
    get_disk_usage,
)


def speak(text):
    """Make RIN speak using the Windows Zira voice when available."""
    print("RIN:", text)

    try:
        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        for voice in voices:
            if "zira" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        engine.say(text)
        engine.runAndWait()

    except Exception as error:
        print("TTS Error:", error)


recognizer = sr.Recognizer()


while True:

    try:
        with sr.Microphone() as source:
            print("Listening...")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(source)

            print("Processing...")

        text = recognizer.recognize_google(
            audio,
            language="en-IN",
        ).lower()

        print("You said:", text)

        # -------------------------
        # Exit Commands
        # -------------------------

        if (
            "goodbye" in text
            or "good bye" in text
            or "stop rin" in text
            or text == "exit"
        ):
            speak("Goodbye buddy. RIN is going offline.")
            break

        # -------------------------
        # Basic Conversation
        # -------------------------

        elif (
            "hello buddy" in text
            or "hello bud" in text
            or text == "hello"
        ):
            speak("Hello buddy. How can I help you?")

        elif "what is your name" in text:
            speak("My name is RIN.")

        elif "how are you" in text or "how r u" in text:
            speak("I am doing great buddy.")

        # -------------------------
        # Date and Time
        # -------------------------

        elif "what time is it" in text or "current time" in text:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time} buddy.")

        elif "today's date" in text or "current date" in text:
            current_date = datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {current_date} buddy.")

        # -------------------------
        # System Information
        # -------------------------

        elif "battery" in text or "charge" in text:
            speak(get_battery_status())

        elif "cpu" in text or "processor" in text:
            speak(get_cpu_usage())

        elif "ram" in text or "memory" in text:
            speak(get_ram_usage())

        elif (
            "disk" in text
            or "storage" in text
            or "drive space" in text
            or "free space" in text
        ):
            speak(get_disk_usage())

        # -------------------------
        # Wikipedia Search
        # -------------------------

        elif "who is" in text or "what is" in text:

            topic = (
                text.replace("who is", "")
                .replace("what is", "")
                .strip()
            )

            print("Topic:", topic)

            if not topic:
                speak("Please tell me what you want to search for.")
                continue

            try:
                results = wikipedia.search(topic)

                if results:
                    best_match = results[0]

                    print("Best match:", best_match)

                    speak(
                        f"I found {best_match} "
                        "on Wikipedia buddy."
                    )

                else:
                    speak(
                        "Sorry buddy, "
                        "I could not find anything."
                    )

            except Exception as error:
                print("Wikipedia Error:", error)

                speak(
                    "Sorry buddy, Wikipedia "
                    "is not responding right now."
                )

        # -------------------------
        # Apps, Folders, Websites
        # -------------------------

        elif any(
            text.startswith(command)
            for command in app_commands
        ):

            target = get_app_name(
                text,
                apps,
                app_commands,
            )

            print("Target:", target)

            if target in folders:
                name, path = folders[target]

                speak(f"Opening {name} buddy.")
                time.sleep(0.3)

                open_folder(name, path)

            elif target in apps:
                name, command = apps[target]

                speak(f"Opening {name} buddy.")
                time.sleep(0.3)

                open_app(name, command)

            elif target in websites:
                name, url = websites[target]

                speak(f"Opening {name} buddy.")
                time.sleep(0.3)

                open_website(name, url)

            else:
                speak(
                    "Sorry buddy, "
                    "I don't know that yet."
                )

        else:
            speak(
                "Sorry buddy, "
                "I do not know that command."
            )

    except sr.UnknownValueError:
        speak(
            "Sorry buddy, "
            "I could not understand."
        )

    except sr.RequestError as error:
        print("Speech API Error:", error)

        speak(
            "Sorry buddy, my speech "
            "service is not responding."
        )

    except KeyboardInterrupt:
        print("\nRIN stopped manually.")
        break

    except Exception as error:
        print("Main Error:", error)

        speak(
            "Sorry buddy, "
            "something went wrong."
        )
