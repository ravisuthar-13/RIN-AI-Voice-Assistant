import os

def open_app(name, command):
    print(f"Opening {name} buddy.")
    os.system(command)

def get_app_name(text, apps, commands):
    for command in commands:
        if text.startswith(command):
            return text.replace(command, "", 1).strip()

    return None