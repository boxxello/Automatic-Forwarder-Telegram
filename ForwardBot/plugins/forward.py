import inspect
import re

from ForwardBot import bot, Config, LOGS,  collezione_get, collezione_fw
from ForwardBot.SymbConfig import Symb_Config, BlacklistWords


@bot.on(telethon.events.NewMessage(incoming=True, chats=Config.CHANNEL_NAME_CLIENT))
async def handler(event: telethon.events.newmessage.NewMessage):
    LOGS.info(f"NEW MESSAGE CAUGHT {event}")
    new_dictionary = {}
    for key__, value__ in event.to_dict().items():
        if isinstance(value__, telethon.tl.tlobject.TLObject):
            new_dictionary.update(dict((key, value) for key, value in value__.to_dict().items() if
                                       not callable(value__) and not key.startswith('__')))
    LOGS.info(f"MESSAGE ACQUIRED {new_dictionary}")
    if not re.match(r"\.(?: |$)?(.*)", new_dictionary.get('message')):
        await collezione_get.insert_one(new_dictionary)
        if event.message.is_reply:
            LOGS.info(f"CAUGHT REPLY")
            the_Dict = await collezione_get.find_one({'id': new_dictionary.get('reply_to').get('reply_to_msg_id')})
            LOGS.info(f"Dict of the event that got a reply: {the_Dict}")

            other_dict = await collezione_fw.find_one({f"{Config.SUFFIX_KEY_ID_DBMS}": the_Dict.get('id')})
            if other_dict is not None:
                LOGS.info(f"DICT OLD  MESSAGE  {other_dict}")
                LOGS.info(
                    f"It is a reply to the message id: {other_dict.get('id')}, text in the message: {other_dict.get('message')}")
                await send_msg_if_pattern_match(new_dictionary["message"], new_dictionary["id"], True,
                                                other_dict.get('id'))
                return
            else:
                LOGS.info("The message wasn't found in the database, so the reply is not going to be forwarded")
                return

        await send_msg_if_pattern_match(new_dictionary["message"], new_dictionary["id"], False, "")
    else:
        LOGS.info("Command registered")


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
            msgsent_ = await bot.send_message(message=text_message, entity=f'{Config.CHANNEL_NAME_BOT}')
        else:
            msgsent_ = await bot.send_message(message=text_message, entity=f'{Config.CHANNEL_NAME_BOT}',
                                              reply_to=input_reply_message_id)

        dict_event = msgsent_.to_dict()
        dict_event.update({Config.SUFFIX_KEY_ID_DBMS: messageid})
        LOGS.info(f"MESSAGE SENT {dict_event}")
        LOGS.info(f" {msgsent_}")
        await collezione_fw.insert_one(dict_event)
        #BotConfig.Config.queue_latest_messages.appendleft(dict_event)

    else:
        LOGS.info("NO MATCH")
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
    elif re.match(Config.PATTERN1, event_text, flags=(re.IGNORECASE | re.UNICODE | re.MULTILINE)):
        return 1, event_text
    elif re.match(Config.PATTERN2, event_text, flags=re.IGNORECASE):
        return 2, event_text
    elif re.match(Config.PATTERN3, event_text, flags=re.IGNORECASE):
        return 3, event_text
    elif re.match(Config.PATTERN4, event_text, flags=re.IGNORECASE):
        return 4, event_text
    elif re.match(Config.PATTERN5, event_text, flags=(re.IGNORECASE | re.MULTILINE)):
        return 5, event_text
    elif re.match(Config.PATTERN6, event_text, flags=re.IGNORECASE | re.MULTILINE):
        return 6, event_text
    elif re.match(Config.PATTERN7, event_text, flags=re.IGNORECASE | re.MULTILINE):
        return 7, event_text
    elif re.match(Config.PATTERN8, event_text, flags=re.IGNORECASE | re.MULTILINE):
        return 8, event_text
    return -1, event_text


