import asyncio
import json

import os
import pickle

import sys
from datetime import datetime
from uuid import uuid4

import motor.motor_asyncio
import pymongo
import pyrogram.types
from bson import Binary
from pyrogram import Client as TelegramClient

from pymongo.errors import ConnectionFailure
from pyrogram.enums import MessageEntityType

import ForwardBot
from ForwardBot.logger import get_logger_no_file_h, get_logger
from ForwardBot.BotConfig import Config
from ForwardBot.const_dirs import const_dirs_class

const_values = const_dirs_class()
const_values.make_dir()

get_logger_no_file_h("")
if ForwardBot.Config.OUTPUT_LOGS_TO_FILE:
    LOGS = get_logger("Telegram", "telegram")

else:
    LOGS = get_logger_no_file_h("Telegram")

CHANNEL_CLIENT_ID = None
CHANNEL_NAME_CLIENT = os.environ.get("CHANNEL_NAME_CLIENT", "")
if Config.API_ID is None:
    LOGS.info("API_ID is None. Exiting...")
    sys.exit(-1)
if Config.API_HASH is None:
    LOGS.info("API_HASH is None. Exiting...")
    sys.exit(-2)

if Config.CELLPHONE_NUMBER is None:
    LOGS.info("STRING_SESSION_CLIENT is None, Defaulting to 'userbot'")
    if Config.SESSION_NAME_CLIENT is None:
        bot = TelegramClient(name="userbot", api_id=Config.API_ID, api_hash=Config.API_HASH)
    else:
        bot = TelegramClient(name=Config.SESSION_NAME_CLIENT, api_id=Config.API_ID, api_hash=Config.API_HASH)

else:
    bot = TelegramClient(name="userbot", api_id=Config.API_ID, api_hash=Config.API_HASH,
                         phone_number=Config.CELLPHONE_NUMBER)

COUNTRY = str(os.environ.get("COUNTRY", "ID"))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

if Config.SUDO_USERS_INT is None:
    LOGS.info("SUDO_USERS is None. Exiting...")
    sys.exit(1)


async def set_chat_id(bot: TelegramClient, channel_name: str) -> int:
    async for dialog in bot.get_dialogs():
        print(f"{dialog.chat.title} checking with:  {channel_name}")
        if dialog.chat.title:
            if all([x in dialog.chat.title for x in channel_name.split(" ")]):
                print("QUALCOSA SUCCEDE")
                channel_id = dialog.chat.id
                LOGS.info(f"{channel_name} chat found.")
                return channel_id
    LOGS.warning(f"{Config.CHANNEL_NAME_CLIENT} chat not found.")
    sys.exit()


def unwrap_dict(obj, classkey=None):
    LOGS.info("VENGO CHIAMATA")
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = unwrap_dict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return unwrap_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [unwrap_dict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if not key.startswith("_") and not callable(value):
                data[key] = unwrap_dict(value, classkey)

        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S%z")
    else:
        return obj


with bot:
    try:
        # LOGS.info(Config.CHANNEL_NAME_CLIENT)
        Config.CLIENT_CHANNEL_ID = bot.loop.run_until_complete(set_chat_id(bot, Config.CHANNEL_NAME_CLIENT))
    except BaseException as e:
        LOGS.info(
            "CHANNEL_NAME_CLIENT environment variable isn't a "
            "valid entity. Check your environment file.")
        LOGS.info(e)
        quit(1)
with bot:
    try:
        # LOGS.info(Config.CHANNEL_NAME_BOT)
        Config.BOT_CHANNEL_ID = bot.loop.run_until_complete(set_chat_id(bot, Config.CHANNEL_NAME_BOT))
    except BaseException as e:
        LOGS.info(
            "CHANNEL_NAME_BOT environment variable isn't a "
            "valid entity. Check your environment file.")
        LOGS.info(e)
        quit(1)

with bot:
    try:
        Config.PING_CHANNEL_ID = bot.loop.run_until_complete(set_chat_id(bot, Config.CHANNEL_NAME_PING))
    except BaseException as e:
        LOGS.info(
            "PING_CHANNEL_ID environment variable isn't a "
            "valid entity. Check your environment file.")
        LOGS.info(e)
        quit(1)

CMD_HELP = {}

client = motor.motor_asyncio.AsyncIOMotorClient(BotConfig.Config.CONNECTION_STRING)

try:
    client.server_info()
except ConnectionFailure:
    LOGS.error(f"Database connection Error {e}")
    LOGS.error("No connection could be made because the target machine actively refused it ")
    exit(-99)
LOGS.info("Database connected")
db = client['mongodb_pyrogram']
collection = db['miacollezione']
collezione_fw = db['collezione_fw']
collezione_get = db['collezione_get']
collezione_get.create_index([("id", pymongo.ASCENDING)], unique=True)

LOGS.info(f"Db name {db.name}, collection names {bot.loop.run_until_complete(db.list_collection_names())}")


# cursor = collezione_get.find({})
# for document in cursor:
#     if document['_id'] is not None:
#         LOGS.info(f"DOCUMENTO {document}")

# async def get_all_messages_to_db():
#     message_dict = {}
#     async for message in bot.get_chat_history(chat_id=Config.CLIENT_CHANNEL_ID):
#         if isinstance(message, pyrogram.types.Message):
#             # LOGS.info(message)
#             # LOGS.info(type(message))
#             message_dict = unwrap_dict(message)
#         # LOGS.info(message_dict)
#         await collezione_get.update_one(filter={"id": message_dict.get('id')}, update={'$setOnInsert': message_dict},
#                                         upsert=True)
async def get_all_messages_to_db():
    async for message in bot.get_chat_history(chat_id=Config.CLIENT_CHANNEL_ID):
        if isinstance(message, pyrogram.types.Message):
            # LOGS.info(message)
            # LOGS.info(type(message))

            # message_dict = str(message)
            # LOGS.info(type(message_dict))
            # message_obj_json = json.loads(message_dict)
            # LOGS.info(message_obj_json)
            # LOGS.info(type(message_obj_json))

            repr_message = repr(message)
            #LOGS.info(repr_message)
            #LOGS.info(type(repr_message))
            pickled_obj = pickle.dumps(message)
            #LOGS.info(pickled_obj)
            #LOGS.info(type(pickled_obj))

            # await collezione_get.insert_one({'id': message.id, 'data': pickled_obj})
            #update the value of the data
            await collezione_get.update_one(filter={"id": message.id}, update={'$set': {'data': pickled_obj}},upsert=True)
            # #find the document
            # document = await collezione_get.find_one({"id": message.id})
            # #get the data from it
            # data = document['data']
            # #unpickle the data
            # unpickled_obj = pickle.loads(data)
            # LOGS.info(unpickled_obj.id)

        # LOGS.info(message_dict)


#
with bot:
    try:
        LOGS.info(f"Attempting to retrieve old previous messages from chat {Config.CHANNEL_NAME_CLIENT}")
        bot.loop.run_until_complete(get_all_messages_to_db())
    except BaseException as e:
        LOGS.info(
            f"Couldn't get all the previous messages from chat {Config.CHANNEL_NAME_CLIENT}")
        LOGS.info(e)
        quit(1)
