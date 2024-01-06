import re
from dataclasses import dataclass, field

import bs4


@dataclass
class Arg:
    name: str
    type: str
    default: str
    enum_values: list[str] = field(default_factory=list)

    @classmethod
    def from_html(cls, html: bs4.BeautifulSoup):
        type_str, name_str, default_str = tuple(map(str.strip, html.strings))

        enum_values = []
        if type_str == "enum":
            enum_values.extend(_find_enum_values(html))

        default_value = cls._default_value(default_str)

        return cls(
            name=name_str.strip(), type=type_str, default=default_value, enum_values=enum_values
        )

    @staticmethod
    def _default_value(default_str):
        pattern = r", \(default:(.*)\)"
        regex = re.compile(pattern)
        match = regex.match(default_str)
        default_value = match[1]
        if default_value == "unchanged":
            return None
        return default_value


def _find_enum_values(arg_elem: bs4.BeautifulSoup):
    enum_list_elem = arg_elem.find_next("ul")
    if enum_list_elem is None:
        return

    for enum_value_elem in enum_list_elem.find_all("li"):
        enum_value = enum_value_elem.text.strip()
        yield enum_value
