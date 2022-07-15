import asyncio

from ForwardBot import CMD_HELP, bot, Config
from ForwardBot.events import register

from platform import uname


modules = CMD_HELP


DEFAULTUSER = str(Config.ALIVE_NAME) if Config.ALIVE_NAME else uname().node


@register(incoming=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await bot.send_message(message=str(CMD_HELP[args]), entity=event.chat_id)
        else:
            await asyncio.sleep(200)
            await event.delete()
    else:
        string = ""

        for idx,i in enumerate(CMD_HELP):
            string += "`" + str(i)
            string += "`\t|  "

        msg_icon=await bot.send_message(message="⚡", entity=event.chat_id)
        await asyncio.sleep(3)
        await bot.edit_message(message=msg_icon,text="**Forward Bot**\n\n"
                         f"**Hosted on {DEFAULTUSER} Operating sys: {Config.HOSTING_OP_SYSTEM}**\n**Loaded modules: {len(modules)}**\n\n"
                         "• **Main menu :**\n"                                                                                                                                                                                                                                                                                       
                         f"╰►| {string} ⋖╯\n\n", entity=event.chat_id)
        await asyncio.sleep(1000)
        await event.delete()
