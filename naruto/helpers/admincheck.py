from pyrogram.types import Message
from naruto import naruto


async def admin_check(message: Message) -> bool:
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await naruto.get_chat_member(chat_id=chat_id, user_id=user_id)
    admin_strings = ["creator", "administrator"]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    return check_status.status in admin_strings
