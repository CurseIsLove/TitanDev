from gpytranslate import Translator
from pyrogram import filters

from naruto import naruto, Command, AdminSettings, edrep

trl = Translator()

__MODULE__ = "Translate"
__HELP__ = """
Translates some text by give a text or reply that text/caption.
Translate by Google Translate.
──「 **Translate** 」──
-> `tr (lang) (*text)`
Give a target language and text as args for translate to that target.
Reply a message to translate that.
* = Not used when reply a message!
"""


@naruto.on_message(filters.user(AdminSettings) & filters.command("tr", Command))
async def translate(_, message):
    trl = Translator()
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await message.delete()
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edrep(message, text=f"Error: `{str(err)}`", parse_mode="Markdown")
            return
    else:
        if len(message.text.split()) <= 2:
            await message.delete()
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await edrep(
                message, text="Error: `{}`".format(str(err)), parse_mode="Markdown"
            )
            return

    await edrep(
        message,
        text=f"**Translated:**\n```{tekstr.text}```\n\n**Detected Language:** `{(await trl.detect(text))}`",
        parse_mode="Markdown",
    )
