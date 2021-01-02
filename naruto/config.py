import os
from typing import Set
import sys
import heroku3
from git import Repo
from pyrogram import filters

class Config:
    """ Configs to setup Userge """
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    WORKERS = min(32, int(os.environ.get("WORKERS")) or os.cpu_count() + 4)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    HU_STRING_SESSION = os.environ.get("HU_STRING_SESSION", None)
    ASSISTANT_SESSION = os.environ.get("ASSISTANT_SESSION")
    OWNER_ID = tuple(filter(lambda x: x, map(int, os.environ.get("OWNER_ID", "0").split())))
    AdminSettings = [int(x) for x in (os.environ.get("AdminSettings", "")).split()]
    LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID"))
    REMINDER_UPDATE = os.environ.get(REMINDER_UPDATE", True)
    DB_URI = os.environ.get("DATABASE_URL", None)
    BOT_IMG = os.environ.get("BOT_IMG", None)
    DB_URI2 = os.environ.get("MONGODB_URL")
    LANG = os.environ.get("PREFERRED_LANGUAGE")
    DOWN_PATH = os.environ.get("DOWN_PATH")
    Command = (os.environ.get("Command", "! . - ^").split())
    CMD_TRIGGER = os.environ.get("CMD_TRIGGER")
    SUDO_TRIGGER = os.environ.get("SUDO_TRIGGER")
    FINISHED_PROGRESS_STR = os.environ.get("FINISHED_PROGRESS_STR")
    UNFINISHED_PROGRESS_STR = os.environ.get("UNFINISHED_PROGRESS_STR")
    ALIVE_MEDIA = os.environ.get("ALIVE_MEDIA", None)
    CUSTOM_PACK_NAME = os.environ.get("CUSTOM_PACK_NAME")
    INSTA_ID = os.environ.get("INSTA_ID")
    INSTA_PASS = os.environ.get("INSTA_PASS")
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO")
    UPSTREAM_REMOTE = os.environ.get("UPSTREAM_REMOTE")
    sw_api = os.environ.get("SPAM_WATCH_API", None)
    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    CURRENCY_API = os.environ.get("CURRENCY_API", None)
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)
    OPEN_WEATHER_MAP = os.environ.get("OPEN_WEATHER_MAP", None)
    REMOVE_BG_API_KEY = os.environ.get("REMOVE_BG_API_KEY", None)
    WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)
    TZ_NUMBER = os.environ.get("TZ_NUMBER", 1)
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    screenshotlayer_API= os.environ.get("SCREENSHOT_LAYER_API", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    G_DRIVE_PARENT_ID = os.environ.get("G_DRIVE_PARENT_ID", None)
    G_DRIVE_INDEX_LINK = os.environ.get("G_DRIVE_INDEX_LINK", None)
    GOOGLE_CHROME_DRIVER = os.environ.get("GOOGLE_CHROME_DRIVER", None)
    GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    G_DRIVE_IS_TD = os.environ.get("G_DRIVE_IS_TD") == "true"
    ASSISTANT_W = int(os.environ.get("ASSISTANT_WORKER"))
    BOT_W = int(os.environ.get("BOT_WORKER"))
    LOAD_UNOFFICIAL_PLUGINS = os.environ.get( "LOAD_UNOFFICIAL_PLUGINS") == "true"
    THUMB_PATH = DOWN_PATH + "thumb_image.jpg"
    TMP_PATH = "naruto/plugins/temp/"
    MAX_MESSAGE_LENGTH = 4096
    MSG_DELETE_TIMEOUT = 120
    WELCOME_DELETE_TIMEOUT = 120
    EDIT_SLEEP_TIMEOUT = 10
    AUTOPIC_TIMEOUT = 300
    ALLOWED_CHATS = filters.chat([])
    ALLOW_ALL_PMS = True
    USE_USER_FOR_CLIENT_CHECKS = False
    SUDO_ENABLED = False
    SUDO_USERS: Set[int] = set()
    ALLOWED_COMMANDS: Set[str] = set()
    ANTISPAM_SENTRY = False
    RUN_DYNO_SAVER = False
    GDRIVE_CREDENTIALS = (os.environ.get("gdrive_credentials"))
    HEROKU_APP = heroku3.from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME] \
        if HEROKU_API_KEY and HEROKU_APP_NAME else None
    STATUS = None
    PM_PERMIT= (os.environ.get("PM_PERMIT",None))
    lydia_api= (os.environ.get("LYDIA_API",None))
