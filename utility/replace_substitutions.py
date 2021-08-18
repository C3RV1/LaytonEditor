# The game uses some substitutions to represent certain characters
# For example: <''> corresponds to a "
# This function 'fixes' this substitutions
subs_dict = {"<''>": '”',
             "<,,>": "„",
             "<^?>": "¿",
             "<'e>": "é",
             "<'a>": "á",
             "<'o>": "ó",
             "<'i>": "í",
             "<'u>": "ú",
             "<^!>": "¡",
             "<'A>": "Á",
             "<'E>": "É",
             "<'I>": "Í",
             "<'O>": "Ó",
             "<'U>": "Ú",
             "<`a>": "à",
             "<`e>": "è",
             "<`i>": "ì",
             "<`o>": "ò",
             "<`u>": "ù",
             "<`A>": "À",
             "<`E>": "È",
             "<`I>": "Ì",
             "<`O>": "Ò",
             "<`U>": "Ù",
             "<^a>": "â",
             "<^e>": "ê",
             "<^i>": "î",
             "<^o>": "ô",
             "<^u>": "û",
             "<^A>": "Â",
             "<^E>": "Ê",
             "<^I>": "Î",
             "<^O>": "Ô",
             "<^U>": "Û",
             "<:a>": "ä",
             "<:e>": "ë",
             "<:i>": "ï",
             "<:o>": "ö",
             "<:u>": "ü",
             "<,c>": "ç",
             "<,C>": "Ç",
             "<-n>": "ñ",
             "@B": "\n",
             "<po>": "£",
             "<->": "•"}


def replace_substitutions(text, puzzle=False):
    for key, sub in subs_dict.items():
        if puzzle and key == "@B":
            continue
        text = text.replace(key, sub)
    return text


def convert_substitutions(text, puzzle=False):
    for key, sub in subs_dict.items():
        if puzzle and key == "@B":
            continue
        text = text.replace(sub, key)
    return text
