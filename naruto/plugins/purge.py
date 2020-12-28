import math
from datetime import datetime
import asyncio
from pyrogram import filters

from naruto.helpers.admincheck import admin_check
from naruto import Owner, app, Command, AdminSettings, edrep

__MODULE__ = "Purges"
__HELP__ = """
Purge many messages in less than one second, you need to be an admin to do this.
Except for purgeme feature
Do with you own risk!
-> Deleted messages won't restore.
Ok looks like you've understood what happens if you play with this powerful weapon.
──「 **Purge** 」──
-> `purge`
Purge from below to that replied message, you need to be an admin to do this!
Give a number **without reply** to purge for x messages.
──「 **Purge My Messages** 」──
-> `purgeme`
Purge your messages only, no need for admin permission.
──「 **Delete** 」─
-> `del`
Deletes a message that you reply to.
"""


@app.on_message(filters.user(AdminSettings) & filters.command("purge", Command))
async def purge_message(client, message):
    if message.chat.type not in ("supergroup", "channel"):
        return
    is_admin = await admin_check(message)
    if not is_admin:
        await message.delete()
        return
    start_t = datetime.now()
    await message.delete()
    message_ids = []
    count_del_etion_s = 0
    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id, message.message_id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if message_ids:
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )
            count_del_etion_s += len(message_ids)
    end_t = datetime.now()
    time_taken_ms = (end_t - start_t).seconds
    ms_g = await client.send_message(
        message.chat.id,
        f"Purged {count_del_etion_s} messages in {time_taken_ms} seconds",
    )
    await asyncio.sleep(5)
    await ms_g.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("purgeme", Command))
async def purge_myself(client, message):
    if len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
        target = int(message.text.split()[1])
    else:
        await edrep(message, text="Give me a number for a range!")
    get_msg = await client.get_history(message.chat.id)
    listall = []
    counter = 0
    for x in get_msg:
        if counter == target + 1:
            break
        if x.from_user.id == int(Owner):
            listall.append(x.message_id)
            counter += 1
    if len(listall) >= 101:
        total = len(listall)
        semua = listall
        jarak = 0
        jarak2 = 0
        for x in range(math.ceil(len(semua) / 100)):
            if total >= 101:
                jarak2 += 100
                await client.delete_messages(
                    message.chat.id, message_ids=semua[jarak:jarak2]
                )
                jarak += 100
                total -= 100
            else:
                jarak2 += total
                await client.delete_messages(
                    message.chat.id, message_ids=semua[jarak:jarak2]
                )
                jarak += total
                total -= total
    else:
        await client.delete_messages(message.chat.id, message_ids=listall)


@app.on_message(filters.user(AdminSettings) & filters.command("del", Command))
async def delete_replied(client, message):
    msg_ids = [message.message_id]
    if message.reply_to_message:
        msg_ids.append(message.reply_to_message.message_id)
    await client.delete_messages(message.chat.id, msg_ids)
