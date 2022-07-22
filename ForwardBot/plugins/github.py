import re

import aiohttp
import pyrogram.types
from pyrogram.enums import ChatAction

from ForwardBot.events import register
from ForwardBot import CMD_HELP, bot

regex_exp = r"^\.github (.*)"
@register(pattern=regex_exp, incoming=True)
async def github(event : pyrogram.types.Message):
    await bot.send_chat_action(chat_id=event.chat.id, action=ChatAction.TYPING)
    match=re.search(regex_exp, event.text)
    URL = f"https://api.github.com/users/{match.group(1)}"

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await bot.send_message(text="`" + match.group(1) +
                                         " user not found or couldn't make the get request!`", chat_id=event.chat.id)


            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"GitHub Info for user `{match.group(1)}`"
                f"\nUsername: `{name}`\nBiography: `{bio}`\nURL: {url}"
                f"\nCompany: `{company}`\nCreated at: `{created_at}`"
            )

            if not result.get("repos_url", None):
                return await bot.send_message(text=REPLY, chat_id=event.chat.id)
            async with session.get(result.get("repos_url", None)) as request:
                if request.status == 404:
                    return await bot.send_message(text=REPLY, chat_id=event.chat.id)

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await bot.send_message(text=REPLY, chat_id=event.chat.id)


CMD_HELP.update({
    "github":
    ">`.github <username>`"
    "\nInfo: gets the GitHub profile info"
})
