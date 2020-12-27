from time import time
from naruto import naruto , AdminSettings , Command
from pyrogram import filters

@naruto.on_message(filters.user(AdminSettings) & filters.command("ping", Command))
async def ping_it(_ , message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")
