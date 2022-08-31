from os import path, remove

from pyrogram import enums


from ForwardBot.plugins.misc import MARKDOWN_FIX_CHAR, __status_out__, get_duration
from pyrogram.types import Message

async def reply_img(
    message: Message,
    photo,
    caption='',
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
    parse=enums.ParseMode.MARKDOWN,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        await message.reply_photo(photo, caption=caption.strip(), parse_mode=parse)
        if delete_orig:
            await message.delete()
        if delete_file:
            remove(photo)
    except BaseException:
        pass


async def reply_audio(
    message,
    audio,
    caption='',
    duration=None,
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR

        if not duration:
            duration = get_duration(audio)

        await message.reply_audio(audio, caption=caption.strip(), duration=int(duration))
        if delete_orig:
            await message.delete()
        if delete_file:
            remove(audio)
    except BaseException:
        pass


async def reply_video(
    message,
    video,
    caption='',
    duration='',
    thumb=None,
    fix_markdown=False,
    progress=None,
    delete_orig=False,
    delete_file=False,
    parse=enums.ParseMode.MARKDOWN,
):
    try:
        if not thumb:
            thumb = 'downloads/thumb.png'
            if path.exists(thumb):
                remove(thumb)
            out = __status_out__(
                f'ffmpeg -i {video} -ss 00:00:01.000 -vframes 1 {thumb}'
            )

            if out[0] != 0:
                thumb = None

        if not duration:
            duration = get_duration(video)

        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if not duration:
            await message.reply_video(
                video,
                caption=caption.strip(),
                parse_mode=parse,
                thumb=thumb,
                progress=progress,
            )
        else:
            await message.reply_video(
                video,
                caption=caption.strip(),
                duration=int(duration),
                parse_mode=parse,
                thumb=thumb,
                progress=progress,
            )
        if delete_orig:
            await message.delete()
        if delete_file:
            remove(video)
    except BaseException as e:
        raise e
        pass


async def reply_voice(
    message,
    voice,
    caption='',
    duration=None,
    fix_markdown=False,
    delete_orig=False,
    delete_file=False,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR

        if not duration:
            duration = get_duration(voice)

        await message.reply_voice(voice, caption=caption.strip(), duration=duration)
        if delete_orig:
            await message.delete()
        if delete_file:
            remove(voice)
    except BaseException:
        pass


async def reply_doc(
    message,
    doc,
    caption='',
    fix_markdown=False,
    delete_orig=False,
    progress=None,
    delete_after_send=False,
):
    try:
        if len(caption) > 0 and fix_markdown:
            caption += MARKDOWN_FIX_CHAR
        if isinstance(doc, str):
            await message.reply_document(doc, caption=caption.strip(), progress=progress)
            if delete_after_send:
                remove(doc)
        else:
            await message.reply_media_group(doc)
            if delete_after_send:
                for media in doc:
                    remove(media.media)
        if delete_orig:
            message.delete()
    except Exception as e:
        raise e


async def reply_sticker(message, sticker, delete_orig=False, delete_file=False):
    try:
        await message.reply_sticker(sticker)
        if delete_orig:
            await message.delete()
        if delete_file:
            remove(sticker)
    except BaseException:
        pass


async def reply_msg(message: Message, message2: Message, delete_orig=False):
    try:
        await message2.copy(chat_id=message.chat.id, reply_to_message_id=message.id)
        if delete_orig:
            await message.delete()
    except Exception as e:
        raise e