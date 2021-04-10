# The game uses some substitutions to represent certain characters
# For example: <''> corresponds to a "
# This function 'fixes' this substitutions
def replace_substitutions(text):
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
    for key, sub in subs_dict.items():
        text = text.replace(key, sub)
    return text
