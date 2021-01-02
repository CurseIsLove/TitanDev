import logging
import os
import platform
import sys
import time
import requests
from inspect import getfullargspec
from pydrive.auth import GoogleAuth
from pyrogram import Client, errors
from pyrogram.types import Message
from naruto.config import Config
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s"
)
logging.basicConfig(
    level=logging.ERROR,
    format=LOG_FORMAT,
    datefmt="%m-%d %H:%M",
    filename="naruto/logs/error.log",
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
log = logging.getLogger()
APP_SESSION = Config.HU_STRING_SESSION
RANDOM_STICKERS = [
    "CAADAgAD6EoAAuCjggf4LTFlHEcvNAI",
    "CAADAgADf1AAAuCjggfqE-GQnopqyAI",
    "CAADAgADaV0AAuCjggfi51NV8GUiRwI",
]
HEROKU_API = Config.HEROKU_API_KEY
OWNER = Config.OWNER_ID
Owner = OWNER
REPOSITORY = "https://github.com/CurseIsLove/TitanDev/blob/main"
ENV = False
gauth = GoogleAuth()
OFFICIAL_BRANCH = ["master"]
GDRIVE_CREDENTIALS = Config.GDRIVE_CREDENTIALS
gdrive_credentials = Config.GDRIVE_CREDENTIALS
AdminSettings = Config.AdminSettings
DB_AVAILABLE = False
BOTINLINE_AVAIABLE = False
USERBOT_VERSION = 0.1
ASSISTANT_VERSION = 0.1
LOG_CHANNEL_ID = Config.LOG_CHANNEL_ID
USERBOT_LOAD =""
USERBOT_NOLOAD = ""
ASSISTANT_LOAD = ""
PM_PERMIT= Config.PM_PERMIT
lydia_api= Config.lydia_api
screenshotlayer_API = Config.screenshotlayer_API
remove_bg_api = Config.REMOVE_BG_API_KEY
ASSISTANT_NOLOAD = ""
IBM_WATSON_CRED_PASSWORD = Config.IBM_WATSON_CRED_PASSWORD
IBM_WATSON_CRED_URL = Config.IBM_WATSON_CRED_URL
Command = (Config.Command)
sw_api = Config.sw_api
COMMAND_PREFIXES = (Config.Command)
StartTime = time.time()
BOT_IMG = Config.BOT_IMG
REMINDER_UPDATE = bool(Config.REMINDER_UPDATE)
# Postgresqlw5mj by
def mulaisql() -> scoped_session:
    global DB_AVAILABLE
    engine = create_engine(Config.DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    try:
        BASE.metadata.create_all(engine)
    except exc.OperationalError:
        DB_AVAILABLE = False
        return False
    DB_AVAILABLE = True
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


async def get_bot_inline(bot):
    global BOTINLINE_AVAIABLE
    if setbot:
        try:
            await naruto.get_inline_bot_results("@{}".format(bot.username), "test")
            BOTINLINE_AVAIABLE = True
        except errors.exceptions.bad_request_400.BotInlineDisabled:
            BOTINLINE_AVAIABLE = False


async def get_self():
    global Owner, OwnerName, OwnerUsername, AdminSettings
    getself = await naruto.get_me()
    Owner = getself.id
    if getself.last_name:
        OwnerName = getself.first_name + " " + getself.last_name
    else:
        OwnerName = getself.first_name
    OwnerUsername = getself.username
    if Owner not in AdminSettings:
        AdminSettings.append(Owner)


async def get_bot():
    global BotID, BotName, BotUsername
    getbot = await setbot.get_me()
    BotID = getbot.id
    BotName = getbot.first_name
    BotUsername = getbot.username


BASE = declarative_base()
SESSION = mulaisql()
setbot = Client(":memory:",api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, workers=Config.ASSISTANT_W)
naruto = Client(APP_SESSION, api_id=Config.API_ID, api_hash=Config.API_HASH, workers=Config.BOT_W)
async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
