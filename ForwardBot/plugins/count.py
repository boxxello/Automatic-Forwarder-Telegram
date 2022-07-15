import telethon
from ForwardBot import bot, collezione_fw, CMD_HELP, collezione_get, LOGS
from ForwardBot.events import register



@register(incoming=True, pattern=r"^\.count(?: |$)(.*)")
async def handler(event: telethon.events.newmessage):
    count = 0
    chat = await event.get_input_chat()
    cursor = collezione_fw.find({})
    async for document in cursor:
        if document['_id'] is not None:
            count += 1
    text_message = f"`Number of messages that got forwarded is {count}`"
    await bot.send_message(message=text_message, entity=chat)


CMD_HELP.update({
    "count":
        "⚡𝘾𝙈𝘿⚡: `.count`"
        "\n↳ : Gets the number of forwarded messages until now."
})


# @register(outgoing=True, pattern=r"^\.tt$")
# async def handler(event: telethon.events.newmessage):
#     try:
#         cursor = collezione_get.find({})
#         for idx,document in enumerate(cursor):
#             if document['_id'] is not None:
#                 await send_msg_if_pattern_match(document['message'], document['id'])
#             LOGS.info(f"DOCUMENT NUMBER {idx}")
#
#     except Exception as e:
#         LOGS.error(e)
# CMD_HELP.update({
#     "tt":
#         "⚡𝘾𝙈𝘿⚡: `.tt`"
#         "\n↳ : Gets the number of forwarded messages until now."
# })