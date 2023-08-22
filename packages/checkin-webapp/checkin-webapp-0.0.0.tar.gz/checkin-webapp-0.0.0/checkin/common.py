import appdirs
import os
import hashlib
import random
import base64

# ----------------------------- Public parameters ---------------------------- #
APP_NAME = "checkin"
APP_AUTHOR = "Ejovo"
SITE_DATA_DIR = appdirs.site_data_dir(APP_NAME, APP_AUTHOR)


_LOG_FILE_PATH = os.path.join(SITE_DATA_DIR, "log.txt")
_DEBUG: bool = False

def init():

    os.makedirs(SITE_DATA_DIR, exist_ok=True)

    if not os.path.exists(_LOG_FILE_PATH):
        touch(_LOG_FILE_PATH)

def touch(path: str):

    f = open(path, 'w')
    f.close()

def log_path() -> str:
    return _LOG_FILE_PATH

def clear_log_file():
    # Erase the contents of the log file
    f = open(log_path(), 'w')
    f.close()

def log_content(txt: str, ln = True):

    if (os.path.exists(log_path())):

        f = open(log_path(), 'a')

    else:

        f = open(log_path(), 'w')

    f.write(txt)
    if ln:
        f.write('\n')
    f.close()

def get_log_file_contents() -> str:

    if os.path.exists(log_path()):
        f = open(log_path(), 'r')
        lines = f.read()
        f.close()
        return lines
    else:
        return ""

def generate_api_key(len_out: int) -> str:
    """Generate an api key that is len_out bytes long, encoded using base64"""
    key = random.randbytes(len_out)
    return base64.b64encode(key)

# We are going to use an sqlite3 database to store user data




# def load_user_data()






