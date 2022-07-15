import subprocess
import sys
from asyncio import create_subprocess_shell
from time import strftime, gmtime
from traceback import format_exc

from telethon import events

from ForwardBot import bot, Config, LOGS


def register(**args):

    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    ignore_unsafe = args.get('ignore_unsafe', False)
    unsafe_pattern = r'^[^/!#@\$A-Za-z]'

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern


    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if pattern:
        if not ignore_unsafe:
            args['pattern'] = pattern.replace('^.', unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(check):
            if str(check.sender_id) not in Config.SUDO_USERS_INT:
                LOGS.info(f"{str(check.sender_id)} tried to send a command, but he's not a sudo user")
                return
            if check.edit_date and check.is_channel and not check.is_group:
                return
            else:
                pass

            try:
                await func(check)

            except events.StopPropagation:
                raise events.StopPropagation

            except KeyboardInterrupt:
                pass
            except BaseException:


                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())


                ftext = "--------BEGIN USERBOT TRACEBACK LOG--------\n"
                ftext += "\nDate: " + date
                ftext += "\nChat ID: " + str(check.chat_id)
                ftext += "\nSender ID: " + str(check.sender_id)
                ftext += "\n\nEvent Trigger:\n"
                ftext += str(check.text)
                ftext += "\n\nTraceback info:\n"
                ftext += str(format_exc())
                ftext += "\n\nError text:\n"
                ftext += str(sys.exc_info()[1])
                ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                LOGS.error(ftext)

            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper
    return decorator
