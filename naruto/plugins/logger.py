import re
import asyncio

from pyrogram import filters
from naruto import naruto , LOG_CHANNEL_ID

@app.on_message(~filters.me & filters.private & ~filters.bot)
async def pm_log(client, message):
    if LOG_CHANNEL_ID is None
        return
    await message.forward("LOG_CHANNEL_ID")
