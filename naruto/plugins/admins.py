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

from naruto import naruto, Command, AdminSettings, edrep
from naruto.utils.admincheck import admin_check



__MODULE__ = "Admin"
__HELP__ = """
Module for Group Admins
──「 **Locks / Unlocks** 」──
-> `lock` or `unlock`
locks and unlocks permission in the group
__Supported Locks / Unlocks__:
 `messages` `media` `stickers`
 `polls` `info` `invite`
 `animations` `games`
 `inlinebots` `webprev`
 `pin` `all`
-> `vlock`
view group permissions
──「 **Promote / Demote** 」──
-> `promote`
Reply to a user to promote
-> `demote`
Reply to a user to demote
──「 **Ban / Unban** 」──
-> `ban` or `unban`
Reply to a user to perform ban or unban
──「 **Kick User** 」──
-> `kick`
Reply to a user to kick from chat
──「 **Mute / Unmute** 」──
-> `mute` or `mute 24` or `unmute`
Reply to a user to mute or unmute
──「 **Invite Link** 」──
-> `invite`
Generate Invite link
──「 **Message Pin** 」──
-> `pin`
Reply a message to pin in the Group
__Supported pin types__: `alert`, `notify`, `loud`
──「 **Deleted Account** 」──
-> `zombies` or `zombies clean`
Checks Group for deleted accounts & clean them
"""
──「 **Group Calls** 」──
-> `cgroupcall` (**chat_id)
Create a GroupCall
"""
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


@naruto.on_message(filters.user(AdminSettings) & filters.command("unpin", Command))
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


@naruto.on_message(filters.user(AdminSettings) & filters.command("invite", Command))
async def invite_link(client, message):
    if message.chat.type in ["group", "supergroup"]:
        chat_name = message.chat.title
        can_invite = await admin_check(message)
        if can_invite:
            try:
                link = await client.export_chat_invite_link(message.chat.id)
                await edrep(message, text=("invite_link").format(chat_name, link))
            except Exception as e:
                print(e)
                await edrep(message, text=("denied_permission"))
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("pin", Command))
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


@naruto.on_message(filters.user(AdminSettings) & filters.command("mute", Command))
async def mute_hammer(client, message):
    if message.chat.type in ["group", "supergroup"]:
        can_mute = await admin_check(message)
        if can_mute:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await message.reply("some ooga booga")
                return
            try:
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=mute_permission,
                )
                await message.delete()
            except Exception as e:
                await edrep(message, text="`Error!`\n" f"**Log:** `{e}`")
                return
        else:
            await edrep(message, text=("denied_permission"))
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("unmute", Command))
async def unmute(client, message):
    if message.chat.type in ["group", "supergroup"]:
        can_unmute = await admin_check(message)
        if can_unmute:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await edrep(message, text="must give a user to unmute")
                return
            try:
                await client.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=user_id,
                    permissions=unmute_permissions,
                )
                await message.delete()
            except ChatAdminRequired:
                await edrep(message, text=("denied_permission"))
                return
            except Exception as e:
                await edrep(message, text="`Error!`\n" f"**Log:** `{e}`")
                return
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("kick", Command))
async def kick_user(client, message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        can_kick = await admin_check(message)
        if can_kick:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await edrep(message, text="must give a user to kick")
                return
            try:
                get_mem = await client.get_chat_member(chat_id, user_id)
                await client.kick_chat_member(
                    chat_id, get_mem.user.id, int(time.time() + 45)
                )
                await message.delete()
            except ChatAdminRequired:
                await edrep(message, text=("denied_permission"))
                return
            except Exception as e:
                await edrep(message, text="`Error!`\n" f"**Log:** `{e}`")
                return
        else:
            await edrep(message, text=("denied_permission"))
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("ban", Command))
async def ban_usr(client, message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        can_ban = await admin_check(message)

        if can_ban:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await edrep(message, text="I cant ban a void xD")
                return
            if user_id:
                try:
                    await client.kick_chat_member(chat_id, user_id)
                    await message.delete()
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
                    await edrep(message, text="`permission denied`")
                    return

                except Exception as e:
                    await edrep(message, text=f"**Log:** `{e}`")
                    return

        else:
            await edrep(message, text="`permission denied`")
            return
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("unban", Command))
async def unban_usr(client, message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        can_unban = await admin_check(message)
        if can_unban:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await edrep(message, text="I cant unban the void xD")
                return
            try:
                get_mem = await client.get_chat_member(chat_id, user_id)
                await client.unban_chat_member(chat_id, get_mem.user.id)
                await message.delete()
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
                await edrep(message, text="`permission denied`")
                return

            except Exception as e:
                await edrep(message, text=f"**Log:** `{e}`")
                return
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("promote", Command))
async def promote_usr(client, message):
    if message.chat.type in ["group", "supergroup"]:
        cmd = message.command
        can_promo = await admin_check(message)
        if can_promo:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                    custom_rank = get_emoji_regexp().sub("", " ".join(cmd[1:]))
                else:
                    usr = await client.get_users(cmd[1])
                    custom_rank = get_emoji_regexp().sub("", " ".join(cmd[2:]))
                    user_id = usr.id
            except IndexError:
                await message.delete()
                return

            if user_id:
                try:
                    await client.promote_chat_member(
                        message.chat.id,
                        user_id,
                        can_change_info=True,
                        can_delete_messages=True,
                        can_restrict_members=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    )

                    await asyncio.sleep(2)
                    await client.set_administrator_title(
                        message.chat.id, user_id, custom_rank
                    )
                    await message.delete()
                except UsernameInvalid:
                    await edrep(message, text=("user_invalid"))
                    await asyncio.sleep(5)
                    await message.delete()
                    return
                except PeerIdInvalid:
                    await edrep(message, text=("peer_invalid"))
                    await asyncio.sleep(5)
                    await message.delete()
                    return
                except UserIdInvalid:
                    await edrep(message, text=("id_invalid"))
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except ChatAdminRequired:
                    await edrep(message, text=("denied_permission"))
                    await asyncio.sleep(5)
                    await message.delete()
                    return

                except Exception as e:
                    await edrep(message, text=f"**Log:** `{e}`")
                    return

        else:
            await edrep(message, text=("denied_permission"))
            await asyncio.sleep(5)
            await message.delete()
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("demote", Command))
async def demote_usr(client, message):
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        can_demote = await admin_check(message)
        if can_demote:
            try:
                if message.reply_to_message:
                    user_id = message.reply_to_message.from_user.id
                else:
                    usr = await client.get_users(message.command[1])
                    user_id = usr.id
            except IndexError:
                await edrep(message, text="I cant demote the void xD")
                return
            try:
                await client.promote_chat_member(
                    chat_id,
                    user_id,
                    can_change_info=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                )
                await message.delete()
            except ChatAdminRequired:
                await edrep(message, text=("denied_permission"))
                await asyncio.sleep(5)
                await message.delete()
                return

            except Exception as e:
                await edrep(message, text=f"**Log:** `{e}`")
                return
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("lock", Command))
async def lock_permission(client, message):
    """module that locks group permissions"""
    if message.chat.type in ["group", "supergroup"]:
        cmd = message.command
        is_admin = await admin_check(message)
        if not is_admin:
            await message.delete()
            return
        lock_type = " ".join(cmd[1:])
        chat_id = message.chat.id
        if not lock_type:
            await message.delete()
            return

        get_perm = await client.get_chat(chat_id)

        messages = get_perm.permissions.can_send_messages
        media = get_perm.permissions.can_send_media_messages
        stickers = get_perm.permissions.can_send_stickers
        animations = get_perm.permissions.can_send_animations
        games = get_perm.permissions.can_send_games
        inlinebots = get_perm.permissions.can_use_inline_bots
        webprev = get_perm.permissions.can_add_web_page_previews
        polls = get_perm.permissions.can_send_polls
        info = get_perm.permissions.can_change_info
        invite = get_perm.permissions.can_invite_users
        pin = get_perm.permissions.can_pin_messages

        if lock_type == "all":
            try:
                await client.set_chat_permissions(chat_id, ChatPermissions())
                await edrep(message, text=("lock_all"))
                await asyncio.sleep(5)
                await message.delete()

            except Exception as e:
                await edrep(message, text=("denied_permission"))
            return

        if lock_type == "messages":
            messages = False
            perm = "messages"

        elif lock_type == "media":
            media = False
            perm = "audios, documents, photos, videos, video notes, voice notes"

        elif lock_type == "stickers":
            stickers = False
            perm = "stickers"

        elif lock_type == "animations":
            animations = False
            perm = "animations"

        elif lock_type == "games":
            games = False
            perm = "games"

        elif lock_type == "inlinebots":
            inlinebots = False
            perm = "inline bots"

        elif lock_type == "webprev":
            webprev = False
            perm = "web page previews"

        elif lock_type == "polls":
            polls = False
            perm = "polls"

        elif lock_type == "info":
            info = False
            perm = "info"

        elif lock_type == "invite":
            invite = False
            perm = "invite"

        elif lock_type == "pin":
            pin = False
            perm = "pin"

        else:
            print(e)
            await message.delete()
            return

        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=messages,
                    can_send_media_messages=media,
                    can_send_stickers=stickers,
                    can_send_animations=animations,
                    can_send_games=games,
                    can_use_inline_bots=inlinebots,
                    can_add_web_page_previews=webprev,
                    can_send_polls=polls,
                    can_change_info=info,
                    can_invite_users=invite,
                    can_pin_messages=pin,
                ),
            )
            await edrep(message, text=("lock_chat").format(perm))
            await asyncio.sleep(5)
            await message.delete()
        except Exception as e:
            print(e)
            await message.delete()
            return
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("unlock", Command))
async def unlock_permission(client, message):
    """this module unlocks group permission for admins"""
    if message.chat.type in ["group", "supergroup"]:
        cmd = message.command
        is_admin = await admin_check(message)
        if not is_admin:
            await message.delete()
            return

        umsg = ""
        umedia = ""
        ustickers = ""
        uanimations = ""
        ugames = ""
        uinlinebots = ""
        uwebprev = ""
        upolls = ""
        uinfo = ""
        uinvite = ""
        upin = ""
        uperm = ""  # pylint:disable=E0602

        unlock_type = " ".join(cmd[1:])
        chat_id = message.chat.id

        if not unlock_type:
            await message.delete()
            return

        get_uperm = await client.get_chat(chat_id)
        umsg = get_uperm.permissions.can_send_messages
        umedia = get_uperm.permissions.can_send_media_messages
        ustickers = get_uperm.permissions.can_send_stickers
        uanimations = get_uperm.permissions.can_send_animations
        ugames = get_uperm.permissions.can_send_games
        uinlinebots = get_uperm.permissions.can_use_inline_bots
        uwebprev = get_uperm.permissions.can_add_web_page_previews
        upolls = get_uperm.permissions.can_send_polls
        uinfo = get_uperm.permissions.can_change_info
        uinvite = get_uperm.permissions.can_invite_users
        upin = get_uperm.permissions.can_pin_messages

        if unlock_type == "all":
            try:
                await client.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_stickers=True,
                        can_send_animations=True,
                        can_send_games=True,
                        can_use_inline_bots=True,
                        can_send_polls=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                        can_add_web_page_previews=True,
                    ),
                )
                await edrep(message, text=("unlock_all"))
                await asyncio.sleep(5)
                await message.delete()

            except Exception as e:
                print(e)
                await edrep(message, text=("denied_permission"))
            return

        if unlock_type == "msg":
            umsg = True
            uperm = "messages"

        elif unlock_type == "media":
            umedia = True
            uperm = "audios, documents, photos, videos, video notes, voice notes"

        elif unlock_type == "stickers":
            ustickers = True
            uperm = "stickers"

        elif unlock_type == "animations":
            uanimations = True
            uperm = "animations"

        elif unlock_type == "games":
            ugames = True
            uperm = "games"

        elif unlock_type == "inlinebots":
            uinlinebots = True
            uperm = "inline bots"

        elif unlock_type == "webprev":
            uwebprev = True
            uperm = "web page previews"

        elif unlock_type == "polls":
            upolls = True
            uperm = "polls"

        elif unlock_type == "info":
            uinfo = True
            uperm = "info"

        elif unlock_type == "invite":
            uinvite = True
            uperm = "invite"

        elif unlock_type == "pin":
            upin = True
            uperm = "pin"

        else:
            await edrep(message, text=("unlock_invalid"))
            await asyncio.sleep(5)
            await message.delete()
            return

        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=umsg,
                    can_send_media_messages=umedia,
                    can_send_stickers=ustickers,
                    can_send_animations=uanimations,
                    can_send_games=ugames,
                    can_use_inline_bots=uinlinebots,
                    can_add_web_page_previews=uwebprev,
                    can_send_polls=upolls,
                    can_change_info=uinfo,
                    can_invite_users=uinvite,
                    can_pin_messages=upin,
                ),
            )
            await edrep(message, text=("unlock_chat").format(uperm))
            await asyncio.sleep(5)
            await message.delete()

        except Exception as e:
            await edrep(message, text="`Error!`\n" f"**Log:** `{e}`")
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("vlock", Command))
async def view_perm(client, message):
    """view group permission."""
    if message.chat.type in ["group", "supergroup"]:
        v_perm = ""
        vmsg = ""
        vmedia = ""
        vstickers = ""
        vanimations = ""
        vgames = ""
        vinlinebots = ""
        vwebprev = ""
        vpolls = ""
        vinfo = ""
        vinvite = ""
        vpin = ""

        v_perm = await client.get_chat(message.chat.id)

        def convert_to_emoji(val: bool):
            if val:
                return "<code>True</code>"
            return "<code>False</code>"

        vmsg = convert_to_emoji(v_perm.permissions.can_send_messages)
        vmedia = convert_to_emoji(v_perm.permissions.can_send_media_messages)
        vstickers = convert_to_emoji(v_perm.permissions.can_send_stickers)
        vanimations = convert_to_emoji(v_perm.permissions.can_send_animations)
        vgames = convert_to_emoji(v_perm.permissions.can_send_games)
        vinlinebots = convert_to_emoji(v_perm.permissions.can_use_inline_bots)
        vwebprev = convert_to_emoji(v_perm.permissions.can_add_web_page_previews)
        vpolls = convert_to_emoji(v_perm.permissions.can_send_polls)
        vinfo = convert_to_emoji(v_perm.permissions.can_change_info)
        vinvite = convert_to_emoji(v_perm.permissions.can_invite_users)
        vpin = convert_to_emoji(v_perm.permissions.can_pin_messages)

        if v_perm is not None:
            try:
                await edrep(
                    message,
                    text=("permission_view_str").format(
                        vmsg,
                        vmedia,
                        vstickers,
                        vanimations,
                        vgames,
                        vinlinebots,
                        vwebprev,
                        vpolls,
                        vinfo,
                        vinvite,
                        vpin,
                    ),
                )
            except Exception as e:
                await edrep(message, text="`Error!`\n" f"**Log:** `{e}`")
    else:
        await message.delete()


@naruto.on_message(filters.user(AdminSettings) & filters.command("zombies", Command))
async def deleted_clean(client, message):
    cmd = message.command
    chat_id = message.chat.id
    get_group = await client.get_chat(chat_id)

    clean_tag = " ".join(cmd[1:])
    rm_delaccs = "clean" in clean_tag
    can_clean = await admin_check(message)
    del_stats = "`no deleted accounts found in this chat`"

    del_users = 0
    if rm_delaccs:
        if can_clean:
            await edrep(message, text="`cleaning deleted accounts from this chat..`")
            del_admins = 0
            del_total = 0
            async for member in client.iter_chat_members(chat_id):

                if member.user.is_deleted:
                    try:
                        await client.kick_chat_member(
                            chat_id, member.user.id, int(time.time() + 45)
                        )
                    except UserAdminInvalid:
                        del_users -= 1
                        del_admins += 1

                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                    del_users += 1
                    del_total += 1

            del_stats = f"`Found` **{del_total}** `total accounts..`"
            await edrep(message, text=del_stats)
            await message.edit(
                f"**Cleaned Deleted accounts**:\n"
                f"Total Deleted Accounts: `{del_total}`\n"
                f"Cleaned Deleted Accounts: `{del_users}`\n"
                f"Chat: `{get_group.title}` (`{chat_id}`)"
            )

        else:
            await edrep(message, text=("denied_permission"))

    else:
        async for member in client.iter_chat_members(chat_id):
            if member.user.is_deleted:
                del_users += 1
        if del_users > 0:
            del_stats = f"`Found` **{del_users}** `deleted accounts in this chat.`"
        await edrep(message, text=del_stats)


@naruto.on_message(
    filters.user(AdminSettings) &
    filters.command("cgroupcall", COMMAND_PREFIXES)
)
async def create_group_call(_, message):
    cmd = message.command
    try:
        peer = await app.resolve_peer(cmd[1])
    except IndexError:
        peer = await app.resolve_peer(message.chat.id)
    try:
        await naruto.send(
            raw.functions.phone.CreateGroupCall(
                peer=raw.types.InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash
                ),
                random_id=app.rnd_id() // 9000000000
            )
        )
    except ChatAdminRequired:
        await edit_or_reply(
            message,
            text=tld("denied_permission")
        )
    except AttributeError:
        await message.delete()
