import asyncio
import os
import re
import sys
from time import strftime, gmtime
from traceback import format_exc

import pyrogram
from pyrogram import filters, enums
from pyrogram.errors import FloodWait
from pyrogram.handlers import EditedMessageHandler, MessageHandler, DeletedMessagesHandler
from pyrogram.raw.types import MessageActionContactSignUp

from ForwardBot import bot, Config, LOGS
from ForwardBot.plugins.misc import edit, is_admin, _parsed_prefix



#

def register(**args):
    pattern = args.get('pattern', None)
    outgoing = args.get('outgoing', True)
    incoming = args.get('incoming', False)
    edited = args.get('edited', False)
    disable_notify = args.get('disable_notify', False)
    compat = args.get('compat', True)
    private = args.get('private', True)
    chat_id=args.get('chat_id', None)

    service = args.get('service', False)
    admin = args.get('admin', False)
    if pattern and '.' in pattern[:2]:
        args['pattern'] = pattern = pattern.replace('.', _parsed_prefix, 1)
    if pattern and pattern[-1:] != '$':
        args['pattern'] = pattern = f'{pattern}(?: |$)'

    def msg_decorator(func):
        async def wrap(client, message):
            try:
                if not message.chat.type in [
                    enums.ChatType.CHANNEL,

                ]:
                    if str(message.from_user.id) not in Config.SUDO_USERS_INT:
                        LOGS.info(f"{str(message.from_user.id)} tried to send a command, but he's not a sudo user")
                        await bot.send_message(chat_id=message.chat.id, text="You are not allowed to use this command.")
                        return
                if message.service and not service:
                    return
                if message.service and isinstance(message.action, MessageActionContactSignUp):
                    return
                if message.chat.type == enums.ChatType.BOT:
                    message.continue_propagation()
                if not private and message.chat.type in [
                    enums.ChatType.PRIVATE,
                    enums.ChatType.BOT,
                ]:
                    if not disable_notify:
                        await edit(message, f'`"groupUsage"`')
                    message.continue_propagation()
                if admin and not await is_admin(message):
                    if not disable_notify:
                        await edit(message, f'`Non puoi usare questo comando`')
                    message.continue_propagation()

                if not compat:
                    await func(client, message)
                else:
                    await func(message)
            except FloodWait as e1:
                LOGS.info(f"FloodWait ERROR: {e1}")
                await asyncio.sleep(e1.value)
            except RetardsException:
                try:
                    quit(-10)
                except BaseException:
                    pass
            except (pyrogram.ContinuePropagation, pyrogram.StopPropagation) as c:
                raise c
            except Exception as e:


                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                ftext = "--------BEGIN USERBOT TRACEBACK LOG--------\n"
                ftext += "\nDate: " + date
                ftext += "\nChat ID: " + str(message.chat.id)
                ftext += "\nSender ID: " + str(message.from_user.id if message.from_user else 'Unknown')
                ftext += "\n\nEvent Trigger:\n"
                ftext += str(message.text)
                ftext += "\n\nTraceback info:\n"
                ftext += str(format_exc())
                ftext += "\n\nError text:\n"
                ftext += str(e)
                ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                LOGS.error(ftext)
        filter = None
        if pattern:
            filter = filters.regex(pattern, flags=(re.IGNORECASE|re.MULTILINE))

            if outgoing and not incoming:
                filter &= filters.me
            elif incoming and not outgoing:
                filter &= filters.incoming & ~filters.bot & ~filters.me
        else:
            if outgoing and not incoming:
                filter = filters.me
            elif incoming and not outgoing:
                filter = filters.incoming & ~filters.bot & ~filters.me
            else:
                filter = (filters.me | filters.incoming) & ~filters.bot
        if chat_id:
            filter &= filters.chat(chat_id)

        if edited:
            bot.add_handler(EditedMessageHandler(wrap, filter))
        else:
            if pattern:
                bot.add_handler(MessageHandler(wrap, filter), group=15)
            else:
                bot.add_handler(MessageHandler(wrap, filter))


    return msg_decorator




# def register(**args):
#     pattern = args.get('pattern', None)
#     if pattern and '.' in pattern[:2]:
#         args['pattern'] = pattern = pattern.replace('.', _parsed_prefix, 1)
#     if pattern and pattern[-1:] != '$':
#         args['pattern'] = pattern = f'{pattern}(?: |$)'
#
#     def msg_decorator(func):
#         async def wrap(client, message):
#             try:
#
#
#                 await func(message)
#
#
#             except Exception as e:
#
#                 print(e)
#         filter = None
#         if pattern:
#             filter = filters.regex(pattern)
#
#         bot.add_handler(MessageHandler(wrap, filter))
#
#
#     return msg_decorator

def message_deleted(**args):
    chat_id = args.get('chat_id', None)

    def msg_decorator(func):
        async def wrap(client, message : pyrogram.types.list.List):
            try:
                await func(message)
            except Exception as e:


                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                ftext = "--------BEGIN USERBOT TRACEBACK LOG--------\n"
                ftext += "\nDate: " + date
                for count,message in enumerate(message):
                    ftext += "\nChat ID: " + str(message.chat.id)
                    ftext += "\nMessage ID: " + str(message.id if message.id else 'Unknown')
                ftext += "\n\nEvent Trigger:\n"
                ftext += str(message.text)

                ftext += "\n\nTraceback info:\n"
                ftext += str(format_exc())
                ftext += "\n\nError text:\n"
                ftext += str(e)
                ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                LOGS.error(ftext)

        filter = None
        if chat_id:
            filter = filters.chat(chat_id)
        bot.add_handler(DeletedMessagesHandler(wrap, filter))

    return msg_decorator

class RetardsException(Exception):
    pass
