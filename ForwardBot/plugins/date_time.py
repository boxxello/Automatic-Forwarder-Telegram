import re
from datetime import datetime as dt

from pyrogram.enums import ChatAction
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from ForwardBot import CMD_HELP, COUNTRY, TZ_NUMBER, bot
from ForwardBot.events import register

time_regex=r"^.time(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?"
date_regex=r"^.date(?: |$)(.*)(?<![0-9])(?: |$)([0-9]+)?"
async def get_tz(con):
    """ Get time zone of the given country. """
    if "(Uk)" in con:
        con = con.replace("Uk", "UK")
    if "(Us)" in con:
        con = con.replace("Us", "US")
    if " Of " in con:
        con = con.replace(" Of ", " of ")
    if "(Western)" in con:
        con = con.replace("(Western)", "(western)")
    if "Minor Outlying Islands" in con:
        con = con.replace("Minor Outlying Islands", "minor outlying islands")
    if "Nl" in con:
        con = con.replace("Nl", "NL")

    for c_code in c_n:
        if con == c_n[c_code]:
            return c_tz[c_code]
    try:
        if c_n[con]:
            return c_tz[con]
    except KeyError:
        return


@register(incoming=True, pattern=time_regex)
async def time_func(tdata):
    """ For .time command, return the time of
        1. The country passed as an argument,
        2. The default userbot country,
        3. The server where the userbot runs.
    """
    await bot.send_chat_action(chat_id=tdata.chat.id, action=ChatAction.TYPING)
    m=re.search(time_regex,tdata.text)
    con = m.group(1).title()
    tz_num = m.group(2)

    t_form = "%H:%M"
    c_name = None

    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif COUNTRY:
        c_name = COUNTRY
        tz_num = TZ_NUMBER
        timezones = await get_tz(COUNTRY)
    else:
        await bot.send_message(text=f"`It's`  **{dt.now().strftime(t_form)}**  `here.`", chat_id=tdata.chat.id)
        return

    if not timezones:
        await bot.send_message(text="`Invaild country.`", chat_id=tdata.chat.id)
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} has multiple timezones:`\n\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Choose one by typing the number "
            return_str += "in the command.`\n"
            return_str += f"`Example: .time {c_name} 2`"

            await bot.send_message(text=return_str, chat_id=tdata.chat.id)
            return

    dtnow = dt.now(tz(time_zone)).strftime(t_form)

    if c_name != COUNTRY:
        await bot.send_message(text=
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`", chat_id=tdata.chat.id)
        return

    elif COUNTRY:
        await bot.send_message(text=f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                         f"({time_zone} timezone).`", chat_id=tdata.chat.id)
        return


@register(incoming=True, pattern=date_regex)
async def date_func(dat):
    """ For .date command, return the date of
        1. The country passed as an argument,
        2. The default userbot country(set it by using .settime),
        3. The server where the userbot runs.
    """
    await bot.send_chat_action(chat_id=dat.chat.id, action=ChatAction.TYPING)
    m=re.search(date_regex,dat.text)

    con = m.group(1).title()
    tz_num = m.group(2)

    d_form = "%d/%m/%y - %A"
    c_name = ''

    if len(con) > 4:
        try:
            c_name = c_n[con]
        except KeyError:
            c_name = con
        timezones = await get_tz(con)
    elif COUNTRY:
        c_name = COUNTRY
        tz_num = TZ_NUMBER
        timezones = await get_tz(COUNTRY)
    else:
        await bot.send_message(text=f"`It's`  **{dt.now().strftime(d_form)}**  `here.`", chat_id=dat.chat.id)
        return

    if not timezones:
        await bot.send_message("`Invaild country.`")
        return

    if len(timezones) == 1:
        time_zone = timezones[0]
    elif len(timezones) > 1:
        if tz_num:
            tz_num = int(tz_num)
            time_zone = timezones[tz_num - 1]
        else:
            return_str = f"`{c_name} has multiple timezones:`\n"

            for i, item in enumerate(timezones):
                return_str += f"`{i+1}. {item}`\n"

            return_str += "\n`Choose one by typing the number "
            return_str += "in the command.`\n"
            return_str += f"Example: .date {c_name} 2"

            await bot.send_message(text=return_str, chat_id=dat.chat.id)
            return

    dtnow = dt.now(tz(time_zone)).strftime(d_form)

    if c_name != COUNTRY:
        await bot.send_message(
            f"`It's`  **{dtnow}**  `in {c_name}({time_zone} timezone).`", chat_id=dat.chat.id)
        return

    elif COUNTRY:
        await bot.send_message(text=f"`It's`  **{dtnow}**  `here, in {COUNTRY}"
                       f"({time_zone} timezone).`", chat_id=dat.chat.id)
        return


CMD_HELP.update({
    "timedate":
    "`.time` <country name/code> <timezone number>\
\nUsage: Usage: Get the time of a country. If a country has multiple timezones, it will list all of them and let you select one.\
\n\n`.date` <country name/code> <timezone number>\
\nUsage: Get the date of a country. If a country has multiple timezones, it will list all of them and let you select one."
})
