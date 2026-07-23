"""
=========================================
RIN AI Voice Assistant
Main Application
Version : v3.0
Author  : Ravi Suthar
=========================================
"""

import pyttsx3
import speech_recognition as sr

from commands import process_command
from config import (
    AMBIENT_NOISE_DURATION,
    ERROR_RESPONSE,
    LANGUAGE,
    NOT_UNDERSTOOD,
    VOICE_NAME,
)


def speak(text: str) -> None:
    """
    Prints and speaks RIN's response.

    A fresh pyttsx3 engine is created for each response because
    reusing one engine can sometimes stop speaking on Windows.
    """

    if not text:
        return

    print("RIN:", text)

    try:
        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        for voice in voices:
            if VOICE_NAME.lower() in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as error:
        print("TTS Error:", error)


def listen(recognizer: sr.Recognizer) -> str:
    """
    Listens through the microphone and converts speech into text.
    """

    with sr.Microphone() as source:
        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=AMBIENT_NOISE_DURATION,
        )

        audio = recognizer.listen(source)

        print("Processing...")

    recognized_text = recognizer.recognize_google(
        audio,
        language=LANGUAGE,
    )

    recognized_text = recognized_text.lower().strip()

    print("You said:", recognized_text)

    return recognized_text


def run_rin() -> None:
    """
    Starts RIN's main voice-assistant loop.
    """

    recognizer = sr.Recognizer()

    print("=" * 50)
    print("RIN AI Voice Assistant v3.0")
    print("Smart Command Engine")
    print("=" * 50)

    while True:
        try:
            user_command = listen(recognizer)

            result = process_command(user_command)

            speak(result.response)

            if result.action is not None:
                try:
                    result.action()

                except Exception as action_error:
                    print("Action Error:", action_error)
                    speak(
                        "Sorry buddy, I could not complete that action."
                    )

            if result.should_exit:
                break

        except sr.UnknownValueError:
            speak(NOT_UNDERSTOOD)

        except sr.RequestError as error:
            print("Speech API Error:", error)

            speak(
                "Sorry buddy, my speech service is not responding."
            )

        except KeyboardInterrupt:
            print("\nRIN stopped from the keyboard.")
            speak("RIN is going offline. Goodbye buddy.")
            break

        except Exception as error:
            print("Main Error:", error)
            speak(ERROR_RESPONSE)


if __name__ == "__main__":
    run_rin()