 
import os
import shutil
import sys

from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError, NoSuchPathError
from pyrogram import filters

from naruto import (
    naruto,
    COMMAND_PREFIXES,
    AdminSettings,
    OFFICIAL_BRANCH,
    REPOSITORY,
    edrep as edit_or_reply,
)
from naruto.__main__ import restart_all, except_hook
from naruto.assistant.updater import update_changelog

__MODULE__ = "Updater"
__HELP__ = """
You want to update latest version?
Easy, just type like bellow
──「 **Check update** 」──
-> `update`
Only check update if avaiable
──「 **Update bot** 」──
-> `update now`
Update your bot to latest version
"""


async def gen_chlog(repo, diff):
    d_form = "%H:%M - %d/%m/%y"
    return "".join(
        "• [{}]: {} <{}>\n".format(
            cl.committed_datetime.strftime(d_form),
            cl.summary,
            cl.author
        )
        for cl in repo.iter_commits(diff)
    )


async def initial_git(repo):
    isexist = os.path.exists("naruto-old")
    if isexist:
        shutil.rmtree("naruto-old")
    os.mkdir("naruto-old")
    os.rename("naruto", "naruto-old/naruto")
    os.rename(".gitignore", "naruto-old/.gitignore")
    os.rename("LICENSE", "naruto-old/LICENSE")
    os.rename("README.md", "naruto-old/README.md")
    os.rename("requirements.txt", "naruto-old/requirements.txt")
    os.rename("Procfile", "naruto-old/Procfile")
    os.rename("runtime.txt", "naruto-old/runtime.txt")
    update = repo.create_remote("main", REPOSITORY)
    update.pull("main")
    os.rename("naruto-old/naruto/config.py", "naruto/config.py")
    shutil.rmtree("naruto/session/")
    os.rename("naruto-old/naruto/session/", "naruto/session/")


@naruto.on_message(
    filters.user(AdminSettings) &
    filters.command("update", COMMAND_PREFIXES)
)
async def updater(client, message):
    initial = False
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await edit_or_reply(
            message,
            text="**Update failed!**\n\n"
            f"Error:\n`directory {error} is not found`",
        )
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        initial = True
    except GitCommandError as error:
        await edit_or_reply(
            message,
            text=f"**Update failed!**\n\nError:\n`{error}`"
        )
        return

    if initial:
        if len(message.text.split()) != 2:
            await edit_or_reply(
                message,
                text="Your git workdir is missing!\nJust do `update "
                "now` to repair and take update!",
            )
            return
        elif len(
            message.text.split()
        ) == 2 and message.text.split()[1] == "now":
            try:
                await initial_git(repo)
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                await edit_or_reply(message, text=f"**Error:**\n{err}")
                await except_hook(exc_type, exc_obj, exc_tb)
                return
            await edit_or_reply(
                message,
                text="Successfully Updated!\nBot is restarting..."
            )
            await update_changelog(
                "-> **WARNING**: Bot has been created a new git"
            )
            await restart_all()
            return

    brname = "Deploy"
    if brname not in OFFICIAL_BRANCH:
        await edit_or_reply(
            message,
            text="**[UPDATER]:** Looks like you are using your own"
            f"custom branch ({brname})."
            "in that case, Updater is unable to"
            "identify which branch is to be merged."
            "please checkout to any official branch",
        )
        return
    try:
        repo.create_remote("upstream", REPOSITORY)
    except BaseException:
        pass

    upstream = repo.remote("upstream")
    upstream.fetch("main")
    try:
        changelog = await gen_chlog(repo, f"HEAD..upstream/main")
    except Exception as err:
        if "fatal: bad revision" in str(err):
            try:
                await initial_git(repo)
            except Exception as err:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                await edit_or_reply(message, text=f"**Error:**\n{err}")
                await except_hook(exc_type, exc_obj, exc_tb)
                return
            await edit_or_reply(
                message, text="Successfully Updated!\nBot is restarting..."
            )
            await update_changelog(
                "-> **WARNING**: Bot has been created a new git"
            )
            await restart_all()
            return
        exc_type, exc_obj, exc_tb = sys.exc_info()
        await edit_or_reply(
            message,
            text="An error has accured!",
        )
        await except_hook(exc_type, exc_obj, exc_tb)
        return

    if not changelog:
        await edit_or_reply(
            message, text=f"titan is up-to-date with branch **{brname}**\n"
        )
        return

    if len(message.text.split()) != 2:
        changelog_str = (
            "To update latest changelog, do\n-> `update now`\n\n**"
            f"New UPDATE available for [{brname}]:\n"
            f"\nCHANGELOG:**\n`{changelog}` "
        )
        if len(changelog_str) > 4096:
            await edit_or_reply(
                message,
                text="`Changelog is too big, view the file to see it.`"
            )
            with open("naruto/cache/output.txt", "w+") as file:
                file.write(changelog_str)
            await client.send_document(
                message.chat.id,
                "naruto/cache/output.txt",
                reply_to_message_id=message.message_id,
                caption="`Changelog file`",
            )
            os.remove("naruto/cache/output.txt")
        else:
            await edit_or_reply(message, text=changelog_str)
        return
    elif len(message.text.split()) == 2 and message.text.split()[1] == "now":
        await edit_or_reply(message, text="`New update found, updating...`")
        try:
            upstream.pull("main")
            await edit_or_reply(
                message, text="Successfully Updated!\nBot is restarting..."
            )
        except GitCommandError:
            repo.git.reset("--hard")
            repo.git.clean("-fd", "naruto/modules/")
            repo.git.clean("-fd", "nana/assistant/")
            repo.git.clean("-fd", "naruto/utils/")
            await edit_or_reply(
                message, text="Successfully Updated!\nBot is restarting..."
            )
        await update_changelog(changelog)
        await restart_all()
    else:
        await edit_or_reply(
            message,
            text="Usage:\n-> `update` to check update\n"
            "-> `update now` to update latest commits\nFor more information ",
        )
