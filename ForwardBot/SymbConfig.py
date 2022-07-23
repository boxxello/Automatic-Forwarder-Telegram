import os.path
from os import environ

import reticker

from ForwardBot import LOGS, const_dirs_class
from ForwardBot.utils_no_bot.utils_no import retrieve_symbols, retrieve_pref_suffix_msg, create_dict_pref_suffix_msg, \
    retrieve_lines_from_file


class Symb_Config(object):
    FILE_SYMB_EXCLUDE = environ.get("FILE_EXCLUDE", "assets_to_ignore.txt")
    path=os.path.join(const_dirs_class.CURR_DIR, FILE_SYMB_EXCLUDE)
    if os.path.exists(path):
        LOGS.info(f"FOUND FILE TO RETRIEVE SYMBOLS FROM {path}")
        if not path.endswith('.txt'):
            LOGS.error("FOUND FILE IS NOT A VALID TXT FILE, EXITING")
            exit(-10)
        FILE_SYMB_EXCLUDE=path
    else:
        LOGS.error(f"Didn't find file {path}, check .env file")
        exit(-11)
    FILE_SYMB_PREF_SUFFIX=environ.get("FILE_PREF_SUFFIX_MSG", "pref_suffix_msg.json")
    #create_dict_pref_suffix_msg(os.path.join(const_dirs_class.CURR_DIR,FILE_SYMB_PREF_SUFFIX))
    DICTIONARY_VALS_PREF_SUFFIX=retrieve_pref_suffix_msg(os.path.join(const_dirs_class.CURR_DIR,FILE_SYMB_PREF_SUFFIX))
    LOGS.info(DICTIONARY_VALS_PREF_SUFFIX)
    extractor=reticker.TickerExtractor()
    SYMB_TO_EXCLUDE = extractor.extract(retrieve_symbols(os.path.join(const_dirs_class.CURR_DIR, FILE_SYMB_EXCLUDE)).__str__())
    LOGS.info(f"Successfully loaded {len(SYMB_TO_EXCLUDE)} symbols to discard: {SYMB_TO_EXCLUDE}")

class BlacklistWords():
    FILE_WORDS_EXCLUDE = environ.get("BLACKLIST_FILE", "blacklist.txt")
    path = os.path.join(const_dirs_class.CURR_DIR, FILE_WORDS_EXCLUDE)
    if os.path.exists(path):
        LOGS.info(f"FOUND FILE TO RETRIEVE BLACKLIST FROM {path}")
        if not path.endswith('.txt'):
            LOGS.error("FOUND FILE IS NOT A VALID TXT FILE, EXITING")
            exit(-10)
    else:
        LOGS.error(f"Didn't find file {path}, check .env file")
        exit(-11)
    WORDS_TO_EXCLUDE=retrieve_lines_from_file(path)
    WORDS_TO_EXCLUDE_SET=set(WORDS_TO_EXCLUDE)
    LOGS.info(f"Successfully loaded {len(WORDS_TO_EXCLUDE)} words to discard: {WORDS_TO_EXCLUDE}")
