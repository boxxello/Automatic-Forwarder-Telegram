
import asyncio
import zipfile
from ForwardBot.events import register
from datetime import date
import time
import os
from ForwardBot import TEMP_DOWNLOAD_DIRECTORY, ZIP_DOWNLOAD_DIRECTORY, bot, CMD_HELP, LOGS
from ForwardBot.utils import progress

# ====================
today = date.today()
# ====================


@register(incoming=True, pattern=r"^\.compress(?: |$)(.*)")
async def _(event):
    # Prevent Channel Bug to use update
    if event.is_channel and not event.is_group:
        await bot.send_message(message="`Compress Command isn't permitted on channels`", entity=event.chat_id)
        return
    if event.fwd_from:
        return
    if not event.is_reply:
        await bot.send_message(message="`Reply to a file to compress it.`", entity=event.chat_id)
        return
    mone = await bot.send_message(message="`Processing...`", entity=event.chat_id)
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "[DOWNLOADING]")
                ),
            )
            directory_name = downloaded_file_name
            await bot.send_message(message=
                f"Downloaded to `{directory_name}`" "`\ncompressing file...`", entity=event.chat_id
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED).write(
        directory_name
    )
    c_time = time.time()
    await bot.send_file(
        event.chat_id,
        directory_name + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, mone, c_time, "[UPLOADING]")
        ),
    )
    await bot.send_message(message="`Done!!`", entity=event.chat_id)
    await asyncio.sleep(7)
    await event.delete()


@register(incoming=True, pattern=r"^\.addzip(?: |$)(.*)")
async def addzip(event):
    # Prevent Channel Bug to use update
    if event.is_channel and not event.is_group:
        await bot.send_message("`Command isn't permitted on channels`", event=event.chat_id)
        return
    if event.fwd_from:
        return
    if not event.is_reply:
        await bot.send_message(message="`Reply to a file to compress it.`", event=event.chat_id)
        return
    mone = await bot.send_message(message="`Processing...`", event=event.chat_id)

    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        os.makedirs(ZIP_DOWNLOAD_DIRECTORY)
        LOGS.info(f"{ZIP_DOWNLOAD_DIRECTORY} was just created")
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                reply_message,
                ZIP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "[DOWNLOADING]")
                ),
            )
            success = str(downloaded_file_name).replace("./zips/", "")
            await bot.send_message(message=f"`{success} Successfully added to list`", entity=event.chat_id)
        except Exception as e:
            await mone.edit(str(e))
            return


@register(incoming=True, pattern=r"^\.upzip(?: |$)(.*)")
async def upload_zip(event):
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        await bot.send_message(message="`Files not found`", entity=event.chat_id)
        return
    mone = await bot.send_message(message="`Zipping File...`", entity=event.chat_id)
    input_str = event.pattern_match.group(1)
    curdate = today.strftime("%m%d%y")
    title = str(input_str) if input_str else "zipfile" + f"{curdate}"
    zipf = zipfile.ZipFile(title + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(ZIP_DOWNLOAD_DIRECTORY, zipf)
    zipf.close()
    c_time = time.time()
    await bot.send_file(
        event.chat_id,
        title + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=up.message.id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, mone, c_time, "[UPLOADING]", input_str)
        ),
    )
    try:
        for root, dirs, files in os.walk(ZIP_DOWNLOAD_DIRECTORY, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    except Exception as e:
        LOGS.info(e)
    await event.delete()


@register(incoming=True, pattern=r"^\.rmzip(?: |$)(.*)")
async def remove_dir(event):
    LOGS.debug("rmzip started")
    if not os.path.isdir(ZIP_DOWNLOAD_DIRECTORY):
        await bot.send_message(message="`Directory not found`", entity=event.chat_id)
        return
    LOGS.info(f"removing dir {ZIP_DOWNLOAD_DIRECTORY}")
    try:
        for root, dirs, files in os.walk(ZIP_DOWNLOAD_DIRECTORY, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        await bot.send_message(message="`Zip list removed`", entity=event.chat_id)
    except Exception as e:
        LOGS.info(e)
        await bot.send_message(message="`Zip list not removed, an error occurred", entity=event.chat_id)



def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))


CMD_HELP.update({
    "zipfile":
        "`.compress` **[optional: <reply to file>]**\
            \nUsage: make files to zip.\
            \n`.addzip` **<reply to file>**\
            \nUsage: add files to zip list.\
            \n`.upzip` **[optional: <zip title>]**\
            \nUsage: upload zip list.\
            \n`.rmzip` **[optional: <zip title>]**\
            \nUsage: clear zip list."
})
