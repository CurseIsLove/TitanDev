from . import ping
from naruto import naruto , AdminSettings , Command
from pyrogram import filters

@naruto.on_message(filters.command(filters.user(AdminSettings) & ("ping", Command)))
async def _(_, message):
   await ping(_, message)
