import re
import asyncio

from pyrogram import filters
from naruto import naruto , PM_LOGGER

@app.on_message(~filters.me & filters.private & ~filters.bot)
async def pm_log(_, message):
    if not PM_LOGGER:
        return
    await message.forward("")
