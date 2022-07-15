import json


def retrieve_symbols(path: str) -> list:
    list_to_return = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            line = line.replace("/", "").replace("\\", "").replace("-", "").replace("|", "")
            list_to_return.append(line.upper())
    return list_to_return

def retrieve_lines_from_file(path: str) -> list:
    list_to_return = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            list_to_return.append(line.upper())
    return list_to_return


def retrieve_pref_suffix_msg(path: str) -> dict:
    with open(path, encoding='utf-8') as inputfile:
        dict_to_return = json.load(inputfile)
    return dict_to_return


def create_dict_pref_suffix_msg(path: str) -> dict:
    dict_to_return = {"glossary": {
        "PATTERN1": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN2": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN3": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN4": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN5": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN6": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN7": {
            "prefix": "",
            "suffix": ""
        },
        "PATTERN8": {
            "prefix": "",
            "suffix": ""
        },
    }
    }
    with open(path, "w") as file:
        json.dump(dict_to_return, file, indent=4)
