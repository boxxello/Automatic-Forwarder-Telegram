import os

import pyrogram

from pyrogram import enums
from pyrogram.enums import ChatAction

import ForwardBot
from ForwardBot import CMD_HELP,  bot
from ForwardBot.events import register
from ForwardBot.plugins.misc import extract_user, edit, download_media_wc
from ForwardBot.plugins.replier import reply_img


@register(incoming=True, pattern='^.whois')
async def who_is( message : pyrogram.types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    find_user = await extract_user(message)
    reply = message.reply_to_message

    if len(find_user) < 1:
        return  await bot.send_message(reply_to_message_id=message.id,text= f'`"banFailUser"`', chat_id=message.chat.id)



    for reply_user in find_user:
        try:

            reply_chat = await bot.get_chat( reply_user.id)
            ForwardBot.LOGS.info("test2")
        except Exception:
            return await  bot.send_message(reply_to_message_id=message.id,text='`"whoisError"`', chat_id=message.chat.id)
        if reply_user or reply_chat is not None:
            try:

                user_photo = reply_user.photo.big_file_id
                photo = await download_media_wc(user_photo, 'photo.png')
            except BaseException:
                ForwardBot.LOGS.info("test3")
                photo = None
                pass
            ForwardBot.LOGS.info("Out of the try except")
            first_name = reply_user.first_name or 'notSet'
            last_name = reply_user.last_name or 'notSet'
            username = (
                f'@{reply_user.username}'
                if reply_user.username
                else 'notSet'
            )
            user_id = reply_user.id
            photos = await bot.get_chat_photos_count(user_id)
            dc_id = reply_user.dc_id or 'notSet'
            premium = reply_user.is_premium
            bio = reply_chat.bio or 'notSet'
            status = reply_user.status
            isbot = reply_user.is_bot
            last_seen = LastSeen(isbot, status)
            sudo = await SudoCheck(user_id)
            chats = len(await bot.get_common_chats(user_id))

            caption = 'WhoisResult'+'\n'+'First Name: `'+first_name+'`'+'\n'+'LastName: `'\
                      +last_name+'`'+'\n'+'Username` '\
                      +username+'`'+'\n'+'User ID: `'\
                      +str(user_id)+'`'\
                      +'\n'+'N° photos: `'  +str(photos)+'`'+'\n'\
                      +'`Assigned Data Center' +str(dc_id)+'`'+'\n'\
                      +'Is premium: `' +str(premium)+'`'+'\n'\
                      +'BIO desc: `'+str(bio)+'`'+'\n'\
                      +'Status: `'+str(status)+'`'+'\n'\
                      +'Last seen: `'+str(last_seen)+'`'+'\n'+\
                      'Sudo status: `'+str(sudo)+'`'+'\n'+\
                      'Chats we got in common: `'+str(chats)+'`'

    if photo:

        await reply_img(reply or message,
                  photo, caption=caption, delete_file=True)

    else:

        return await bot.send_message(reply_to_message_id=message.id,text= caption, chat_id=message.chat.id)

def LastSeen(bot, status):
    if bot:
        return 'BOT'
    elif status == enums.UserStatus.ONLINE:
        return 'statusOnline'
    elif status == enums.UserStatus.OFFLINE:
        return 'statusOffline'
    elif status == enums.UserStatus.RECENTLY:
        return 'statusRecently'
    elif status == enums.UserStatus.LAST_WEEK:
        return 'statusWeek'
    elif status == enums.UserStatus.LAST_MONTH:
        return 'statusMonth'
    elif status == enums.UserStatus.LONG_AGO:
        return 'statusLong'

async def SudoCheck(user_id):
    if user_id in ForwardBot.Config.SUDO_USERS_INT:
        return 'sudoCheck'
CMD_HELP.update({
    "whois":
    ">`.whois <username>`"
    "\nInfo: Gets the  information of the specified user."
})
