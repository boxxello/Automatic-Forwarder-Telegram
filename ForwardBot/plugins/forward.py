import re
import pyrogram
from pyrogram import enums

from ForwardBot import bot, Config, LOGS, collezione_get, collezione_fw, unwrap_dict
from ForwardBot.SymbConfig import Symb_Config, BlacklistWords
from ForwardBot.events import register, message_deleted


@register(outgoing=True, chat_id=Config.CLIENT_CHANNEL_ID)
async def handler(event: pyrogram.types.Message):
    new_dictionary = unwrap_dict(event)
    # LOGS.info(event)
    # LOGS.info(new_dictionary)
    if event.text is not None:
        LOGS.info(f"-----MESSAGE BLOCK STARTED ------\n\nMESSAGE ACQUIRED: {repr(event.text)}")

        # await bot.send_message(chat_id=Config.BOT_CHANNEL_ID, text=f"{event.text}")
        if not re.match(r"\.(?: |$)?(.*)", new_dictionary.get('text')):
            await collezione_get.insert_one(new_dictionary)
            # check if is reply
            if new_dictionary.get('reply_to_message_id'):
                LOGS.info(f"CAUGHT REPLY")
                the_Dict = await collezione_get.find_one({'id': new_dictionary.get('reply_to_message_id')})
                LOGS.info(f"Dict of the event that got a reply: {the_Dict}")

                other_dict = await collezione_fw.find_one({f"{Config.SUFFIX_KEY_ID_DBMS}": the_Dict.get('id')})
                if other_dict is not None:
                    LOGS.info(f"DICT OLD  MESSAGE  {other_dict}")
                    LOGS.info(
                        f"It is a reply to the message id: {other_dict.get('id')}, text in the message: {other_dict.get('text')}")
                    await send_msg_if_pattern_match(new_dictionary["text"], new_dictionary["id"], True,
                                                    other_dict.get('id'))
                    return
                else:
                    LOGS.info("The message wasn't found in the database, so the reply is not going to be forwarded")
                    return

            await send_msg_if_pattern_match(new_dictionary["text"], new_dictionary["id"], False, "")
        else:
            LOGS.info("Command registered")
        LOGS.info(f"-----MESSAGE ACQUIRED BLOCK FINISH------")
    else:
        LOGS.info(f"-----Message has got no text in it. DISCARDING ------")



