import re
from pycaw.pycaw import AudioUtilities
import screen_brightness_control as sbc
import pyautogui


def get_audio_endpoint():
    """Return the Windows master audio endpoint."""
    device = AudioUtilities.GetSpeakers()
    return device.EndpointVolume


def get_volume():
    """Return the current Windows master volume percentage."""
    volume = get_audio_endpoint()
    current_level = volume.GetMasterVolumeLevelScalar()

    return round(current_level * 100)


def set_volume(percent):
    """Set the Windows master volume to an exact percentage."""
    percent = int(percent)

    if percent < 0 or percent > 100:
        return "Volume must be between 0 and 100 percent, buddy."

    volume = get_audio_endpoint()
    volume.SetMasterVolumeLevelScalar(percent / 100, None)

    return f"Volume set to {percent} percent buddy."


def volume_up(amount=10):
    """Increase volume by the requested percentage."""
    amount = abs(int(amount))
    current = get_volume()
    new_volume = min(current + amount, 100)

    volume = get_audio_endpoint()
    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)

    return (
        f"Volume increased by {amount} percent. "
        f"Current volume is {new_volume} percent buddy."
    )


def volume_down(amount=10):
    """Decrease volume by the requested percentage."""
    amount = abs(int(amount))
    current = get_volume()
    new_volume = max(current - amount, 0)

    volume = get_audio_endpoint()
    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)

    return (
        f"Volume decreased by {amount} percent. "
        f"Current volume is {new_volume} percent buddy."
    )


def volume_mute():
    """Mute Windows audio."""
    volume = get_audio_endpoint()
    volume.SetMute(1, None)

    return "Volume muted buddy."


def volume_unmute():
    """Unmute Windows audio."""
    volume = get_audio_endpoint()
    volume.SetMute(0, None)

    return "Volume unmuted buddy."


def handle_volume_command(text):
    """Understand natural-language volume commands."""
    command = text.lower().strip()
    numbers = re.findall(r"\d+", command)
    amount = int(numbers[0]) if numbers else None

    if "unmute" in command:
        return volume_unmute()

    if "mute" in command:
        return volume_mute()

    if (
        "current volume" in command
        or "what is my volume" in command
        or "what's my volume" in command
        or "volume status" in command
    ):
        return f"Current volume is {get_volume()} percent buddy."

    if "set volume" in command:
        if amount is None:
            return "Please tell me the volume percentage buddy."

        return set_volume(amount)

    if (
        "volume up" in command
        or "increase volume" in command
        or "raise volume" in command
        or "turn volume up" in command
    ):
        return volume_up(amount if amount is not None else 10)

    if (
        "volume down" in command
        or "decrease volume" in command
        or "lower volume" in command
        or "turn volume down" in command
    ):
        return volume_down(amount if amount is not None else 10)

    return "Sorry buddy, I could not understand the volume command."

# =========================================================
# BRIGHTNESS CONTROLS
# =========================================================

def get_brightness():
    """Return the current brightness percentage."""

    try:
        brightness_values = sbc.get_brightness()

        if not brightness_values:
            return None

        return round(brightness_values[0])

    except Exception as error:
        print(f"Brightness read error: {error}")
        return None


def set_brightness(percent):
    """Set brightness between 0 and 100 percent."""

    try:
        percent = int(percent)

        if percent < 0 or percent > 100:
            return "Brightness must be between 0 and 100 percent, buddy."

        sbc.set_brightness(percent)

        return f"Brightness has been set to {percent} percent."

    except Exception as error:
        print(f"Brightness set error: {error}")
        return "Sorry buddy, I could not change the brightness."


def brightness_up(amount=10):
    """Increase brightness by the given percentage."""

    try:
        current = get_brightness()

        if current is None:
            return "Sorry buddy, I could not detect the current brightness."

        amount = abs(int(amount))
        new_brightness = min(current + amount, 100)

        sbc.set_brightness(new_brightness)

        if current == 100:
            return "Brightness is already at 100 percent, buddy."

        return (
            f"Brightness increased by {amount} percent. "
            f"Current brightness is {new_brightness} percent."
        )

    except Exception as error:
        print(f"Brightness increase error: {error}")
        return "Sorry buddy, I could not increase the brightness."


def brightness_down(amount=10):
    """Decrease brightness by the given percentage."""

    try:
        current = get_brightness()

        if current is None:
            return "Sorry buddy, I could not detect the current brightness."

        amount = abs(int(amount))
        new_brightness = max(current - amount, 0)

        sbc.set_brightness(new_brightness)

        if current == 0:
            return "Brightness is already at 0 percent, buddy."

        return (
            f"Brightness decreased by {amount} percent. "
            f"Current brightness is {new_brightness} percent."
        )

    except Exception as error:
        print(f"Brightness decrease error: {error}")
        return "Sorry buddy, I could not decrease the brightness."


def handle_brightness_command(text):
    """Understand brightness-related voice commands."""

    command = text.lower().strip()
    numbers = re.findall(r"\d+", command)

    amount = int(numbers[0]) if numbers else 10

    if (
        "current brightness" in command
        or "brightness level" in command
        or "what is my brightness" in command
        or "what's my brightness" in command
    ):
        current = get_brightness()

        if current is None:
            return "Sorry buddy, I could not detect the current brightness."

        return f"Current brightness is {current} percent."

    if "set brightness" in command:
        if not numbers:
            return "Please tell me the brightness percentage, buddy."

        return set_brightness(amount)

    if (
        "brightness up" in command
        or "increase brightness" in command
        or "raise brightness" in command
    ):
        return brightness_up(amount)

    if (
        "brightness down" in command
        or "decrease brightness" in command
        or "lower brightness" in command
        or "reduce brightness" in command
    ):
        return brightness_down(amount)

    return "Sorry buddy, I did not understand the brightness command."

# =========================================================
# MEDIA CONTROLS
# =========================================================

def play_pause_media():
    """Toggle the currently active media between play and pause."""
    try:
        pyautogui.press("playpause")
        return "Media play or pause command completed."
    except Exception as error:
        print(f"Media play/pause error: {error}")
        return "Sorry buddy, I could not control the media."


def next_track():
    """Move to the next track or playlist item."""
    try:
        pyautogui.press("nexttrack")
        return "Playing the next track."
    except Exception as error:
        print(f"Next-track error: {error}")
        return "Sorry buddy, I could not play the next track."


def previous_track():
    """Move to the previous track or playlist item."""
    try:
        pyautogui.press("prevtrack")
        return "Playing the previous track."
    except Exception as error:
        print(f"Previous-track error: {error}")
        return "Sorry buddy, I could not play the previous track."


def stop_media():
    """Stop the currently active media."""
    try:
        pyautogui.press("stop")
        return "Media stopped."
    except Exception as error:
        print(f"Stop-media error: {error}")
        return "Sorry buddy, I could not stop the media."


def handle_media_command(command):
    """Understand natural-language media commands."""
    command = command.lower().strip()

    if "next" in command:
        return next_track()

    if "previous" in command or "back track" in command:
        return previous_track()

    if "stop" in command:
        return stop_media()

    if (
        "play" in command
        or "pause" in command
        or "resume" in command
        or "continue" in command
    ):
        return play_pause_media()

    return (
        "Sorry buddy, I did not understand the media command. "
        "You can say play, pause, next track, previous track, or stop media."
    )