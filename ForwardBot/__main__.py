from importlib import import_module



from ForwardBot import bot, LOGS
from ForwardBot.plugins import ALL_MODULES
from ForwardBot.utils_no_bot import MODS
INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\nTip: Use Country Code along with number ' \
             '\n or check your phone number and try again !'

try:
    bot.start()
except BaseException:
    LOGS.error(INVALID_PH)
    exit(-3)
for module_name in MODS:
    imported_module= import_module("ForwardBot.utils_no_bot." + module_name)
for module_name in ALL_MODULES:
    imported_module = import_module("ForwardBot.plugins." + module_name)

LOGS.info("Attempting to run bot")
bot.run_until_disconnected()