import pickle
import re
from typing import Optional

import pyrogram

from pyrogram.types import MessageEntity

from ForwardBot import bot, Config, LOGS, collezione_get, collezione_fw,  BotConfig
from ForwardBot.SymbConfig import Symb_Config, BlacklistWords
from ForwardBot.events import register, message_deleted

@register(incoming=True, chat_id=Config.CLIENT_CHANNEL_ID)
async def handler(event: pyrogram.types.Message):

    pickled_obj = pickle.dumps(event)
    # LOGS.info(event)
    # LOGS.info(new_dictionary)
    if event.text is not None:
        LOGS.info(f"-----MESSAGE BLOCK STARTED - MESSAGE ID {event.id} ------\n\n MESSAGE ACQUIRED: {event.text}")

        # await bot.send_message(chat_id=Config.BOT_CHANNEL_ID, text=f"{event.text}")
        if not re.match(r"\.(?: |$)?(.*)", event.text):
            await collezione_get.insert_one({'id': event.id, 'data': pickled_obj})
            # check if is reply
            if event.reply_to_message_id:
                LOGS.info(f"CAUGHT REPLY")

                the_Dict = await collezione_get.find_one({'id': event.reply_to_message_id})
                if the_Dict:
                    LOGS.info(f"ID OF THE EVENT THAT GOT THE REPLY: {the_Dict.get('id')}")

                    other_dict = await collezione_fw.find_one({f"{Config.SUFFIX_KEY_ID_DBMS}": the_Dict.get('id')})
                    if other_dict is not None:
                        # get the data from it
                        data = other_dict['data']
                        # unpickle the data
                        unpickled_obj = pickle.loads(data)

                        LOGS.info(
                            f"It is a reply to the message id: {unpickled_obj.id}, text in the message: {unpickled_obj.text}")
                        await send_msg_if_pattern_match(event.text, event.entities, event.id, True,
                                                        unpickled_obj.id)

                    else:
                        LOGS.info("The message wasn't found in the database, so the reply is not going to be forwarded")

                else:
                    LOGS.info(
                        "The input collection document wasn't found in the database, so the reply is not going to be forwarded")
                return

            await send_msg_if_pattern_match(event.text, event.entities, event.id, False, "")
        else:
            LOGS.info("Command registered")
        LOGS.info(f"-----MESSAGE ACQUIRED BLOCK FINISH------")
    else:
        LOGS.info(f"-----Message has got no text in it. DISCARDING ------")


async def send_msg_if_pattern_match(text_message: str, entities, messageid: int, is_reply: bool = None,
                                    input_reply_message_id: str = None):
    if not is_reply:
        LOGS.info(f"Trying to forward message: {text_message}")
    elif is_reply and input_reply_message_id:
        LOGS.info(f"Trying to forward REPLY MESSAGE: {text_message}")
    else:
        LOGS.error(f"UNEXPECTED ERROR in function send_pattern_match, CHECK LOGS ")
    if re.search(Config.PATTERNURL, text_message, flags=re.IGNORECASE):
        text_message = re.sub(Config.PATTERNURL, "", text_message, flags=re.IGNORECASE)
        LOGS.info(f"A link was removed, actual msg {text_message}")

    val_ret, text_message = await check_for_pattern_match(text_message)
    if val_ret != -1 and text_message == None:
        LOGS.info(f"PATTERN MATCH FOUND BUT CONTAINED PATTERN TO EXCLUDE, message discarded")
        return
    elif val_ret != -1 and text_message != None:
        LOGS.info(f"MATCH {val_ret}")
        # matches = regex.finditer(Config.PATTERN1, text_message, re.M)
        # for matchNum, match in enumerate(matches, start=1):
        #     my_dict = match.capturesdict()
        # LOGS.info(my_dict)
        if not await check_for_symbols(text_message):
            return
        # walrus operator on add_prefix_suffix assigning it to a value

        text_message, prefix_length = await add_prefix_suffix(val_ret, text_message)
        LOGS.info(f"PREFIX LENGTH: {prefix_length}")

        entities = await check_entities(entities, prefix_length)

        if not is_reply:
            msgsent_ = await bot.send_message(text=text_message, entities=entities, chat_id=f'{Config.BOT_CHANNEL_ID}')
        else:
            msgsent_ = await bot.send_message(text=text_message, entities=entities, chat_id=f'{Config.BOT_CHANNEL_ID}',
                                              reply_to_message_id=input_reply_message_id)

        dict_event = {'id': msgsent_.id, 'data': pickle.dumps(msgsent_), Config.SUFFIX_KEY_ID_DBMS: messageid}
        # LOGS.info(f"{len(text_message)}")
        # LOGS.info(f"{len(ascii(text_message))}")
        # LOGS.info(f"{repr(text_message)}")
        #
        # LOGS.info(f"{len(msgsent_.text)}")
        # LOGS.info(f"{len(ascii(msgsent_.text))}")
        # LOGS.info(f"{repr(msgsent_.text)}")
        #
        # LOGS.info(f"{text_message}")
        # LOGS.info(f"{ascii(text_message)}")
        LOGS.info(
            f"Forwarded message id: {msgsent_.id}, Text in the message {msgsent_.text}")
        await collezione_fw.insert_one(dict_event)


    else:
        LOGS.info("NO MATCH")
    LOGS.info("-----BLOCK send_msg_if_pattern_match FINISH------")
    #     if text_message:
    #         with open("match_found.txt", "ab") as f:
    #             f.write(f"START-----------\n"
    #                     f"{text_message}\n"
    #                     f"END------------\n\n\n".encode("UTF-8"))
    # else:
    #     LOGS.info(f"No MATCH MESSAGE {text_message}")
    #     if text_message:
    #         with open("match_not_found.txt", "ab") as f:
    #             f.write(f"START-----------\n"
    #                     f"{text_message}\n"
    #                     f"END------------\n\n\n".encode("UTF-8"))


