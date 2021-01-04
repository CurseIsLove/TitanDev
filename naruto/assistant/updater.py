
import random
from git import Repo
from git.exc import GitCommandError, NoSuchPathError, InvalidGitRepositoryError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from naruto import (
    setbot,
    Owner,
    USERBOT_VERSION,
    ASSISTANT_VERSION,
    log,
    OFFICIAL_BRANCH,
    REPOSITORY,
    RANDOM_STICKERS,
    REMINDER_UPDATE,
)
from naruto.__main__ import restart_all, loop
from naruto.assistant.__main__ import dynamic_data_filter


async def gen_chlog(repo, diff):
    changelog = ""
    d_form = "%H:%M - %d/%m/%y"
    try:
        for cl in repo.iter_commits(diff):
            changelog += "• [{}]: {} <{}>\n".format(
                cl.committed_datetime.strftime(d_form),
                cl.summary,
                cl.author
            )
    except GitCommandError:
        changelog = None
    return changelog


async def update_changelog(changelog):
    await setbot.send_sticker(Owner, random.choice(RANDOM_STICKERS))
    text = ("update_successful"\n)
    text += ("update_welcome").format(USERBOT_VERSION, ASSISTANT_VERSION)
    text += ("\nupdated_changelo--g")
    text += changelog
    await setbot.send_message(Owner, text)


async def update_checker():
    try:
        repo = Repo()
    except NoSuchPathError as error:
        log.warning(f"Check update failed!\nDirectory {error} is not found!")
        return
    except InvalidGitRepositoryError as error:
        log.warning(
            "Check update failed!\nDirectory {} Not a git repository".format(
                error
            )
        )
        return
    except GitCommandError as error:
        log.warning(f"Check update failed!\n{error}")
        return

    brname = "main"
    if brname not in OFFICIAL_BRANCH:
        return

    try:
        repo.create_remote("upstream", REPOSITORY)
    except BaseException:
        pass

    upstream = repo.remote("upstream")
    upstream.fetch("main")
    changelog = await gen_chlog(repo, f"HEAD..upstream/{brname}")

    if not changelog:
        log.info(f"Titan is up-to-date with branch {brname}")
        return

    log.warning(f"New UPDATE available for [{brname}]!")

    text = tld("updater_available_text").format(brname)
    text += f"**CHANGELOG:**\n`{changelog}`"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    ("update_now_btn"),
                    callback_data="update_now"
                )
            ]
        ]
    )
    await setbot.send_message(
        Owner,
        text,
        reply_markup=button,
        parse_mode="markdown"
    )


@setbot.on_callback_query(dynamic_data_filter("update_now"))
async def update_button(client, query):
    await query.message.delete()
    await client.send_message(Owner, "Updating, please wait...")
    try:
        repo = Repo()
    except NoSuchPathError as error:
        log.warning(f"Check update failed!\nDirectory {error} is not found!")
        return
    except InvalidGitRepositoryError as error:
        log.warning(
            "Check update failed!\nDirectory {} Not a git repository".format(
                error
            )
        )
        return
    except GitCommandError as error:
        log.warning(f"Check update failed!\n{error}")
        return

    brname = "main"
    if brname not in OFFICIAL_BRANCH:
        return

    try:
        repo.create_remote("upstream", REPOSITORY)
    except BaseException:
        pass

    upstream = repo.remote("upstream")
    upstream.fetch("main")
    changelog = await gen_chlog(repo, f"HEAD..upstream/{brname}")
    try:
        upstream.pull(main)
        await client.send_message(Owner, "update_successful")
    except GitCommandError:
        repo.git.reset("--hard")
        repo.git.clean("-fd", "naruto/modules/")
        repo.git.clean("-fd", "naruto/assistant/")
        repo.git.clean("-fd", "naruto/utils/")
        await client.send_message(Owner, ("update_successful_force"))
    await update_changelog(changelog)
    await restart_all()


if REMINDER_UPDATE:
    loop.create_task(update_checker())
