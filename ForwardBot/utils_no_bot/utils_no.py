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
    # get the lines from the file and store them in a list
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
    dict_to_return = {
        "glossary": {
            "PATTERN1": {
                "prefix": "NUOVA IDEA DI TRADING \uD83D\uDCC8 \n\n",
                "suffix": "\n\n⚠️ Questo messaggio non costituisce un consiglio di investimento ed è esclusivamente a scopo didattico ⚠️️\n"
            },
            "PATTERN2": {
                "prefix": "",
                "suffix": "",
                "remove_string": {
                    "optional_info": [
                        "copier user"
                    ]
                }
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
                "suffix": "",
                "remove_string": {
                    "optional_info": [
                        "copier user"
                    ]
                }
            },
            "PATTERN8": {
                "prefix": "",
                "suffix": "",

            }
        }
    }

    with open(path, "w") as file:
        json.dump(dict_to_return, file, indent=4)
    return dict_to_return