# def add_prefix_suffix(val_ret: int, text_message: str) -> str:
#     if val_ret == 1:
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN1"]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN1"]["suffix"]
#     elif val_ret == 2:
#
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN2"]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN2"]["suffix"]
#
#     elif val_ret == 3:
#
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN3"]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN3"]["suffix"]
#
#     elif val_ret == 4:
#
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN4"]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN4"]["suffix"]
#
#
#     elif val_ret == 5:
#
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN5"]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN5"]["suffix"]
#     elif val_ret == 6:
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN6"][
#                            "prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN6"]["suffix"]
#     elif val_ret == 7:
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN7"][
#                            "prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN7"]["suffix"]
#     elif val_ret == 8:
#         text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN8"][
#                            "prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN8"]["suffix"]
#     return text_message

# def add_prefix_suffix(val_ret: int, text_message: str) -> str:
#     patterns = ["PATTERN1", "PATTERN2", "PATTERN3"]
#     return Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][patterns[val_ret]]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][patterns[val_ret]]["suffix"]
#
# def add_prefix_suffix(val_ret: int, text_message: str) -> str:
#   if val_ret in [1,2,3]:
#     key = f"PATTERN{val_ret}"
#     text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][key]["prefix"] + text_message + \
#                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][key]["suffix"]
#   else:
#     text_message = "something"
#   return text_message

async def check_entities(entities: Optional[list[MessageEntity]], prefix_length: int) -> Optional[list[MessageEntity]]:
    LOGS.info(entities)
    if entities:
        if prefix_length != -1:

            for x in entities:

                x.offset += prefix_length

    LOGS.info(entities)
    return entities


async def check_for_symbols(text_message: str) -> int:
    input_symbols = Symb_Config.extractor.extract(text_message.upper())
    if input_symbols:
        LOGS.info(f"SYMBOLS FOUND IN THE MESSAGE (if any): {input_symbols}")
        # if any(elemen in Symb_Config.SYMB_TO_EXCLUDE for elemen in input_symbols) :
        # sets are faster
        # Its going to look through every item in the smaller set and perform a 0(1) lookup to check if its in the other set. So O(1 * len(s)) where s in the shorter of the two
        # Meanwhite, [x in y_list for x in x_list] is going to do (up to) len(x_list) checks with complexity O(len(y_list))
        # Hence O(len(x_list) * len(y_list)). Several orders of complexity slower

        if intersection := set(input_symbols).intersection(Symb_Config.SYMB_TO_EXCLUDE):
            LOGS.warning(
                f"MATCH WAS FOUND BUT SYMBOL {intersection} was discarded. Message not forwarded")
            return False
    if BlacklistWords.WORDS_TO_EXCLUDE_SET:
        if word_found := set(text_message.upper().split()) & BlacklistWords.WORDS_TO_EXCLUDE_SET:
            LOGS.warning(
                f"MATCH WAS FOUND BUT WORD {word_found} was discarded. Message not forwarded")
            return False
    return True


