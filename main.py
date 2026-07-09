from apps import open_app, get_app_name
from websites import open_website, get_website_name
from folders import open_folder, get_folder_name
from data import websites, folders, website_commands, apps, app_commands, folder_commands
import speech_recognition as sr
import pyttsx3
import time
from datetime import datetime
import wikipedia
from system_info import (
    get_battery_status,
    get_cpu_usage,
    get_ram_usage,
    get_disk_usage
)


def speak(text):
    print("RIN:", text)

    try:
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        for voice in voices:
            if "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print("TTS Error:", e)

recognizer = sr.Recognizer()

while True:

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

        print("Processing...")

    try:
        text = recognizer.recognize_google(audio, language="en-IN")

        text = text.lower()

        print("You said:", text)

        if "goodbye" in text or "good bye" in text or "stop rin" in text or "exit" in text:
            speak("Goodbye buddy. RIN is going offline.")
            break

        elif "hello buddy" in text or "hello bud" in text:
            speak("Hello buddy. How can I help you?")

        elif "what is your name" in text:
            speak("My name is Rin.")

        elif "how are you" in text or "how r u" in text:
            speak("I am doing great buddy.")

        elif "what time is it" in text:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time} buddy.")

        elif "what is today's date" in text:
            current_date = datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {current_date} buddy.")
        
        elif "battery" in text or "charge" in text:
            speak(get_battery_status())

        elif "cpu" in text or "processor" in text:
            speak(get_cpu_usage())

        elif "ram" in text or "memory" in text:
            speak(get_ram_usage())

        elif "disk" in text or "storage" in text or "drive" in text or "space" in text or "usage" in text:
            speak(get_disk_usage())

        elif "who is" in text or "what is" in text:

            topic = text.replace("who is", "").replace("what is", "").strip()

            print("Topic:", topic)

            try:
                results = wikipedia.search(topic)

                if len(results) > 0:

                    best_match = results[0]

                    speak(f"I found {best_match} on Wikipedia buddy.")

                    print("Best match:", best_match)

                else:
                    speak("Sorry buddy, I could not find anything.")

            except Exception as e:

                print("Wikipedia Error:", e)

                speak("Sorry buddy, Wikipedia is not responding right now.")
        
        elif any(text.startswith(cmd) for cmd in app_commands):

            target = get_app_name(text, apps, app_commands)

            print("Target:", target)

            if target in folders:
                name, path = folders[target]
                speak(f"Opening {name} buddy.")
                time.sleep(0.5)
                open_folder(name, path)

            elif target in apps:
                name, command = apps[target]
                speak(f"Opening {name} buddy.")
                time.sleep(0.5)
                open_app(name, command)

            elif target in websites:
                name, url = websites[target]
                speak(f"Opening {name} buddy.")
                time.sleep(0.5)
                open_website(name, url)

            else:
                speak("Sorry buddy, I don't know that yet.")
        
        else:
            speak("Sorry buddy, I do not know that command.")

    except sr.UnknownValueError:
        speak("Sorry buddy, I could not understand.")

    except sr.RequestError as e:
        print("Speech API Error:", e)
        speak("Sorry buddy, my speech service is not responding.")

    except Exception as e:
        print("Main Error:", e)
        speak("Sorry buddy, something went wrong.")