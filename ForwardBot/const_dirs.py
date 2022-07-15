import os
import sys
from datetime import datetime


class const_dirs_class:
    CURR_DIR = os.path.dirname(__file__)
    USER_DATA_PATH = os.path.join(CURR_DIR, "user_data.env")
    LOG_DIR=os.path.join(CURR_DIR, "logs")
    LOG_FILE_SUFFIX = ('_{}.log'.format(datetime.now().strftime("%d_%m_%Y__%H_%M_%S")))

    def __init__(self):
        pass


    def make_dir(self):
        dir_list = {self.LOG_DIR}

        for dir in dir_list:
            if not os.path.isdir(dir):
                try:
                    os.makedirs(dir)
                except OSError as e:
                    print(f"Unable to create {dir}, exception was thrown {e.strerror}")
                    sys.exit(-4)