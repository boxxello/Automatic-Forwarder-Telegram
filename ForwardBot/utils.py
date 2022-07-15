from telethon import events

from ForwardBot import Config, bot

bothandler = Config.COMMAND_HAND_LER
def forwardbot_cmd(add_cmd, is_args=False):
    def cmd(func):
        if is_args:
            pattern = bothandler + add_cmd + "(?: |$)(.*)"
        else:
            pattern = bothandler + add_cmd + "$"
        bot.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )
    return cmd

async def is_sudo(event):
    if str(event.sender_id) in Config.SUDO_USERS_INT:
        return True
    else:
        return False