from apps import open_app, get_app_name
from websites import open_website, get_website_name
from folders import open_folder
from data import websites, folders, website_commands, apps, app_commands
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia


engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    if "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening...")

    recognizer.adjust_for_ambient_noise(source, duration=1)

    audio = recognizer.listen(source)

    print("Processing...")

    try:
        text = recognizer.recognize_google(audio, language="en-IN")

        text = text.lower()

        print("You said:", text)

        if "hello buddy" in text or "hello bud" in text:
            speak("Hello buddy. How can I help you?")

        elif "what is your name" in text:
            speak("My name is Rin.")

        elif "how are you" in text or "how r u" in text:
            speak("I am doing great buddy.")

        elif "goodbye" in text:
            speak("See you later buddy.")

        elif any(text.startswith(cmd) for cmd in app_commands):

            app = get_app_name(
                text,
                apps,
                app_commands
            )

            print("App:", app)

            if app in apps:
                name, command = apps[app]

                speak(f"Opening {name} buddy.")

                open_app(name, command)

            else:
                speak("Sorry buddy, I don't know that application.")

        elif "what time is it" in text:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time} buddy.")

        elif "what is today's date" in text:
            current_date = datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {current_date} buddy.")

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
        
        elif "open rin folder" in text:
            name, path = folders["rin folder"]
            open_folder(name, path)

        elif any(text.startswith(cmd) for cmd in website_commands):
            website = get_website_name(text, websites, website_commands)

            print("Website:", website)

            if website in websites:
                name, url = websites[website]
                speak(f"Opening {name} buddy.")
                open_website(name, url)
            else:
                speak("Sorry buddy, I don't know that website.")
        
    except:
        speak("Sorry buddy, I could not understand.")