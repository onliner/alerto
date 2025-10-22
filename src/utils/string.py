import re


def strip_whitespaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
