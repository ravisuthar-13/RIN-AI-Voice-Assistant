from pathlib import Path
import os


PROJECT_FOLDER = Path(__file__).resolve().parent
HOME = Path.home()
ONEDRIVE = os.environ.get("OneDrive")


def get_user_folder(folder_name):
    if ONEDRIVE:
        onedrive_folder = Path(ONEDRIVE) / folder_name

        if onedrive_folder.exists():
            return str(onedrive_folder)

    return str(HOME / folder_name)


folders = {
    "desktop": ("Desktop", get_user_folder("Desktop")),
    "documents": ("Documents", get_user_folder("Documents")),
    "downloads": ("Downloads", get_user_folder("Downloads")),
    "pictures": ("Pictures", get_user_folder("Pictures")),
    "videos": ("Videos", get_user_folder("Videos")),
    "music": ("Music", get_user_folder("Music")),
    "rin folder": ("RIN", str(PROJECT_FOLDER)),
}


apps = {
    "calculator": ("Calculator", "calc"),
    "notepad": ("Notepad", "notepad"),
    "paint": ("Paint", "mspaint"),
    "chrome": ("Google Chrome", "start chrome"),
}


websites = {
    "google": ("Google", "https://www.google.com"),
    "youtube": ("YouTube", "https://www.youtube.com"),
    "github": ("GitHub", "https://github.com"),
    "linkedin": ("LinkedIn", "https://www.linkedin.com"),
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
