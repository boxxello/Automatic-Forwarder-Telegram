from collections import deque
from os import environ
import platform

from dotenv import load_dotenv


from ForwardBot.const_dirs import const_dirs_class


class Config(object):
    SEP = ";"
    CLIENT_CHANNEL_ID=None
    BOT_CHANNEL_ID=None
    load_dotenv(const_dirs_class.USER_DATA_PATH, encoding="utf-8")
    API_ID = int(environ.get("TELEGRAM_API_ID", None))
    SUDO_USERS_INT = environ["SUDO_USERS"].split(SEP)
    API_HASH = environ.get("TELEGRAM_API_HASH", None)
    BOT_PREFIX=environ.get("BOT_PREFIX", None)
    CHANNEL_NAME_BOT = environ.get("CHANNEL_NAME_BOT", None)
    CHANNEL_NAME_CLIENT = environ.get("CHANNEL_NAME_CLIENT", None)
    SESSION_NAME_CLIENT = environ.get("SESSION_NAME_CLIENT", None)
    SUFFIX_KEY_ID_DBMS = environ.get("SUFFIX_KEY_ID_DBMS", "id_msg_fw_bef")
    CELLPHONE_NUMBER=environ.get("CELLPHONE_NUMBER", None)
    COMMAND_HAND_LER = environ.get("COMMAND_HAND_LER", "^/")
    ALIVE_NAME = environ.get(f"{platform.uname().node}", None)
    HOSTING_OP_SYSTEM = platform.uname().system
    CONNECTION_STRING=environ.get("CONNECTION_STRING", None)
    # ([A-Za-z_][A-Za-z0-9_]{2,60}|(__.*__))
    # PATTERN1 = r"^\s*(?P<symbol>[A-Z]{3}[\/I\\\ |-]?[A-Z]{3}|(GOLD))\s*(?P<word2>BUY|SELL|SELL LIMIT|BUY LIMIT)+\s*(?:\s*@\s*)?(?P<amount>-?((\d+\.\d+)|(\d+\.\d+\+?)|(\d+)))\s*(?P<entry>\(?\d{1}[A-Z|a-z]{2}\s*Entry\)?)?\s*(?:\s*(?P<word4>SL|TP)\s*(?P<word5>-?\d+\.\d+|\d+\.\d+\+|(?:\()?Open(?:\))?)\s*(?P<word6>\((-?\d+|\d+\+)?\s*Pips\))?)*\s*(?P<type>Intra-Day Trade|SWING TRADE)?\s*(?:\()?(?P<optional_info>(?<=\().*(?=\)))?(?:\))?\s*$"
    # https://regex101.com/r/tWoqR5/2
    PATTERN_EMOJI = r"[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]|[\U00002702-\U000027B0]|[\U000024C2-\U0001F251]"
    # https://regex101.com/r/i6G7UB/1
    PATTERN1 = r"^\s*(?P<symbol>([A-Z]{6}[\/\\\ |-]GOLD)|(([A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3})|(GOLD)))\s*(?P<word2>BUY|SELL|SELL LIMIT|BUY LIMIT|BUY STOP|SELL STOP)+\s*(?:AGAIN)?\s*(?:\s*@\s*)?(?P<amount>-?((\d+\.\d+)|(\d+\.\d+\+?)|(\d+)))?\s*(?P<entry>\(?\d{1}[A-Z|a-z]{2}\s*Entry\)?)?\s*(?:\s*(?P<word4>SL|TP)\s*(?P<amount_tp_sl>-?((\d+\.\d+)|(\d+\.\d+\+?)|(\d+))|(?:\()?Open(?:\))?)\s*(?P<word6>\((-?\d+|\d+\+)?\s*Pips\))?)*\s*(?P<type>Intra-Day\s*Trade|SWING\s*TRADE|(Swing\s*([\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]|[\U00002702-\U000027B0]|[\U000024C2-\U0001F251])*))?\s*(?P<whole_optional_group>(?:\()?(?P<optional_info>(?<=\().*(?=\)))?(?:\))?)\s*$"
    # https://regex101.com/r/Hpccet/1 con emoji dentro
    # https://regex101.com/r/W4Sc3B/1 no emoji /backup
    # https://regex101.com/r/G3RBXI/1 con emoji dentro+opt value
    PATTERNURL = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"
    PATTERN2 = r"^\s*(?P<symbol>([A-Z]{6}[\/\\\ |-]GOLD)|(([A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3})|(GOLD)))?\s*(\(?(Intra-Day)?\s*\d*[A-Z|a-z]{2}\s*ENTRY\)?)?\s*(((?P<instance>RUNNING|CLOSED|CLOSE)((?:\s*)With)?\s*(?P<pips_num>-\s*\d+|\d+\+|\d+|\+\d+)?\s*((PIPS)?))|\s*((?:\s*)With)?\s*(?P<pips_num2>-\s*\d+|\d+\+|\d+|\+\d+)?\s*((PIPS)?)(\s*(?P<instance2>RUNNING|CLOSED|CLOSE)))\s*((✅)?)+\s*(\d+:((\d+\.\d+|\d+)?\+?))?\s*(RRR\s*(🔥?)*)?(?P<close>CLOSE)?\s*(?P<where>TO|AT|WITH)?\s*(?P<pips_num3>-\s*\d+|\d+\+|\d+|\+\d+)?\s*(?:(PIPS)?)(?P<optional_info>[\s\S]*)?$"
    # https://regex101.com/r/LlVQum/1
    # https://regex101.com/r/SM2i0S/1 backup

    PATTERN3 = r"\s*((?P<symbol>([A-Z]{6}[\/\\\ |-]GOLD)|(([A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3})|(GOLD)))\s*(?P<info>Trade\s*Recap\s*:?)?|(\s*(?P<info2>Trade\s*Recap\s*:?)?\s*(?P<symbol2>[A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3}|(GOLD))))?\s*(?P<type>(SL|TP)?(\d{1})?)\s*(?P<type_act>Hit)\s*((-\d+|\d+\+|\d+|\+\d+)?\s*(&\s*(-\d+|\d+\+|\d+|\+\d+)+)?\s*((Pips)+)?)+\s*((✅)?)+\s*(\d+:((\d+\.\d+|\d+)?\+?))?\s*(RRR\s*(🔥?)*)?\s*$"
    # https://regex101.com/r/nbP8i4/1
    PATTERN4 = r"""(?:((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))?\s*(\d+))?\s*((?P<symbol>([A-Z]{6}[\/\\\ |-]GOLD)|(([A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3})|(GOLD)))\s*(?P<word2>BUY|SELL)+\s*(?:-?)+\s*(?P<outcome>PROFIT)?\s*((✅)?)+\s*(?P<word3>-\d+|\d+\+|\d+|\+\d+)\s*(PIPS)\s*)+((?P<when_month>(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))?\s*(?P<when_day>\d+)\s*(?:-)\s*(Profit)\s*(\d+ (PIPS)\s*((✅)?)))?\s*$
    """
    # https://regex101.com/r/6jedk9/1
    PATTERN5 = r"^\s*((?P<symbol>([A-Z]{6}[\/\\\ |-]GOLD)|(([A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3})|(GOLD)))?\s*(?P<move>Move|CHANGE)|(?P<move2>Move)\s*(?P<symbol2>[A-Z]{3}[\/I\\\ |-]?[A-Z]{3}|(GOLD))?\s*)\s*(?P<what>SL|TP)\s*(?P<where>TO|AT)?\s*(?P<value>(?:\d+\.)*\d+)?(?P<optional_info>.*\s*)?$"
    # https://regex101.com/r/20rGLv/1
    PATTERN6 = r"^\s*(SET)?\s*(?P<what>SL(?:\s*:?)|TP(?:\s*:?))+\s*(?P<where>AT|TO)?\s*(?P<value>(?:@\s*)?(?:\d+\.)*\d+)(?P<optional_info>.*\s*)?$"
    # https://regex101.com/r/u9wf3K/1
    PATTERN7 = r"^(?P<close>CLOSE)\s*(?P<where>TO|AT|WITH)?\s*(?P<pips_num>-\s*\d+|\d+\+|\d+|\+\d+)?\s*(?:(PIPS)?)(?P<optional_info>.*\s*)?$"
    # https://regex101.com/r/2NkaWr/1
    PATTERN8 = r"^\s*((?P<symbol>([A-Z]{6}[\/\\\ |-]GOLD)|(([A-Z]{3}[\/I\\\ |-]?[(A-Z)|(0-9)]{3})|(GOLD)))\s*(?P<info>Trade\s*Recap\s*:?)|(\s*(?P<info2>Trade\s*Recap\s*:?)\s*(?P<symbol2>[A-Z]{3}[\/I\\\s\-\|]?[A-Z]{3}|(GOLD))))\s*(?P<type>(SL|TP)?)\s*(?P<type_act>Hit)\s*((-\d+|\d+\+|\d+|\+\d+)?\s*(&\s*(-\d+|\d+\+|\d+|\+\d+)+)?\s*((Pips)+)?)+\s*((✅)?)+\s*(\d+:((\d+\.\d+|\d+)?\+?))?\s*(RRR\s*(🔥?)*)?\s*"
    # https://regex101.com/r/75ke5e/2
    SYMB_PATTERN = r"^(?P<symbol>[A-Z]{3}[\/I\\\ |-]?[A-Z]{3}|(GOLD))$"
    # https://regex101.com/r/6jedk9/1
    queue_latest_messages = deque(maxlen=5)
    HELP_MSG = """

    """
