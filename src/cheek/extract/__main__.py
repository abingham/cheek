from pathlib import Path
import sys
import bs4

from .arg import Arg

from .command import Command


def main():
    commands = tuple(parse_commands(Path(sys.argv[1]).read_text(encoding="utf-8")))

    print("from enum import Enum")

    for command in commands:
        command_lines = _command_to_python(command)
        print("\n".join(command_lines))


def parse_commands(text: str):
    soup = bs4.BeautifulSoup(text, features="html.parser")
    for table in soup.find_all("table")[1:]:
        for row in table.find_all("tr")[1:]:
            yield Command.from_html(row)


def _command_to_python(command: Command):
    for arg in command.args:
        if arg.enum_values:
            yield from _enum_to_python(command.name, arg)

    yield f"class {_valid_python_name(command.name)}:"
    if command.args:
        for arg in command.args:
            yield from _arg_to_python(command.name, arg)
    else:
        yield "    pass"


def _arg_to_python(command_name, arg: Arg):
    yield f"    {_valid_python_name(arg.name)}: {_python_type(command_name, arg)} = {_default_to_python(command_name, arg)}"


def _default_to_python(command_name, arg: Arg):
    if arg.default is None:
        return None
    if arg.type == "string":
        if arg.default == "":
            return "''"
        return f'"{arg.default}"'
    if arg.type == "enum":
        return f"{_python_enum_name(command_name, arg.name)}.{_valid_python_name(arg.default)}"
    return arg.default


def _enum_to_python(command_name: str, arg: Arg):
    assert arg.enum_values
    yield f"class {_python_enum_name(command_name, arg.name)}(Enum):"
    for enum_value in arg.enum_values:
        yield f"    {_valid_python_name(enum_value)} = '{enum_value}'"


def _python_enum_name(command_name, arg_name):
    return f"{_valid_python_name(command_name)}{_valid_python_name(arg_name)}"


def _valid_python_name(name: str):
    if name == "None":
        name = "None_"
    name = name.replace(",", "_")
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.replace("-", "_")
    name = name.replace("(", "_")
    name = name.replace(")", "_")
    return name


def _python_type(command_name, arg: Arg):
    match arg.type:
        case "size_t":
            return "int"
        case "int":
            return "int"
        case "string":
            return "str"
        case "double":
            return "float"
        case "float":
            return "float"
        case "bool":
            return "bool"
        case "enum":
            return _python_enum_name(command_name, arg.name)
        case _:
            raise ValueError(f"No python type for '{type_str}'")


if __name__ == "__main__":
    main()