import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from naruto import setbot, AdminSettings, BotUsername, naruto, Command, OwnerName, OwnerUsername
from naruto import StartTime
from naruto.helpers.PyroHelpers import ReplyCheck
from naruto.assistant.__main__ import dynamic_data_filter


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

Alive_pic = "https://telegra.ph/file/096e4e77231ca13b6ff47.mp4"
@naruto.on_message(filters.user(AdminSettings) & filters.command("alive", Command))
async def google_search(client, message):
    start_time = time.time()
    uptime = get_readable_time((time.time() - StartTime))
    reply_msg = f"**TITAN USERBOT** serving \n                 {OwnerName}@titan\n"
    reply_msg += "------------------\n"
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    reply_msg += f"Ping: {ping_time}ms\n"
    reply_msg += f"Userbot uptime: {uptime}\n"
    reply_msg += f"Owners username : {OwnerUsername}\n"
    reply_msg += f"__Running on pyrogram__\n"
    reply_msg += f"**Pyhton version**  : 3.8\n"
    reply_msg += f"Servers functioning- normal"
    await client.send_video(message.chat.id , Alive_pic , reply_msg)
    await message.delete()
