import asyncio
import sqlite3
from importlib import import_module

from pyrogram import idle
from pyrogram.errors import FloodWait

from ForwardBot import bot, LOGS
from ForwardBot.plugins import ALL_MODULES
from ForwardBot.utils_no_bot import MODS

INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\nTip: Use Country Code along with number ' \
             '\n or check your phone number and try again !'
for module_name in MODS:
    imported_module = import_module("ForwardBot.utils_no_bot." + module_name)
for module_name in ALL_MODULES:
    imported_module = import_module("ForwardBot.plugins." + module_name)


# start the bot and make it idle to wait for messages
async def start_bot():
    try:
        await bot.start()
        await idle()
    except BaseException as ex:
        LOGS.error(f"ERROR: {INVALID_PH}\n\n {ex}")
        exit(-3)
    except OSError as e:
        LOGS.error(f"An error happened while running the bot {e}")
    except sqlite3.ProgrammingError as e2:
        LOGS.error(f"Database error while running the bot {e2}")
        quit(-5012)


LOGS.info("Attempting to run bot")
loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
