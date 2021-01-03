# Copyright (C) 2020 by CurselsLove@Github, < https://github.com/CurselsLove >.
#
# This file is part of < https://github.com/CurselsLove/Titan > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see <https://github.com/CurselsLove/Titan/blob/main/LICENSE >
#
# All rights reserved.import asyncio

from pyrogram import Client

APP_ID = int(input("enter Telegram APP ID: "))

API_HASH = input("enter Telegram API HASH: ")

async def main(api_id, api_hash):

    """ generate StringSession for the current MemorySession"""

    async with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:

        print(app.export_session_string())

if __name__ == "__main__":

	loop = asyncio.get_event_loop()

	loop.run_until_complete(main(APP_ID, API_HASH))
