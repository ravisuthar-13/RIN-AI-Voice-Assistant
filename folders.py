import os

def open_folder(name, path):
    print(f"Opening {name} buddy.")
    os.startfile(path)

def get_folder_name(text, folders, commands):
    for command in commands:
        if text.startswith(command):
            return text.replace(command, "", 1).strip()

    return None