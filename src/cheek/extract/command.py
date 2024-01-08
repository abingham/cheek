from dataclasses import dataclass

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
    def from_spec(cls, spec: dict):
        command_name = spec["id"]
        args = [Arg.from_spec(param) for param in spec["params"]]
        doc = spec["tip"]
        return cls(command_name, args, doc.strip())

    def class_string(self):
        return TEMPLATE.format(command_name=self.name, doc=self.doc, args=self.args)

