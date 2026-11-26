import re


def split(source):
    markers = list(re.finditer(r"(?m)^[ \t]*(?://|#)[ \t]*EVOLVE_(START|END)[ \t]*\r?$", source))
    if [match[1] for match in markers] != ["START", "END"]:
        raise ValueError("Exactly one ordered EVOLVE marker pair is required")
    start, end = markers
    return source[:start.end()], source[start.end():end.start()], source[end.start():]


def integrate(source, body):
    header, _, trailer = split(source)
    updated = header + "\n" + body.strip("\r\n") + "\n" + trailer
    if split(updated)[::2] != (header, trailer):
        raise ValueError("Generated body changed marker boundaries")
    return updated


def executable(source):
    head, body, tail = split(source)
    return head[:head.rfind("\n") + 1] + body + tail.partition("\n")[2]
