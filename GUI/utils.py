def auto_newline(text: str, max_line_length: int):
    def wrap_line_helper(line: str):
        words = line.split(" ")
        wrapped_line = []
        current_line = ""
        for word in words:
            current_line += word
            if len(current_line) > max_line_length:
                current_line = " ".join(current_line.split(" ")[:-1])
                wrapped_line.append(current_line)
                current_line = word
            current_line += " "
        wrapped_line.append(current_line[:-1])
        return "\n".join(wrapped_line)
    lines = text.split("\n")
    wrapped_lines = []
    for line1 in lines:
        wrapped_lines.append(wrap_line_helper(line1))
    return "\n".join(wrapped_lines)


def to_int(s: str):
    if s.startswith("0x"):
        return int(s[2:], 16)
    return int(s)
