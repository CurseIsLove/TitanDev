import logging
import os
import platform
import sys
import time
from pyrogram import Client, errors
from naruto.config import Config
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


if HU_STRING_SESSION and ASSISTANT_SESSION:
    BOT_SESSION = ASSISTANT_SESSION
    APP_SESSION = HU_STRING_SESSION
OWNER = OWNER_ID
gauth = GoogleAuth()
AdminSettings = Owner
DB_AVAILABLE = False
BOTINLINE_AVAIABLE = False
USERBOT_VERSION = 0.1
ASSISTANT_VERSION = 0.1
USERBOT_LOAD =""
USERBOT_NOLOAD = ""
ASSISTANT_LOAD = ""
ASSISTANT_NOLOAD = ""
# Postgresql
def mulaisql() -> scoped_session:
    global DB_AVAILABLE
    engine = create_engine(DB_URI, client_encoding="utf8")
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
            await app.get_inline_bot_results("@{}".format(bot.username), "test")
            BOTINLINE_AVAIABLE = True
        except errors.exceptions.bad_request_400.BotInlineDisabled:
            BOTINLINE_AVAIABLE = False


async def get_self():
    global Owner, OwnerName, OwnerUsername, AdminSettings
    getself = await app.get_me()
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

setbot = Client(BOT_SESSION, api_id=api_id, api_hash=api_hash, bot_token=ASSISTANT_BOT_TOKEN, workers=ASSISTANT_W,
                test_mode=TEST_MODE)
app = Client(APP_SESSION, api_id=api_id, api_hash=api_hash, workers=BOT_W, test_mode=TEST_MODE)
