import os
import re
import sys

import telethon

from ForwardBot import bot, LOGS,  const_dirs_class, CMD_HELP
from ForwardBot.SymbConfig import Symb_Config
from ForwardBot.events import register
from ForwardBot.utils_no_bot.utils_no import retrieve_symbols


@register(incoming=True, pattern=r"^\.getsymbols(?: |$)(.*)")
async def handler(event: telethon.events.newmessage.NewMessage):
    LOGS.info(f"---Trying to get the symbols---")
    LOGS.info(f"Symbols to exclude: {Symb_Config.SYMB_TO_EXCLUDE}")

    list_to_string = '\n'.join(Symb_Config.SYMB_TO_EXCLUDE)
    if list_to_string == "" or list_to_string == None:
        await bot.send_message(message="`•Current Symbols:`\nNone", entity=event.chat_id)
    else:
        await bot.send_message(message="`•Current Symbols:`", entity=event.chat_id)
        await bot.send_message(message=f"`{list_to_string}`", entity=event.chat_id)


@register(incoming=True, pattern=r"^\.symbignore(?: |$)(.*)")
async def handler(event: telethon.events.newmessage.NewMessage):
    LOGS.info(f"---Trying to change symbols to ignore---")
    list_to_string = '\n'.join(Symb_Config.SYMB_TO_EXCLUDE)
    current_symbols = f"Current symbols\n{list_to_string}"
    LOGS.info(f"{current_symbols}")
    if list_to_string == "" or list_to_string == None:
        await bot.send_message(message="`•Current Symbols:`\nNone", entity=event.chat_id)
    else:
        await bot.send_message(message="`•Current Symbols:`", entity=event.chat_id)
        await bot.send_message(message=f"`{list_to_string}`", entity=event.chat_id)
    input_symbols = Symb_Config.extractor.extract(event.message.text)
    LOGS.info(f"Opening file {Symb_Config.FILE_SYMB_EXCLUDE} to save input_symbols: {input_symbols}")
    try:
        with open(Symb_Config.FILE_SYMB_EXCLUDE, "w") as f:
            for x in input_symbols:
                f.write(f"{x}\n")
        LOGS.info("Successfully saved symbols")
        Symb_Config.SYMB_TO_EXCLUDE = retrieve_symbols(
            os.path.join(const_dirs_class.CURR_DIR, Symb_Config.FILE_SYMB_EXCLUDE))
        LOGS.info(f"Retrieved symbols from file {Symb_Config.SYMB_TO_EXCLUDE}")
        list_to_string = '\n'.join(Symb_Config.SYMB_TO_EXCLUDE)
        if list_to_string == "" or list_to_string == None:
            await bot.send_message(message="`•New symbols`\n`None`", entity=event.chat_id)
        else:
            await bot.send_message(message=f"`New symbols:\n{list_to_string}`", entity=event.chat_id)
    except IOError as e:
        LOGS.error(f"I/O error({e.errno}): {e.strerror}")
    except:
        LOGS.error(f"Unexpected error: {sys.exc_info()[0]}")


CMD_HELP.update({
    "symbols": "✘ Pʟᴜɢɪɴ : Gets the current symbols to ignore."
                       "\n\n⚡𝘾𝙈𝘿⚡: `.symbignore <symbols>`"
                       "\n↳ : Updates current symbols to ignore"
                       "\n\n⚡𝘾𝙈𝘿⚡: `.getsymbols`"
                       "\n↳ : Gets the current that are being ignored"
})