@bot.on(telethon.events.MessageEdited(incoming=True, chats=Config.CHANNEL_NAME_CLIENT))
async def handler(event: telethon.events.messageedited.MessageEdited.Event):
    LOGS.info(f"----EDITED MESSAGE EVENT CAPTURED BLOCK START----")
    LOGS.info(event)
    try:
        edited_message_real_dict = {}
        edited_message_dict = event.to_dict()

        for key__, value__ in edited_message_dict.items():
            if isinstance(value__, telethon.tl.tlobject.TLObject):
                edited_message_real_dict.update(dict((key, value) for key, value in value__.to_dict().items() if
                                                     not callable(value__) and not key.startswith('__')))
        LOGS.info(f"PRINTING EDITED MESSAGE {edited_message_real_dict}")
        if (return_tuple_match := check_for_pattern_match(edited_message_real_dict.get('message'))) != (-1, None):
            LOGS.info(f"MATCH EDITED MESSAGE")
            # collezione_fw is a mongodb collection which holds all the forwarded messages from the start to end channel, it has got a key-value pair to hold the start channel message id
            if (the_Dict := await collezione_fw.find_one(
                    {Config.SUFFIX_KEY_ID_DBMS: edited_message_real_dict.get('id')})) is not None:

                LOGS.info(f"Printing retrieved {the_Dict}")
                LOGS.info(f"Printing retrieved message id: {the_Dict.get(Config.SUFFIX_KEY_ID_DBMS)}")

                LOGS.info(f"EDITING MSG FROM {Config.CHANNEL_NAME_CLIENT} to {Config.CHANNEL_NAME_BOT}")
                # here i try to edit the message on the end channel by the end channel id
                text_message = add_prefix_suffix(return_tuple_match[0], return_tuple_match[1])
                await bot.edit_message(text=text_message, entity=Config.CHANNEL_NAME_BOT, message=the_Dict.get('id'))
            
                
                    
            else:
                LOGS.info(
                    f"NO MESSAGE WAS FOUND IN THE COLLECTION  TO EDIT BUT IT MATCHED THE PATTERN, SENDING THE MESSAGE")
                await send_msg_if_pattern_match(text_message=return_tuple_match[1],
                                                messageid=edited_message_real_dict.get('id'))
        LOGS.info(f"----EDITED MESSAGE BLOCK FINISH----")
    except Exception as e:
        LOGS.error(f"ERROR {e}")
        LOGS.info(f"----EXCEPTION THROWN, EDITED MESSAGE BLOCK FINISH----")


        
@bot.on(telethon.events.messagedeleted.MessageDeleted(chats=Config.CHANNEL_NAME_CLIENT))
async def handler(event: telethon.events.messagedeleted.MessageDeleted.Event):
    LOGS.info(f"----MESSAGE DELETED EVENT CAPTURED BLOCK START----")
    LOGS.info(event)

    edited_message_real_dict = {}
    edited_message_dict = event.to_dict()
    LOGS.info(edited_message_dict)
    for key__, value__ in edited_message_dict.items():
        if isinstance(value__, telethon.tl.tlobject.TLObject):
            edited_message_real_dict.update(dict((key, value) for key, value in value__.to_dict().items() if
                                                 not callable(value__) and not key.startswith('__')))
        else:
            edited_message_real_dict.update({key__: value__})
    chatname=await retrieve_chat_name(bot, edited_message_real_dict.get('channel_id'))
    LOGS.info(
        f"{len(edited_message_real_dict.get('deleted_ids'))} DELETED MESSAGES FROM CHAT NAME {chatname}, chat_id: {edited_message_real_dict.get('channel_id')}")

    for idx, deleted_id in enumerate(edited_message_real_dict.get('deleted_ids')):
        deleted_message_from_start_chat = await collezione_get.find_one({'id': deleted_id})
        if deleted_message_from_start_chat is not None:
            LOGS.info(f"Message #{idx+1} that got deleted {deleted_message_from_start_chat.get('message')}")
            if (the_Dict := await collezione_fw.find_one({Config.SUFFIX_KEY_ID_DBMS: deleted_id})) is not None:
                await bot.delete_messages(entity=Config.CHANNEL_NAME_BOT, message_ids=[the_Dict.get('id')], revoke=True)
                await collezione_fw.delete_one(the_Dict)
                await collezione_get.delete_one({'id': deleted_id})
        else:
            LOGS.warning("UNEXPECTED ERROR IN DELETED MESSAGE FUNCT. DELETE MESSAGE IS NONE")

    LOGS.info(f"----MESSAGE DELETED EVENT CAPTURED BLOCK END----")


async def retrieve_chat_name(bot: TelegramClient, channel_id: int) -> str:

    async for dialog in bot.iter_dialogs():
        if str(dialog.id) == str(f"-100{channel_id}"):
            return dialog.name


    # cursor = collection.find({})
    # for document in cursor:
    #     print(document)
    #     if document['_id'] is not None:
    #         print(document['_id'])
    # with open("events.json", "a") as f:
    #     json.dump(new_dictionary, f, indent=2, default=str)
    # print(inspect.getmro(telethon.types.Message))
    # top class is  <class 'telethon.tl.tlobject.TLObject'> and obviously <class 'object'>)
