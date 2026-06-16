import os
import shutil

from config import LOGS_DIR


def make_log_file(file_path: str, log_message: str):

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(log_message)


def clear_log_directory():
    for item in os.listdir(LOGS_DIR):
        item_path = os.path.join(LOGS_DIR, item)

        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