async def add_prefix_suffix(val_ret: int, text_message: str) -> tuple:
    if val_ret in range(1, 9):
        key = f"PATTERN{val_ret}"
        prefix = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][key]["prefix"]
        suffix = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][key]["suffix"]
        return prefix + text_message + suffix, len(prefix)
    return text_message, -1


async def check_for_pattern_match(event_text: str) -> tuple:
    if re.search(Config.PATTERNURL, event_text, flags=re.IGNORECASE):
        event_text = re.sub(Config.PATTERNURL, "", event_text, flags=re.IGNORECASE)
    elif matches := (re.match(Config.PATTERN1, event_text, flags=(re.IGNORECASE | re.UNICODE | re.MULTILINE))):
        return 1, event_text
    elif matches := (re.match(Config.PATTERN2, event_text, flags=re.IGNORECASE)):
        if await remove_message_if_opt(matches, "PATTERN2"):
            return 2, None
        else:
            return 2, event_text
    elif matches := (re.match(Config.PATTERN3, event_text, flags=re.IGNORECASE)):
        return 3, event_text
    elif matches := (re.match(Config.PATTERN4, event_text, flags=re.IGNORECASE)):
        return 4, event_text
    elif matches := (re.match(Config.PATTERN5, event_text, flags=(re.IGNORECASE | re.MULTILINE))):
        return 5, event_text
    elif matches := (re.match(Config.PATTERN6, event_text, flags=re.IGNORECASE | re.MULTILINE)):
        return 6, event_text
    elif matches := (re.match(Config.PATTERN7, event_text, flags=re.IGNORECASE | re.MULTILINE)):
        if await remove_message_if_opt(matches, "PATTERN7"):
            return 7, None
        else:
            return 7, event_text
    # elif matches := (re.match(Config.PATTERN2, event_text, flags=re.IGNORECASE)):
    #     return (2, ret_[1]) if (ret_ := remove_optional_info(matches, "PATTERN2"))[0] else (2, event_text)

    # if (ret_ := baz("aaa", "bb"))[0]:
    #     return 7, ret_[1]
    elif matches := (re.match(Config.PATTERN8, event_text, flags=re.IGNORECASE | re.MULTILINE)):
        return 8, event_text
    return -1, event_text


async def remove_optional_info(matches: re.Match, pattern) -> tuple:
    if matches:
        if matches.lastgroup == "optional_info":
            if [x for x in
                Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][pattern]["remove_string"]["optional_info"]
                if x in matches.group('optional_info')]:
                # replace the optional_info value with an empty string
                opt_start, opt_end = matches.span('optional_info')
                rest = matches.string[:opt_start] + matches.string[opt_end:]
                return True, rest
    return False, ""


async def remove_message_if_opt(matches: re.Match, pattern) -> bool:
    LOGS.info(pattern)
    if matches:
        if matches.lastgroup == "optional_info":
            if Symb_Config.DICTIONARY_VALS_PREF_SUFFIX.get("glossary").get(pattern):
                if Symb_Config.DICTIONARY_VALS_PREF_SUFFIX.get("glossary").get(pattern).get("remove_string"):
                    if [x for x in
                        Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"][pattern]["remove_string"]["optional_info"]
                        if x in matches.group('optional_info')]:
                        return True
                else:
                    LOGS.error("CHECK YOUR PREF_SUFFIX_MSG, NO REMOVE_STRING")
    return False


