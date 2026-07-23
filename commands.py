"""
=========================================
RIN AI Voice Assistant
Smart Command Engine
Version : v3.0
Author  : Ravi Suthar
=========================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional
import re
import time

import wikipedia

from apps import get_app_name, open_app
from config import (
    GOODBYE,
    GREETING,
    UNKNOWN_COMMAND,
    WIKIPEDIA_ERROR,
    WIKIPEDIA_RESULT,
)
from data import app_commands, apps, folders, websites
from folders import open_folder
from system_controls import (
    handle_brightness_command,
    handle_media_command,
    handle_volume_command,
)
from system_info import (
    get_battery_status,
    get_cpu_usage,
    get_disk_usage,
    get_ram_usage,
)
from websites import open_website


@dataclass
class CommandResult:
    """
    Stores the result returned by RIN's command engine.

    response:
        Text that RIN should speak.

    should_exit:
        True when RIN should stop running.

    action:
        Optional function that runs after RIN speaks.
    """

    response: str
    should_exit: bool = False
    action: Optional[Callable[[], None]] = None


def normalize_command(command: str) -> str:
    """
    Cleans recognized speech while preserving important target names.

    Examples:
        "Can you open GitHub for me?"
        becomes:
        "open github"

        "Open RIN folder"
        remains:
        "open rin folder"
    """

    if not command:
        return ""

    text = command.lower().strip()

    # Remove punctuation.
    text = re.sub(r"[?,.!]", "", text)

    # Remove polite phrases only from the beginning.
    beginning_phrases = (
        "could you please ",
        "can you please ",
        "would you please ",
        "could you ",
        "can you ",
        "would you ",
        "please ",
    )

    for phrase in beginning_phrases:
        if text.startswith(phrase):
            text = text[len(phrase):].strip()
            break

    # Remove polite phrases only from the end.
    ending_phrases = (
        " for me please",
        " for me",
        " please",
    )

    for phrase in ending_phrases:
        if text.endswith(phrase):
            text = text[:-len(phrase)].strip()
            break

    # Remove repeated spaces.
    text = " ".join(text.split())

    return text


def convert_natural_command(command: str) -> str:
    """
    Converts common natural phrases into standard RIN commands.
    """

    natural_patterns = {
        # YouTube
        "i want to watch youtube": "open youtube",
        "i want to use youtube": "open youtube",
        "watch youtube": "open youtube",
        "play youtube": "open youtube",
        "show me youtube": "open youtube",

        # Browser
        "i want to browse the internet": "open chrome",
        "i want to use chrome": "open chrome",
        "browse the internet": "open chrome",
        "start chrome": "open chrome",

        # Notepad
        "i want to write something": "open notepad",
        "i need to write something": "open notepad",
        "let me write something": "open notepad",

        # Calculator
        "i want to calculate something": "open calculator",
        "i need a calculator": "open calculator",
        "show me calculator": "open calculator",

        # GitHub
        "show me github": "open github",
        "take me to github": "open github",
        "go to github": "open github",

        # ChatGPT
        "show me chatgpt": "open chatgpt",
        "take me to chatgpt": "open chatgpt",
        "go to chatgpt": "open chatgpt",
    }

    converted_command = natural_patterns.get(command, command)

    if converted_command != command:
        print("Natural command converted:", converted_command)

    return converted_command


def is_exit_command(text: str) -> bool:
    """
    Checks whether the user wants to close RIN.
    """

    exit_commands = {
        "goodbye",
        "good bye",
        "bye",
        "bye rin",
        "stop rin",
        "exit",
        "close rin",
        "shutdown rin",
        "go offline",
    }

    return text in exit_commands


def is_greeting_command(text: str) -> bool:
    """
    Checks whether the user is greeting RIN.
    """

    greeting_commands = {
        "hello",
        "hello rin",
        "hello buddy",
        "hello bud",
        "hi",
        "hi rin",
        "hi buddy",
        "hey",
        "hey rin",
        "hey buddy",
    }

    return text in greeting_commands


def get_wikipedia_response(text: str) -> str:
    """
    Searches Wikipedia and returns the best matching result.
    """

    topic = text

    search_prefixes = (
        "who is ",
        "what is ",
        "tell me about ",
        "search wikipedia for ",
    )

    for prefix in search_prefixes:
        if topic.startswith(prefix):
            topic = topic[len(prefix):].strip()
            break

    if not topic:
        return "Please tell me what you want to search for, buddy."

    print("Wikipedia topic:", topic)

    try:
        results = wikipedia.search(topic)

        if not results:
            return "Sorry buddy, I could not find anything."

        best_match = results[0]

        print("Wikipedia best match:", best_match)

        return WIKIPEDIA_RESULT.format(best_match)

    except wikipedia.exceptions.DisambiguationError as error:
        if error.options:
            best_match = error.options[0]
            return WIKIPEDIA_RESULT.format(best_match)

        return WIKIPEDIA_ERROR

    except wikipedia.exceptions.PageError:
        return "Sorry buddy, I could not find that Wikipedia page."

    except Exception as error:
        print("Wikipedia Error:", error)
        return WIKIPEDIA_ERROR


def create_open_action(target: str) -> Optional[Callable[[], None]]:
    """
    Creates an action for opening an app, folder, or website.
    """

    if target in folders:
        display_name, path = folders[target]

        def folder_action() -> None:
            time.sleep(0.5)
            open_folder(display_name, path)

        return folder_action

    if target in apps:
        display_name, command = apps[target]

        def app_action() -> None:
            time.sleep(0.5)
            open_app(display_name, command)

        return app_action

    if target in websites:
        display_name, url = websites[target]

        def website_action() -> None:
            time.sleep(0.5)
            open_website(display_name, url)

        return website_action

    return None


def get_open_command_result(text: str) -> CommandResult:
    """
    Finds and prepares the requested app, folder, or website.
    """

    target = get_app_name(text, apps, app_commands)

    print("Open-command target:", target)

    if target in folders:
        display_name, _ = folders[target]

    elif target in apps:
        display_name, _ = apps[target]

    elif target in websites:
        display_name, _ = websites[target]

    else:
        return CommandResult(
            response="Sorry buddy, I don't know how to open that yet."
        )

    action = create_open_action(target)

    if action is None:
        return CommandResult(
            response=f"Sorry buddy, I could not prepare {display_name}."
        )

    return CommandResult(
        response=f"Opening {display_name} buddy.",
        action=action,
    )


def process_command(raw_text: str) -> CommandResult:
    """
    Main command router for RIN.

    Flow:
        Raw speech
        → normalization
        → natural-language conversion
        → command detection
        → structured result
    """

    text = normalize_command(raw_text)
    text = convert_natural_command(text)

    print("Normalized command:", text)

    if not text:
        return CommandResult(
            response="Sorry buddy, I did not receive a command."
        )

    # Exit commands
    if is_exit_command(text):
        return CommandResult(
            response=GOODBYE,
            should_exit=True,
        )

    # Greetings
    if is_greeting_command(text):
        return CommandResult(response=GREETING)

    # Basic conversation
    if text in {
        "what is your name",
        "what's your name",
        "tell me your name",
    }:
        return CommandResult(response="My name is Rin.")

    if text in {
        "how are you",
        "how r u",
        "how are you doing",
    }:
        return CommandResult(
            response="I am doing great buddy."
        )

    # Time
    if text in {
        "what time is it",
        "current time",
        "tell me the time",
        "what is the time",
    }:
        current_time = datetime.now().strftime("%I:%M %p")

        return CommandResult(
            response=f"The current time is {current_time} buddy."
        )

    # Date
    if text in {
        "what is today's date",
        "what is todays date",
        "today's date",
        "todays date",
        "current date",
        "tell me the date",
    }:
        current_date = datetime.now().strftime("%d %B %Y")

        return CommandResult(
            response=f"Today's date is {current_date} buddy."
        )

    # System information
    if "battery" in text or "charge" in text:
        return CommandResult(
            response=get_battery_status()
        )

    if "cpu" in text or "processor" in text:
        return CommandResult(
            response=get_cpu_usage()
        )

    if "ram" in text or "memory usage" in text:
        return CommandResult(
            response=get_ram_usage()
        )

    if (
        "disk" in text
        or "storage" in text
        or "drive space" in text
        or "disk space" in text
    ):
        return CommandResult(
            response=get_disk_usage()
        )

    # Volume controls
    if (
        "volume" in text
        or text == "mute"
        or text == "unmute"
    ):
        return CommandResult(
            response=handle_volume_command(text)
        )

    # Brightness controls
    if "brightness" in text:
        return CommandResult(
            response=handle_brightness_command(text)
        )

    # Media controls
    media_commands = {
        "play music",
        "play media",
        "pause music",
        "pause media",
        "resume music",
        "resume media",
        "continue music",
        "next track",
        "next song",
        "next video",
        "previous track",
        "previous song",
        "previous video",
        "stop music",
        "stop media",
    }

    if text in media_commands:
        return CommandResult(
            response=handle_media_command(text)
        )

    # Apps, folders, and websites
    if any(text.startswith(command) for command in app_commands):
        return get_open_command_result(text)

    # Wikipedia
    wikipedia_prefixes = (
        "who is ",
        "what is ",
        "tell me about ",
        "search wikipedia for ",
    )

    if text.startswith(wikipedia_prefixes):
        return CommandResult(
            response=get_wikipedia_response(text)
        )

    return CommandResult(response=UNKNOWN_COMMAND)