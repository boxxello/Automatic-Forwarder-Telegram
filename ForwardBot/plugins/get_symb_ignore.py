import os
import re
import sys

import pyrogram
from pyrogram.enums import ChatAction

import ForwardBot
from ForwardBot import bot, LOGS, const_dirs_class, CMD_HELP
from ForwardBot.SymbConfig import Symb_Config, BlacklistWords
from ForwardBot.events import register
from ForwardBot.utils_no_bot.utils_no import retrieve_symbols, retrieve_lines_from_file


@register(incoming=True, pattern=r"^\.getsymbols(?: |$)(.*)")
async def handler(event: pyrogram.types.Message):
    await bot.send_chat_action(chat_id=event.chat.id, action=ChatAction.TYPING)
    LOGS.info(f"---Trying to get the symbols---")
    LOGS.info(f"Symbols to exclude: {Symb_Config.SYMB_TO_EXCLUDE}")

    list_to_string = '\n'.join(Symb_Config.SYMB_TO_EXCLUDE)
    if list_to_string == "" or list_to_string == None:
        await bot.send_message(text="<b>•Current Symbols:</b>\n`None`", chat_id=event.chat.id, reply_to_message_id=event.id)
    else:
        await bot.send_message(text=f"<b>•Current Symbols:</b>\n`{list_to_string}`", chat_id=event.chat.id, reply_to_message_id=event.id)


@register(incoming=True, pattern=r"^\.symbignore(?: |$)(.*)")
async def handler(event: pyrogram.types.Message):
    await bot.send_chat_action(chat_id=event.chat.id, action=ChatAction.TYPING)
    LOGS.info(f"---Trying to change symbols to ignore---")
    list_to_string = '\n'.join(Symb_Config.SYMB_TO_EXCLUDE)
    current_symbols = f"Current symbols\n{list_to_string}"
    LOGS.info(f"{current_symbols}")
    if list_to_string == "" or list_to_string == None:
        await bot.send_message(text="<b>•Current Symbols:</b>\n`None`", chat_id=event.chat.id)
    else:
        await bot.send_message(text=f"<b>•Current Symbols:</b>\n`{list_to_string}`", chat_id=event.chat.id)
    input_symbols = Symb_Config.extractor.extract(event.text)
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
        if list_to_string == "" or list_to_string is None:
            await bot.send_message(text="`•New symbols`\n`None`", chat_id=event.chat.id, reply_to_message_id=event.id)
        else:
            await bot.send_message(text=f"<b>•New symbols:</b>\n`{list_to_string}`", chat_id=event.chat.id,reply_to_message_id=event.id)
    except IOError as e:
        LOGS.error(f"I/O error({e.errno}): {e.strerror}")
    except:
        LOGS.error(f"Unexpected error: {sys.exc_info()[0]}")


@register(incoming=True, pattern=r"^\.blacklist(?: |$)(.*)")
async def handler(event: pyrogram.types.Message):
    await bot.send_chat_action(chat_id=event.chat.id, action=ChatAction.TYPING)
    list_to_string = '\n'.join(BlacklistWords.WORDS_TO_EXCLUDE)
    await bot.send_message(text=f"<b>•Blacklist:</b>\n<code>{list_to_string} </code>", chat_id=event.chat.id, reply_to_message_id=event.id)



pattern_blacklist=r'^\.blacklistignore(?: |$)(.*)$'
@register(incoming=True, pattern=pattern_blacklist)
async def handler(event: pyrogram.types.Message):
    LOGS.info(f"---Trying to change blacklist---")

    await bot.send_chat_action(chat_id=event.chat.id, action=ChatAction.TYPING)
    matches = re.findall(pattern_blacklist, event.text, re.IGNORECASE|re.MULTILINE|re.DOTALL)
    matches= matches[0].split(' ')
    #removing '' strings from list
    matches=[x for x in matches if x]
    if len(matches)>0:
        LOGS.info(f"Opening file {BlacklistWords.path} to save input_words: {matches}")
        try:
            with open(BlacklistWords.path, "w") as f:
                for match in matches:
                    f.write(f"{match}\n")

        except IOError as e:
            LOGS.error(f"I/O error({e.errno}): {e.strerror}")
        except:
            LOGS.error(f"Unexpected error: {sys.exc_info()[0]}")
        else:
            list_to_string = '\n'.join(BlacklistWords.WORDS_TO_EXCLUDE)
            await bot.send_message(text=f"<b>•Old blacklist:</b>\n<code>{list_to_string} </code>", chat_id=event.chat.id)
            BlacklistWords.WORDS_TO_EXCLUDE = retrieve_lines_from_file(
                os.path.join(const_dirs_class.CURR_DIR, BlacklistWords.path))
            list_to_string = '\n'.join(BlacklistWords.WORDS_TO_EXCLUDE)

            await bot.send_message(text=f"<b>•New Blacklist:</b>\n <code>{list_to_string}</code>",
                                   chat_id=event.chat.id, reply_to_message_id=event.id)
    else:
        await bot.send_message(text="<b>•Current Blacklist:</b>\n`None`", chat_id=event.chat.id, reply_to_message_id=event.id)
    LOGS.info(f"---END CHANGE blacklist---")







CMD_HELP.update({
    "symbols": "✘ Pʟᴜɢɪɴ : Gets the current symbols to ignore."
               "\n\n⚡𝘾𝙈𝘿⚡: `.symbignore <symbols>`"
               "\n↳ : Updates current symbols to ignore"
               "\n\n⚡𝘾𝙈𝘿⚡: `.getsymbols`"
               "\n↳ : Gets the current symbols that are being ignored"
               "\n\n⚡𝘾𝙈𝘿⚡: `.blacklist `"
               "\n↳ : Gets the current words that are being ignored"
               "\n\n⚡𝘾𝙈𝘿⚡: `.blacklistignore <any_word>`"
               "\n↳ : Ignore an amount of msgs from the input_chat"
})
