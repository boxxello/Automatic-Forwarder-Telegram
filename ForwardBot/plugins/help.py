import asyncio
import re

import pyrogram
from pyrogram.enums import ChatAction

from ForwardBot import CMD_HELP, bot, Config
from ForwardBot.events import register

from platform import uname


modules = CMD_HELP


DEFAULTUSER = str(Config.ALIVE_NAME) if Config.ALIVE_NAME else uname().node

help_regex=r"^\.help(?: |$)(.*)"
@register(incoming=True, pattern=help_regex, group=-10)
async def help(event: pyrogram.types.Message):
    await bot.send_chat_action(chat_id=event.chat.id, action=ChatAction.TYPING)
    m=re.search(help_regex,event.text)
    args = m.group(1).lower()
    if args:
        if args in CMD_HELP:
            await bot.send_message(text=str(CMD_HELP[args]), chat_id=event.chat.id)
        else:
            await asyncio.sleep(200)
            await event.delete()
    else:
        string = ""

        for idx,i in enumerate(CMD_HELP):
            string += "`" +'.help '+ str(i)
            string += "`\t|  "

        message_sent=await bot.send_message(text="⚡", chat_id=event.chat.id)

        await asyncio.sleep(3)
        await bot.edit_message_text(message_id=message_sent.id,text="**Forward Bot**\n\n"
                         f"**Hosted on {DEFAULTUSER} Operating sys: {Config.HOSTING_OP_SYSTEM}**\n**Loaded modules: {len(modules)}**\n\n"
                         "• **Main menu of modules :**\n"
                         f"╰►| {string}\n\n<b>By picking one you will see all the commands in the module</b>", chat_id=event.chat.id)

        await asyncio.sleep(1000)
        await event.delete()
