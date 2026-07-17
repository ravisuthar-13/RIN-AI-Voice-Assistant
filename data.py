"""
RIN - Shared Data and Configuration

This module stores public-safe application commands, website URLs,
folder paths, and supported voice-command keywords.

No personal username or hard-coded private path is stored here.
"""

import os
from pathlib import Path


# ==========================================================
# Base directories
# ==========================================================

PROJECT_FOLDER = Path(__file__).resolve().parent
HOME_FOLDER = Path.home()

# Windows commonly stores Desktop, Documents, Pictures, etc.
# inside OneDrive. This detects OneDrive automatically.
ONEDRIVE_FOLDER = os.environ.get("OneDrive")


def get_user_folder(folder_name: str) -> str:
    """
    Return a common Windows user folder safely.

    It first checks the current user's OneDrive directory.
    If the folder does not exist there, it uses the normal
    Windows home directory.
    """

    if ONEDRIVE_FOLDER:
        onedrive_path = Path(ONEDRIVE_FOLDER) / folder_name

        if onedrive_path.exists():
            return str(onedrive_path)

    return str(HOME_FOLDER / folder_name)


# ==========================================================
# Folder data
# ==========================================================

folders = {
    "desktop": ("Desktop", get_user_folder("Desktop")),
    "documents": ("Documents", get_user_folder("Documents")),
    "downloads": ("Downloads", get_user_folder("Downloads")),
    "pictures": ("Pictures", get_user_folder("Pictures")),
    "videos": ("Videos", get_user_folder("Videos")),
    "music": ("Music", get_user_folder("Music")),
    "rin folder": ("RIN", str(PROJECT_FOLDER)),
}


folder_commands = [
    "open",
    "start",
    "launch",
    "run",
    "please open",
    "can you open",
    "open up",
]


# ==========================================================
# Application data
# ==========================================================

apps = {
    "calculator": ("Calculator", "calc"),
    "notepad": ("Notepad", "notepad"),
    "paint": ("Paint", "mspaint"),
    "chrome": ("Google Chrome", "start chrome"),
}


app_commands = [
    "open",
    "start",
    "launch",
    "run",
    "please open",
    "can you open",
    "open up",
]


# ==========================================================
# Website data
# ==========================================================

websites = {
    "google": ("Google", "https://www.google.com"),
    "youtube": ("YouTube", "https://www.youtube.com"),
    "github": ("GitHub", "https://github.com"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com"),
}


website_commands = [
    "open",
    "visit",
    "go to",
    "launch",
    "start",
    "please open",
    "can you open",
]


# ==========================================================
# Optional compatibility aliases
# ==========================================================

FOLDER_PATHS = folders
APPLICATIONS = apps
WEBSITES = websites


# ==========================================================
# Development test
# ==========================================================

if __name__ == "__main__":
    print("RIN data configuration loaded successfully.")
    print(f"Project folder: {PROJECT_FOLDER}")
    print(f"Home folder: {HOME_FOLDER}")
    print(f"OneDrive detected: {ONEDRIVE_FOLDER is not None}")
    print(f"Available folders: {list(folders.keys())}")
    print(f"Available applications: {list(apps.keys())}")
    print(f"Available websites: {list(websites.keys())}")