@register(incoming=True, chat_id=Config.CLIENT_CHANNEL_ID, edited=True)
async def handler(event: pyrogram.types.Message):
    LOGS.info(f"----EDITED MESSAGE EVENT CAPTURED BLOCK START----")
    # LOGS.info(event)
    try:

        LOGS.info(f"PRINTING EDITED MESSAGE {event.text}")
        return_tuple_match = await check_for_pattern_match(event.text)
        if return_tuple_match[1] == None and return_tuple_match[0] != -1:
            deleted_message_from_end_chat = await collezione_fw.find_one(
                {BotConfig.Config.SUFFIX_KEY_ID_DBMS: event.id})
            if deleted_message_from_end_chat:
                # get data and then id from collection document
                pickled_end_document = pickle.loads(deleted_message_from_end_chat['data'])
                # await collezione_fw.delete_one({'id': deleted_message_from_end_chat['id']})
                await collezione_fw.delete_one(deleted_message_from_end_chat)
                await bot.delete_messages(chat_id=Config.BOT_CHANNEL_ID, message_ids=[pickled_end_document.id],
                                          revoke=True)
            LOGS.info(f"MATCH EDITED MESSAGE BUT CONTAINED A PATTERN TO REMOVE, SO MESSAGE WAS EXCLUDED")
        elif return_tuple_match != (-1, None):
            LOGS.info(f"MATCH EDITED MESSAGE")
            # collezione_fw is a mongodb collection which holds all the forwarded messages from the start to end channel, it has got a key-value pair to hold the start channel message id

            if (document := await collezione_fw.find_one(
                    {Config.SUFFIX_KEY_ID_DBMS: event.id})) is not None:

                # get the data from it
                data = document['data']
                # unpickle the data
                unpickled_obj = pickle.loads(data)

                LOGS.info(
                    f"EDITING MSG {unpickled_obj.id} FROM {Config.CHANNEL_NAME_CLIENT} to {Config.CHANNEL_NAME_BOT}")

                # here i try to edit the message on the end channel by the end channel id
                if not await check_for_symbols(event.text):
                    return
                text_message, prefix_length = await add_prefix_suffix(return_tuple_match[0], return_tuple_match[1])

                event.entities = await check_entities(event.entities, prefix_length)

                msgsent_ = await bot.edit_message_text(text=text_message, chat_id=Config.BOT_CHANNEL_ID,
                                                       message_id=unpickled_obj.id, entities=event.entities)
                LOGS.info(f"TEXT EDITED WITH SUFFIX AND PREFIX:\n{msgsent_.text} and entities {msgsent_.entities}")
            else:
                LOGS.info(
                    f"NO MESSAGE WAS FOUND IN THE COLLECTION  TO EDIT BUT IT MATCHED THE PATTERN, SENDING THE MESSAGE")
                await send_msg_if_pattern_match(text_message=return_tuple_match[1],
                                                messageid=event.id, entities=event.entities)
        LOGS.info(f"----EDITED MESSAGE BLOCK FINISH----")
    except Exception as e:
        LOGS.error(f"ERROR {e}")
        LOGS.info(f"----EXCEPTION THROWN, EDITED MESSAGE BLOCK FINISH----")


## @bot.on_deleted_messages(filters=filters.chat(Config.CLIENT_CHANNEL_ID))
@message_deleted(chat_id=Config.CLIENT_CHANNEL_ID)
async def handler(event: pyrogram.types.List):
    LOGS.info(f"----MESSAGE DELETED EVENT CAPTURED BLOCK START----")
    LOGS.info(event)

    LOGS.info(
        f"{[x.id for x in event]} DELETED MESSAGE FROM CHAT NAME {Config.CHANNEL_NAME_CLIENT}")

    for count, message in enumerate(event):
        deleted_id = message.id
        deleted_message_from_start_chat = await collezione_get.find_one({'id': deleted_id})
        if deleted_message_from_start_chat is not None:
            # get the data from it
            data = deleted_message_from_start_chat['data']
            # unpickle the data
            unpickled_obj = pickle.loads(data)
            LOGS.info(f"Message #{count + 1} that got deleted {unpickled_obj.text}")
            if (the_Dict := await collezione_fw.find_one({Config.SUFFIX_KEY_ID_DBMS: deleted_id})) is not None:
                data_ = the_Dict['data']
                unpickled_obj_ = pickle.loads(data_)
                await bot.delete_messages(chat_id=Config.BOT_CHANNEL_ID, message_ids=[unpickled_obj_.id], revoke=True)
                await collezione_fw.delete_one(the_Dict)
            await collezione_get.delete_one(deleted_message_from_start_chat)
        else:
            LOGS.warning("DELETE MESSAGE TEXT IS NONE AND IT WAS NOT FOUND IN THE COLLECTION")

    LOGS.info(f"----MESSAGE DELETED EVENT CAPTURED BLOCK END----")


# @pyrogram.Client.on_raw_update()
# async def handler(event):
#     LOGS.info(f"----RAW UPDATE EVENT CAPTURED BLOCK START----")
#     if isinstance(event, pyrogram.raw.types.UpdatesTooLong):
#         # handle the update by calling GetDifference
#         getstate = await bot.invoke(
#             GetState()
#         )
#
#         test=await bot.invoke(
#             GetDifference(pts=getstate.pts, date=getstate.date, qts=getstate.qts))
#         LOGS.info(f"pts: {getstate.pts}, date: {getstate.date}, qts: {getstate.qts}")
#
#         LOGS.info(f"----RAW UPDATE EVENT CAPTURED BLOCK END----")
