from dataclasses import dataclass

import bs4

from .arg import Arg

TEMPLATE = '''
@register_command
class {command_name}(Command):
    """{doc}
    """
    # {args}
    pass

'''


@dataclass
class Command:
    name: str
    args: list[Arg]
    doc: str

    @classmethod
    def from_html(cls, html: bs4.BeautifulSoup):
        command_name = html.find_all("td")[0].find("b").text[:-1]
        args = [Arg.from_html(h) for h in html.find_all("td")[2].find_all("i") if h.text != "none"]
        doc = html.find_all("td")[3].text
        return cls(command_name, args, doc.strip())

    def class_string(self):
        return TEMPLATE.format(command_name=self.name, doc=self.doc, args=self.args)

