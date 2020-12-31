
import asyncio
import time
from emoji import get_emoji_regexp

from pyrogram import filters
from pyrogram.types import ChatPermissions
from pyrogram.errors import (
    UsernameInvalid,
    ChatAdminRequired,
    PeerIdInvalid,
    UserIdInvalid,
    UserAdminInvalid,
    FloodWait,
)

from naruto import naruto, Command, AdminSettings, edrep ,setbot
from naruto.utils.admincheck import admin_check


custom_rank = ""
messages = ""
media = ""
stickers = ""
animations = ""
games = ""
inlinebots = ""
webprev = ""
polls = ""
info = ""
invite = ""
pin = ""
perm = ""

# Mute permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_stickers=False,
    can_send_animations=False,
    can_send_games=False,
    can_use_inline_bots=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@setbot.on_message(filters.command("unpin", "/") & filters.group)
async def unpin_message(client, message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        can_pin = await admin_check(message)
        if can_pin:
            try:
                await client.unpin_chat_message(chat_id)
            except UsernameInvalid:
                await edrep(message, text="`invalid username`")
                return

            except PeerIdInvalid:
                await edrep(message, text="`invalid username or userid`")
                return

            except UserIdInvalid:
                await edrep(message, text="`invalid userid`")
                return

            except ChatAdminRequired:
                await edrep(message, text=("denied_permission"))
                return

            except Exception as e:
                await edrep(message, text=f"`Error!`\n**Log:** `{e}`")
                return
        else:
            await edrep(message, text=("denied_permission"))
    else:
        await message.delete()
@setbot.on_message(filters.user(filters.command("pin", Command) & filters.group)
async def pin_message(client, message):
    if message.chat.type in ["group", "supergroup"]:
        can_pin = await admin_check(message)
        if can_pin:
            try:
                if message.reply_to_message:
                    disable_notification = True
                    if len(message.command) >= 2 and message.command[1] in [
                        "alert",
                        "notify",
                        "loud",
                    ]:
                        disable_notification = False
                    await client.pin_chat_message(
                        message.chat.id,
                        message.reply_to_message.message_id,
                        disable_notification=disable_notification,
                    )
                else:
                    await edrep(message, text=("pin_message"))
                    await asyncio.sleep(5)
                await message.delete()
            except Exception as e:
                await edrep(message, text="`Error!`\n" f"**Log:** `{e}`")
                return
        else:
            await edrep(message, text=("denied_permission"))
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()
