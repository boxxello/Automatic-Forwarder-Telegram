import os
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from ForwardBot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from ForwardBot.events import register


@register(pattern=".whois(?: |$)(.*)", incoming=True)
async def who(event):

    new_msg=await bot.send_message(message=
        "`Get request to the TG Servers started...`", entity=event.chat_id)

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        return new_msg.edit("`Couldn't get any info about this user`")

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        resp=await bot.send_file(event.chat_id,
                                     photo,
                                     caption=caption,
                                     link_preview=False,
                                     force_document=False,
                                     reply_to=message_id_to_reply,
                                     parse_mode="html")

        if not photo.startswith("http"):
            os.remove(photo)
        await event.delete()

    except TypeError:
        await resp.edit(caption, parse_mode="html")


async def get_user(event):
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return replied_user


async def fetch_info(replied_user, event):
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.user.id,
                             offset=42,
                             max_id=0,
                             limit=80))
    replied_user_profile_photos_count = "No profile picture"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    common_chat = replied_user.common_chats_count
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    photo = await event.client.download_profile_photo(user_id,
                                                      TEMP_DOWNLOAD_DIRECTORY +
                                                      str(user_id) + ".jpg",
                                                      download_big=True)
    first_name = first_name.replace(
        "\u2060", "") if first_name else ("No firstName")
    last_name = last_name.replace(
        "\u2060", "") if last_name else ("No lastName")
    username = "@{}".format(username) if username else (
        "He hasn't got an username")
    user_bio = user_bio if user_bio else ("No bio available")

    caption = f"<b>Info about user - {username} -</b>\n\n"
    caption += f"First name: {first_name}\n"
    caption += f"Last name: {last_name}\n"
    caption += f"Username: {username}\n"
    caption += f"Number of profile pics: {replied_user_profile_photos_count}\n"
    caption += f"Is Bot: {is_bot}\n"
    caption += f"Is he restricted: {restricted}\n"
    caption += f"Is he verified: {verified}\n"
    caption += f"ID: <code>{user_id}</code>\n\n"
    caption += f"Biography: \n<code>{user_bio}</code>\n\n"
    caption += f"Number of chats we have in common: {common_chat}\n"
    caption += f"Permanent link to the profile: <a href=\"tg://user?id={user_id}\">{first_name}</a>"

    return photo, caption


CMD_HELP.update({
    "whois":
    ">`.whois <username>`"
    "\nInfo: Gets the userinfo"
})
