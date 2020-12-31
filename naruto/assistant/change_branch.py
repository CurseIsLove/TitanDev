from git import Repo
from git.exc import GitCommandError
from naruto import setbot, NANA_IMG
from naruto.__main__ import restart_all
from naruto.assistant.__main__ import dynamic_data_filter
import re
from asyncio import create_subprocess_exec, sleep

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters

repo = Repo()


@setbot.on_callback_query(dynamic_data_filter("change_branches"))
async def chng_branch(_, query):
    buttons = [
        [InlineKeyboardButton(r, callback_data=f"chng_branch_{r}")]
        for r in repo.branches
    ]
    if BOT_IMG:
        await query.message.edit_caption(
            "Which Branch would you like to change to?\n" +
            "(this might destroy your userbot" +
            "if you are not cautious of what you are doing)"
        ),
        await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
    else:
        await query.message.edit(
            "Which Branch would you like to change to?. U might stop your userbot",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


async def branch_button_callback(_, __, query):
    if re.match(r"chng_branch_", query.data):
        return True


branch_button_create = filters.create(branch_button_callback)


@setbot.on_callback_query(branch_button_create)
async def change_to_branch(client, query):
    branch_match = re.findall(r"main|dev|translations", query.data)
    if branch_match:
        try:
            repo.git.checkout(branch_match[0])
        except GitCommandError as exc:
            await query.message.edit(f"**ERROR**: {exc}")
            return
        await create_subprocess_exec(
            "pip3",
            "install",
            "-U",
            "-r",
            "requirements.txt"
        )
        await query.message.edit(
            "Branch Changed to {}\nplease consider checking the logs".format(
                repo.active_branch
            )
        )
        await query.answer()
        await sleep(60)
        await restart_all()
    else:
        await query.answer("Doesnt look like an Official Branch, Aborting!")