async def send_msg_if_pattern_match(text_message: str, messageid: str, is_reply: bool = None,
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

    val_ret, text_message = check_for_pattern_match(text_message)
    if val_ret != -1:
        LOGS.info(f"MATCH {val_ret}")
        # matches = regex.finditer(Config.PATTERN1, text_message, re.M)
        # for matchNum, match in enumerate(matches, start=1):
        #     my_dict = match.capturesdict()
        # LOGS.info(my_dict)
        input_symbols = Symb_Config.extractor.extract(text_message)

        LOGS.info(f"SYMBOLS FOUND IN THE MESSAGE (if any): {input_symbols}")
        if input_symbols:
            # if any(elemen in Symb_Config.SYMB_TO_EXCLUDE for elemen in input_symbols) :
            # sets are faster
            # Its going to look through every item in the smaller set and perform a 0(1) lookup to check if its in the other set. So O(1 * len(s)) where s in the shorter of the two
            # Meanwhite, [x in y_list for x in x_list] is going to do (up to) len(x_list) checks with complexity O(len(y_list))
            # Hence O(len(x_list) * len(y_list)). Several orders of complexity slower

            if set(input_symbols).intersection(Symb_Config.SYMB_TO_EXCLUDE):
                LOGS.warning(
                    f"MATCH WAS FOUND BUT SYMBOL {input_symbols} was discarded. Message not forwarded")
                return
        if word_found := set(text_message.upper().split()) & BlacklistWords.WORDS_TO_EXCLUDE_SET:
            LOGS.warning(
                f"MATCH WAS FOUND BUT WORD {word_found} was discarded. Message not forwarded")
            return
        text_message = add_prefix_suffix(val_ret, text_message)
        LOGS.info(messageid)
        if not is_reply:
            msgsent_ = await bot.send_message(text=text_message, chat_id=f'{Config.BOT_CHANNEL_ID}')
        else:
            msgsent_ = await bot.send_message(text=text_message, chat_id=f'{Config.BOT_CHANNEL_ID}',
                                              reply_to_message_id=input_reply_message_id)

        dict_event = unwrap_dict(msgsent_)
        dict_event.update({Config.SUFFIX_KEY_ID_DBMS: messageid})
        LOGS.info(f"MESSAGE SENT {dict_event}")
        LOGS.info(f"Text in the message {msgsent_.text}")
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


def add_prefix_suffix(val_ret: int, text_message: str) -> str:
    if val_ret == 1:
        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN1"]["prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN1"]["suffix"]
    elif val_ret == 2:

        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN2"]["prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN2"]["suffix"]
        pass
    elif val_ret == 3:

        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN3"]["prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN3"]["suffix"]
        pass
    elif val_ret == 4:

        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN4"]["prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN4"]["suffix"]

        pass
    elif val_ret == 5:

        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN5"]["prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN5"]["suffix"]
    elif val_ret == 6:
        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN6"][
                           "prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN6"]["suffix"]
    elif val_ret == 7:
        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN7"][
                           "prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN7"]["suffix"]
    elif val_ret == 8:
        text_message = Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN8"][
                           "prefix"] + text_message + \
                       Symb_Config.DICTIONARY_VALS_PREF_SUFFIX["glossary"]["PATTERN8"]["suffix"]
    return text_message


def check_for_pattern_match(event_text: str) -> tuple:
    if re.search(Config.PATTERNURL, event_text, flags=re.IGNORECASE):
        event_text = re.sub(Config.PATTERNURL, "", event_text, flags=re.IGNORECASE)
    elif matches := (re.match(Config.PATTERN1, event_text, flags=(re.IGNORECASE | re.UNICODE | re.MULTILINE))):
        return 1, event_text
    elif matches := (re.match(Config.PATTERN2, event_text, flags=re.IGNORECASE)):
        return (2, ret_[1]) if (ret_ :=remove_optional_info(matches, "PATTERN2"))[0] else (2, event_text)
    elif matches := (re.match(Config.PATTERN3, event_text, flags=re.IGNORECASE)):
        return 3, event_text
    elif matches := (re.match(Config.PATTERN4, event_text, flags=re.IGNORECASE)):
        return 4, event_text
    elif matches := (re.match(Config.PATTERN5, event_text, flags=(re.IGNORECASE | re.MULTILINE))):
        return 5, event_text
    elif matches := (re.match(Config.PATTERN6, event_text, flags=re.IGNORECASE | re.MULTILINE)):
        return 6, event_text
    elif matches := (re.match(Config.PATTERN7, event_text, flags=re.IGNORECASE | re.MULTILINE)):
        return (7, ret_[1]) if (ret_ :=remove_optional_info(matches, "PATTERN7"))[0] else (7, event_text)
        # if (ret_ := baz("aaa", "bb"))[0]:
        #     return 7, ret_[1]
    elif matches := (re.match(Config.PATTERN8, event_text, flags=re.IGNORECASE | re.MULTILINE)):
        return 8, event_text
    return -1, event_text


def remove_optional_info(matches: re.Match, pattern) -> tuple:
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


