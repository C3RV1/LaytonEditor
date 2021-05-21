# The game uses some substitutions to represent certain characters
# For example: <''> corresponds to a "
# This function 'fixes' this substitutions
subs_dict = {"<''>": "\"",
             "<^?>": "¿",
             "<'e>": "é",
             "<'a>": "á",
             "<'o>": "ó",
             "<'i>": "í",
             "<'u>": "ú",
             "<^!>": "¡",
             "<-n>": "ñ",
             "@B": "\n",
             "<po>": "£",
             "<->": "•"}


def replace_substitutions(text):
    for key, sub in subs_dict.items():
        text = text.replace(key, sub)
    return text


def convert_substitutions(text):
    for key, sub in subs_dict.items():
        text = text.replace(sub, key)
    return text
