import os
from glob import glob
from mega import Mega
from pyrogram import filters

from naruto import naruto, Command, AdminSettings, edrep

__MODULE__ = "Mega"
__HELP__ = """
Download any file from URL or from telegram
──「 **Download mega file from URL** 」──
-> `mega (url)`
Give url as args to download it.
**Note**
this is a sync module. you cannot use your userbot while mega is downloading a file
For now folders are not supported yet
"""


async def megadl(url):
    mega = Mega()
    mega.download_url(url, "titan/downloads/mega")


@naruto.on_message(filters.user(AdminSettings) & filters.command(["mega"], Command))
async def mega_download(_, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await edrep(message, text="usage: mega (url)")
        return
    await edrep(message, text="__Processing...__")
    if not os.path.exists("titan/downloads/mega"):
        os.makedirs("titan/downloads/mega")
    await megadl(args[1])
    files_list = glob("titan/downloads/mega/*")
    for doc in files_list:
        await message.reply_document(doc)
        os.remove(doc)
    await message.delete()
