# Copyright (C) 2020-2022 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from os import makedirs
from re import escape, sub
from subprocess import STDOUT, CalledProcessError, check_output
from typing import List

from pyrogram import enums
from pyrogram.types import Message, User

import ForwardBot

MARKDOWN_FIX_CHAR = '\u2064'
SPAM_COUNT = [0]
_parsed_prefix = escape(ForwardBot.Config.BOT_PREFIX) if ForwardBot.Config.BOT_PREFIX else r'\.'
_admin_status_list = [
    enums.ChatMemberStatus.OWNER,
    enums.ChatMemberStatus.ADMINISTRATOR,
]
def reply(
    message,
    text,
    preview=True,
    fix_markdown=False,
    delete_orig=False,
    parse=enums.ParseMode.MARKDOWN,
):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        ret = message.reply_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
        if delete_orig:
            message.delete()
        return ret
    except BaseException:
        pass


def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ''

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if ' ' not in text:
        return ''

    text = sub(r'\s+', ' ', text)
    text = text[text.find(' ') :].strip()
    return text


def extract_args_arr(message, markdown=True):
    return extract_args(message, markdown).split()


async def edit(
    message, text, preview=True, fix_markdown=False, parse=enums.ParseMode.MARKDOWN
):
    try:
        if fix_markdown:
            text += MARKDOWN_FIX_CHAR
        await message.edit_text(
            text.strip(), disable_web_page_preview=not preview, parse_mode=parse
        )
    except BaseException:
        pass


async def download_media(client, data, file_name=None, progress=None, sticker_orig=True):
    if not file_name:
        if data.document:
            file_name = (
                data.document.file_name
                if data.document.file_name
                else f'{data.document.file_id}.bin'
            )
        elif data.audio:
            file_name = (
                data.audio.file_name
                if data.audio.file_name
                else f'{data.audio.file_id}.mp3'
            )
        elif data.photo:
            file_name = f'{data.photo.file_id}.png'
        elif data.voice:
            file_name = f'{data.voice.file_id}.ogg'
        elif data.video:
            file_name = (
                data.video.file_name
                if data.video.file_name
                else f'{data.video.file_id}.mp4'
            )
        elif data.animation:
            file_name = f'{data.animation.file_id}.mp4'
        elif data.video_note:
            file_name = f'{data.video_note.file_id}.mp4'
        elif data.sticker:
            file_name = f'sticker.{("tgs" if sticker_orig else "json.gz") if data.sticker.is_animated else "webm" if data.sticker.is_video else "webp" if sticker_orig else "png"}'
        else:
            return None

    if progress:
        return await client.download_media(data, file_name=file_name, progress=progress)

    return await client.download_media(data, file_name=file_name)


async def download_media_wc(data, file_name=None, progress=None, sticker_orig=False):
    return await download_media(ForwardBot.bot, data, file_name, progress, sticker_orig)


def get_me():
    return ForwardBot.bot.get_me()


def forward(message, chat_id):
    try:
        return message.forward(chat_id or 'me')
    except Exception as e:
        raise e


def get_messages(chat_id, msg_ids=None, client=ForwardBot.bot):
    try:
        ret = client.get_messages(chat_id=(chat_id or 'me'), message_ids=msg_ids)
        return [ret] if ret and isinstance(ret, Message) else ret
    except BaseException:
        return []






def get_cmd(message):
    text = message.text or message.caption
    if text:
        text = text.strip()
        return parse_cmd(text)
    return ''


def parse_cmd(text):
    cmd = sub(r'\s+', ' ', text)
    cmd = cmd.split()[0]
    cmd = cmd.split(_parsed_prefix)[-1] if ForwardBot.Config.BOT_PREFIX else cmd[1:]
    return cmd




def is_admin(message):
    if not message.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        return True

    user = ForwardBot.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    return user.status in _admin_status_list


def is_admin_myself(chat):
    if not chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
        return True

    user = ForwardBot.bot.get_chat_member(chat_id=chat.id, user_id='me')
    return user.status in _admin_status_list


def get_download_dir() -> str:
    dir = './downloads'
    makedirs(dir, exist_ok=True)
    return dir


def get_duration(media):
    out = __status_out__(
        f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{media}"'
    )
    if out[0] == 0:
        return int(float(out[1]))
    return None


def __status_out__(cmd, encoding='utf-8'):
    try:
        output = check_output(
            cmd, shell=True, text=True, stderr=STDOUT, encoding=encoding
        )
        return (0, output)
    except CalledProcessError as ex:
        return (ex.returncode, ex.output)
    except BaseException as e:
        if encoding != 'latin-1':
            return __status_out__(cmd, 'latin-1')
        raise e


async def extract_user(message: Message) -> List[User]:
    users: List[User] = []
    mentions = None

    if message.text and not mentions:
        try:
            users.append(await message.client.get_users(message.text.split()[1]))
        except BaseException:
            pass

    if message.reply_to_message:
        users.append(message.reply_to_message.from_user)

    if message.entities:
        mentions = [
            entity
            for entity in message.entities
            if entity.type == enums.MessageEntityType.TEXT_MENTION
        ]
        no_username = [
            i.user for i in mentions if i.type == enums.MessageEntityType.TEXT_MENTION
        ]
        users += no_username

        for i in mentions:
            try:
                users.append(
                    await message.client.get_users(
                        message.text[i.offset : i.offset + i.length]
                    )
                )
            except BaseException:
                pass

    return users
