import os
import sys


def locate_collection():
    if sys.platform == "win32":
        base_path = os.path.expandvars(r"%APPDATA%\Anki2")
    elif sys.platform == "darwin":
        base_path = os.path.expanduser("~/Library/Application Support/Anki2")
    else:
        base_path = os.path.expanduser("~/.local/share/Anki2")

    return os.path.join(base_path, "User 1", "collection.anki2")
