import aiohttp
from ForwardBot.events import register
from ForwardBot import CMD_HELP, bot


@register(pattern=r".github (.*)", incoming=True)
async def github(event):
    chat = await event.get_input_chat()
    URL = f"https://api.github.com/users/{event.pattern_match.group(1)}"
    await event.get_chat()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await bot.send_message(message="`" + event.pattern_match.group(1) +
                                         " user not found or couldn't make the get request!`", entity=chat)


            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"GitHub Info for user `{event.pattern_match.group(1)}`"
                f"\nUsername: `{name}`\nBiography: `{bio}`\nURL: {url}"
                f"\nCompany: `{company}`\nCreated at: `{created_at}`"
            )

            if not result.get("repos_url", None):
                return await bot.send_message(message=REPLY, entity=chat)
            async with session.get(result.get("repos_url", None)) as request:
                if request.status == 404:
                    return await bot.send_message(message=REPLY, entity=chat)

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await bot.send_message(message=REPLY, entity=chat)


CMD_HELP.update({
    "github":
    ">`.github <username>`"
    "\nInfo: gets the GitHub profile info"
})