@register(outgoing=True, chat_id=Config.CLIENT_CHANNEL_ID, edited=True)
async def handler(event: pyrogram.types.Message):
    LOGS.info(f"----EDITED MESSAGE EVENT CAPTURED BLOCK START----")
    # LOGS.info(event)
    try:

        edited_message_real_dict = unwrap_dict(event)

        LOGS.info(f"PRINTING EDITED MESSAGE {edited_message_real_dict.get('text')}")
        if (return_tuple_match := check_for_pattern_match(edited_message_real_dict.get('text'))) != (-1, None):
            LOGS.info(f"MATCH EDITED MESSAGE")
            # collezione_fw is a mongodb collection which holds all the forwarded messages from the start to end channel, it has got a key-value pair to hold the start channel message id
            if (the_Dict := await collezione_fw.find_one(
                    {Config.SUFFIX_KEY_ID_DBMS: edited_message_real_dict.get('id')})) is not None:

                LOGS.info(f"Printing retrieved {the_Dict.get('text')}")
                LOGS.info(f"Printing retrieved message id: {the_Dict.get(Config.SUFFIX_KEY_ID_DBMS)}")

                LOGS.info(f"EDITING MSG FROM {Config.CHANNEL_NAME_CLIENT} to {Config.CHANNEL_NAME_BOT}")
                # here i try to edit the message on the end channel by the end channel id
                text_message = add_prefix_suffix(return_tuple_match[0], return_tuple_match[1])
                await bot.edit_message_text(text=text_message, chat_id=Config.BOT_CHANNEL_ID, message_id=the_Dict.get('id'))



            else:
                LOGS.info(
                    f"NO MESSAGE WAS FOUND IN THE COLLECTION  TO EDIT BUT IT MATCHED THE PATTERN, SENDING THE MESSAGE")
                await send_msg_if_pattern_match(text_message=return_tuple_match[1],
                                                messageid=edited_message_real_dict.get('id'))
        LOGS.info(f"----EDITED MESSAGE BLOCK FINISH----")
    except Exception as e:
        LOGS.error(f"ERROR {e}")
        LOGS.info(f"----EXCEPTION THROWN, EDITED MESSAGE BLOCK FINISH----")


## @bot.on_deleted_messages(filters=filters.chat(Config.CLIENT_CHANNEL_ID))
@message_deleted(chat_id=Config.CLIENT_CHANNEL_ID)
async def handler(event: pyrogram.types.Message):
    LOGS.info(f"----MESSAGE DELETED EVENT CAPTURED BLOCK START----")
    # LOGS.info(event)
    edited_message_real_dict = unwrap_dict(event)

    LOGS.info(
        f"{len(edited_message_real_dict)} DELETED MESSAGES FROM CHAT NAME {Config.CHANNEL_NAME_CLIENT}")

    for count, message in enumerate(edited_message_real_dict):
        deleted_id = message.get('id')
        deleted_message_from_start_chat = await collezione_get.find_one({'id': deleted_id})
        if deleted_message_from_start_chat is not None:
            LOGS.info(f"Message #{count + 1} that got deleted {deleted_message_from_start_chat.get('text')}")
            if (the_Dict := await collezione_fw.find_one({Config.SUFFIX_KEY_ID_DBMS: deleted_id})) is not None:
                await bot.delete_messages(chat_id=Config.BOT_CHANNEL_ID, message_ids=[the_Dict.get('id')], revoke=True)
                await collezione_fw.delete_one(the_Dict)
                await collezione_get.delete_one({'id': deleted_id})
        else:
            LOGS.warning("DELETE MESSAGE TEXT IS NONE AND IT WAS NOT FOUND IN THE COLLECTION")

    LOGS.info(f"----MESSAGE DELETED EVENT CAPTURED BLOCK END----")

    # cursor = collection.find({})
    # for document in cursor:
    #     print(document)
    #     if document['_id'] is not None:
    #         print(document['_id'])
    # with open("events.json", "a") as f:
    #     json.dump(new_dictionary, f, indent=2, default=str)
    # print(inspect.getmro(telethon.types.Message))
    # top class is  <class 'telethon.tl.tlobject.TLObject'> and obviously <class 'object'>)
