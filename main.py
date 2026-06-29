from apps import open_app
from websites import open_website
from folders import open_folder
from data import websites
from data import folders
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

        elif "open notepad" in text:
            open_app("Notepad", "notepad")

        elif "open calculator" in text:
            open_app("Calculator", "calc")
        
        elif "open paint" in text:
            open_app("Paint", "mspaint")
        
        elif "open chrome" in text:
            open_app("Google Chrome","chrome")

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

        elif text.startswith("open "):
            website = text.replace("open ", "").strip()

            print("Website name:", website)

            if website in websites:
                name, url = websites[website]
                open_website(name, url)
            else:
                speak("Sorry buddy, I do not know that website.")
        
        else:
            speak("Sorry buddy, I do not know that command.")

    except:
        speak("Sorry buddy, I could not understand.")