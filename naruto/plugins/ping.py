from . import ping
from naruto import naruto , AdminSettings , Command
from pyrogram import filters

@naruto.on_message(filters.user(AdminSettings) & filters.command("ping", Command))
async def _(_, message):
   await ping
