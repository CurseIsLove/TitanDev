import re
import asyncio

from pyrogram import filters
from naruto import naruto , LOG_CHANNEL_ID

@naruto.on_message(~filters.me & filters.private & ~filters.bot)
async def pm_log(client, message):
    if not LOG_CHANNEL_ID:
        return
    await message.forward("LOG_CHANNEL_ID")
