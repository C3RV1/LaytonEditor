# Data and Code Container (DCC) format by Cervi

import typing


def is_int(var):
    try:
        int(var)
        return True
    except ValueError:
        return False


def is_float(var):
    try:
        float(var)
        return True
    except ValueError:
        return False


def is_hex(var):
    try:
        int(var, 16)
        return True
    except ValueError:
        return False


class Parser:
    def __init__(self):
        self.code: typing.Union[str, dict] = ""
        self.converted_paths = []
        self.imported = {}

    def parse(self, code_=None):
        if code_:
            self.code = code_
        self.converted_paths = []
        self.split_by_tokens()
        self.create_structure()
        self.convert_variables()

    def serialize(self, code_=None, imported=None):
        if imported is None:
            imported = []
        if code_:
            self.code = code_
        self.converted_paths = []
        self.revert_variables()
        self.remove_structure(imported)
        self.join_by_tokens()
        return self.code

    def split_by_tokens(self):
        tokens = []
        in_string = False
        code_index = 0
        current_token = ""
        while code_index < len(self.code):
            if self.code[code_index] == "\n":
                if not in_string:
                    if current_token != "":
                        tokens.append(current_token)
                    current_token = ""
                    code_index += 1
                    if code_index >= len(self.code):
                        continue
                    if self.code[code_index] == "#":
                        while self.code[code_index] != "\n" and code_index < len(self.code):
                            code_index += 1
                    continue
            elif self.code[code_index] == "(" and not in_string:
                tokens.append(current_token + "(")
                current_token = ""
            elif self.code[code_index] == ")" and not in_string:
                tokens.append(current_token)
                current_token = ")"
            elif self.code[code_index] == "\"":
                in_string = not in_string
                current_token += self.code[code_index]
            elif self.code[code_index] == "\\" and self.code[code_index + 1] == "\"" and in_string:
                code_index += 1
                current_token += "\""
            elif self.code[code_index] == " " and not in_string:
                pass
            else:
                current_token += self.code[code_index]
            code_index += 1
        tokens.append(current_token)
        self.code = list(filter(lambda x: len(x) > 0, tokens))

    def join_by_tokens(self, add_string_newline=True):
        joined = ""
        indent = 0
        for token in self.code:
            if ":" in token:
                token_split = token.split(":")
                token = token_split[0] + ": " + token_split[1]
            if "\"" in token:
                token_parsed = ""
                while token[0] != "\"":
                    token_parsed += token[0]
                    token = token[1:]
                token_parsed += "\""
                token = token[1:]
                while len(token) > 0:
                    if token[:2] == "\\n" and add_string_newline:
                        token_parsed += "\\n\n"
                        token = token[2:]
                        continue
                    token_parsed += token[0]
                    token = token[1:]
                token = token_parsed
            if token[-1] == "]" or token == ")":
                indent -= 1
            if token[-1] == "(":
                token = token[:-1] + " ("
            joined += " " * (4 * indent) + token + "\n"
            if token[-1] == "[" or token[-1] == "(":
                indent += 1
        self.code = joined

    def create_structure(self):
        tokens = self.code

        def convert_to_group(is_call=False):
            nonlocal tokens
            current_group = {"unnamed": [], "named": {}, "calls": []}
            while len(tokens) > 0:
                token = tokens[0]
                tokens = tokens[1:]
                if token == "]" or token == ")":
                    break
                if "=" == token[0]:
                    token_value = token[1:]
                    current_group['unnamed'].append(token_value)
                elif is_call:  # "," in token and
                    params = []
                    token_copy = token
                    current_token = ""
                    while len(token_copy) > 0:
                        if token_copy[0] == "\"":
                            current_token += "\""
                            token_copy = token_copy[1:]
                            while len(token_copy) > 0 and token_copy[0] != "\"":
                                if token_copy[:2] == "\"":
                                    current_token += "\""
                                    token_copy = token_copy[1:]
                                current_token += token_copy[0]
                                token_copy = token_copy[1:]
                            current_token += "\""
                            token_copy = token_copy[1:]
                        elif token_copy[0] == ",":
                            params.append(current_token)
                            current_token = ""
                            token_copy = token_copy[1:]
                        else:
                            current_token += token_copy[0]
                            token_copy = token_copy[1:]
                    params.append(current_token)
                    for par_i in range(len(params)):
                        params[par_i] = params[par_i].strip()
                    current_group["unnamed"].extend(params)
                elif "$" == token[0]:
                    token_value = token[1:]
                    if token_value not in self.imported:
                        new_parser = Parser()
                        file_to_imp = open(token_value, "r")
                        new_parser.parse(file_to_imp.read())
                        file_to_imp.close()
                        self.imported[token_value] = new_parser
                    else:
                        new_parser = self.imported[token_value]
                    current_group["named"].update(new_parser.code["named"])
                    self.converted_paths.extend(new_parser.converted_paths[1:])
                elif ":" in token:
                    if is_call:
                        raise SyntaxError("Call is not allowed to have named")
                    token_name = token.split(":")[0]
                    token_value = token.split(":")[1]
                    if token_value == "[":
                        token_value = convert_to_group()
                    current_group['named'][token_name] = token_value
                elif "(" == token[-1]:
                    if is_call:
                        raise SyntaxError("Call is not allowed to have calls")
                    current_group['calls'].append({
                        "func": token[:-1],
                        "parameters": convert_to_group(is_call=True)
                    })
            if is_call:
                return current_group['unnamed']
            return current_group

        self.code = convert_to_group()

    def remove_structure(self, imported):
        def revert_group(group):
            pre_group = []
            for element in group["unnamed"]:
                if not isinstance(element, dict):
                    pre_group.append(f"={element}")
                else:
                    pre_group.append("=[")
                    pre_group.extend(revert_group(element))
                    pre_group.append("]")
            for element in group["named"].keys():
                if not isinstance(group["named"][element], dict):
                    pre_group.append(f"{element}:{group['named'][element]}")
                else:
                    pre_group.append(f"{element}:[")
                    pre_group.extend(revert_group(group["named"][element]))
                    pre_group.append("]")
            for element in group["calls"]:
                pre_group.append(f"{element['func']}(" + ", ".join(element['parameters']) + ")")
            return pre_group

        for imported_file in imported:
            if imported_file not in self.imported:
                new_parser = Parser()
                imported_code = open(imported_file, "r")
                new_parser.parse(imported_code.read())
                imported_code.close()
            else:
                new_parser = self.imported[imported_file]
            for named in new_parser.code["named"].keys():
                if named in self.code["named"].keys():
                    self.code["named"].pop(named)
            # TODO: Finish remove imported
        self.code = revert_group(self.code)
        for imported_file in imported:
            self.code.insert(0, f"${imported_file}")

    def convert_variables(self):

        def convert_variable(value):
            if value.startswith("\"") and value.endswith("\""):
                value = value[1:-1]
                value = bytes(value, "utf-8").decode("unicode_escape")
                return value
            elif is_int(value):
                return int(value)
            elif is_hex(value):
                return int(value, 16)
            elif is_float(value):
                return float(value)
            elif value == "true":
                return True
            elif value == "false":
                return False
            elif value == "null":
                return None
            elif self.get_path(value) is not None:
                if value not in self.converted_paths:
                    convert_path(".".join(value.split(".")[:-1]))
                return self.get_path(value)
            else:
                raise ValueError(f"{value} is not recognised as a valid value")

        def convert_path(path):
            path_obj = self.get_path(path)
            if path in self.converted_paths:
                return path_obj
            self.converted_paths.append(path)
            if isinstance(path_obj, dict):
                for i in range(len(path_obj["unnamed"])):
                    path_obj["unnamed"][i] = convert_variable(path_obj["unnamed"][i])
                for i in path_obj["named"].keys():
                    if path is not None:
                        new_path = path + "." + i
                    else:
                        new_path = i
                    path_obj["named"][i] = convert_path(new_path)
                for i in path_obj["calls"]:
                    for parameter in range(len(i['parameters'])):
                        i['parameters'][parameter] = convert_variable(i['parameters'][parameter])
                return path_obj
            else:
                return convert_variable(path_obj)

        convert_path(None)

    def revert_variables(self):
        def revert_variable(value):
            if isinstance(value, str):
                value = bytes(value, 'unicode_escape').decode('utf-8').replace('\"', '\\\"')
                return f"\"{value}\""
            elif value is True:
                return "true"
            elif value is False:
                return "false"
            elif value is None:
                return "null"
            elif isinstance(value, int):
                return str(value)
            elif isinstance(value, float):
                return str(value)
            else:
                raise ValueError(f"{value} can't be converted to non-value")

        def revert_path(path):
            path_obj = self.get_path(path)
            if isinstance(path_obj, dict):
                for i in range(len(path_obj["unnamed"])):
                    path_obj["unnamed"][i] = revert_variable(path_obj["unnamed"][i])
                for i in path_obj["named"].keys():
                    if path is not None:
                        new_path = path + "." + i
                    else:
                        new_path = i
                    path_obj["named"][i] = revert_path(new_path)
                for i in path_obj["calls"]:
                    for parameter in range(len(i['parameters'])):
                        i['parameters'][parameter] = revert_variable(i['parameters'][parameter])
                return path_obj
            else:
                return revert_variable(path_obj)
        revert_path(None)

    def get_path(self, path, create=False, index=0) -> typing.Union[dict, str, None]:
        if path is not None:
            path = path.split(".")
        else:
            path = []
        if index != 0:
            path = path[:index]
        current: dict = self.code
        while len(path) > 0:
            if path[0] not in current['named']:
                if create:
                    current['named'][path[0]] = {"unnamed": [], "named": {}, "calls": []}
                else:
                    return None
            current = current['named'][path[0]]
            path = path[1:]
        return current

    def __getitem__(self, item):
        if isinstance(item, str):
            path = item.split("::")[0]
            proper = item.split("::")[1:]
            current = self.get_path(path)
            while len(proper) > 0:
                if is_int(proper[0]):
                    proper: list
                    proper[0] = int(proper[0])
                current = current[proper[0]]
                proper = proper[1:]
            return current
        else:
            raise Exception

    def reset(self):
        self.code = {"unnamed": [], "named": {}, "calls": []}

    def set_named(self, path, value):
        path_obj = self.get_path(path, index=-1, create=True)
        path_obj['named'][path.split(".")[-1]] = value

    def exists(self, path):
        if self.get_path(path) is not None:
            return True
        return False


"""if __name__ == "__main__":
    file = open("event_example.dcc")
    code = file.read()
    file.close()
    parser = Parser()
    parser.parse(code)
    # parser.serialize()
    # parser.parse()
    print(parser.code)"""
