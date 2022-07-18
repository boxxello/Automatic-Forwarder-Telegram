import pyrogram
from speedtest import Speedtest


from ForwardBot import LOGS, bot, CMD_HELP
from ForwardBot.events import register
from ForwardBot.utils import humanbytes


@register(incoming=True, pattern=r"^\.speedtest$", group=12)
async def speedtest(event:  pyrogram.types.Message):

    await bot.send_message(text="`Running speed test...`", chat_id=event.chat.id)
    try:
        test = Speedtest()
        test.get_best_server()
        test.download()
        test.upload()

        result = test.results.dict()

        msg = (
            f"**Started at {result['timestamp']}**\n\n"
            "**Client**\n"
            f"**ISP :** `{result['client']['isp']}`\n"
            f"**Country :** `{result['client']['country']}`\n\n"
            "**Server**\n"
            f"**Name :** `{result['server']['name']}`\n"
            f"**Country :** `{result['server']['country']}`\n"
            f"**Sponsor :** `{result['server']['sponsor']}`\n\n"
            f"**Ping :** `{result['ping']}ms`\n"
            f"**Upload :** `{humanbytes(result['upload'])}/s`\n"
            f"**Download :** `{humanbytes(result['download'])}/s`"
        )

        await bot.send_message(chat_id=event.chat.id, text=msg)
    except Exception as e:
        await bot.send_message(chat_id=event.chat.id, text=f"Error: occurred {e}")

CMD_HELP.update({
    "speedtest":
    "⚡𝘾𝙈𝘿⚡: `.speedtest`"
    "\n↳ : Gets info about the bot Internet speeds."
})



