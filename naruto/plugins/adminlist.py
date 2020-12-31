import html

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from naruto import naruto, Command, edrep
from naruto.utils.parser import mention_html, mention_markdown

__MODULE__ = "Admin List"
__HELP__ = """
This module meant for check admins/bots or report someone, not for spamming groups.
Please note spam admin will give you instant banned. Don't play with this command if you understand what it cost!
──「 **Admin list** 」──
-> `admins`
-> `adminlist`
For get admin list in spesific chat or current chat
──「 **Report admin** 」──
-> `reportadmin`
-> `reportadmins`
To report someone or report your message to all admins
──「 **Bot list** 」──
-> `botlist`
Check all bots in spesific chat or current chat
"""


@naruto.on_message(filters.me & filters.command(["admins", "adminlist"], Command))
async def adminlist(client, message):
    creator = []
    admin = []
    badmin = []
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    alladmins = client.iter_chat_members(chat, filter="administrators")
    async for a in alladmins:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == "administrator":
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == "creator":
            creator.append(mention_markdown(a.user.id, nama))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = ("adminlist_one").format(grup.title)
    for x in creator:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += ("adminlist_two").format(len(admin))
    for x in admin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += ("adminlist_three").format(len(badmin))
    for x in badmin:
        teks += "│ • {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += ("adminlist_four").format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await edrep(message, text=teks)


@naruto.on_message(filters.me & filters.command("reportadmins", Command))
async def report_admin(client, message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = None
    grup = await client.get_chat(message.chat.id)
    alladmins = client.iter_chat_members(message.chat.id, filter="administrators")
    admin = [
        mention_html(a.user.id, "\u200b")
        for a in alladmins
        if a.status in ["administrator", "creator"] and not a.user.is_bot
    ]

    if message.reply_to_message:
        if text:
            teks = "{}".format(text)
        else:
            user = message.reply_to_message.from_user
            teks = ("reportadmins_one").format(
                mention_html(user.id, user.first_name)
            )
    else:
        if text:
            teks = "{}".format(html.escape(text))
        else:
            teks = ("reportadmins_two").format(grup.title)
    teks += "".join(admin)
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            teks,
            reply_to_message_id=message.reply_to_message.message_id,
            parse_mode="html",
        )
    else:
        await client.send_message(message.chat.id, teks, parse_mode="html")


@naruto.on_message(filters.me & filters.command("tagall", Command))
async def tag_all_users(client, message):
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = tld("tagall")
    kek = client.iter_chat_members(message.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, "\u200b")
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            text,
            reply_to_message_id=message.reply_to_message.message_id,
            parse_mode="html",
        )
    else:
        await client.send_message(message.chat.id, text, parse_mode="html")
    await message.delete()


@naruto.on_message(filters.me & filters.command("botlist", Command))
async def get_list_bots(client, message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    getbots = client.iter_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = ("botlist_one")
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, nama))
    teks = ("botlist_two").format(grup.title)
    teks += "botlist_three"
    for x in bots:
        teks += "│ • {}\n".format(x)
    teks += ("botlist_four").format(len(bots))
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await edrep(message, text=teks)
