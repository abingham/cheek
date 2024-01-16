"""Scripting commands supported by Audacity.

NB: This is currently built on pyaudacity, and will remain so until we decide if and how to
replace its core functionality.
"""

import time
from enum import Enum
from typing import Type

import pyaudacity
from pydantic import BaseModel, PlainSerializer
from typing_extensions import Annotated


class Command(BaseModel):
    "Base of all commands."

    @property
    def command(self):
        "The command string what will be send to Audacity."
        return f'{self._scripting_command_name()}: {" ".join(self._field_strings())}'

    def _field_strings(self):
        "Yields the fields of the command, skipping None values."
        for field, value in self.model_dump().items():
            if value is None:
                continue
            if isinstance(value, Enum):
                value = value.value
            yield f'{field}="{value}"'

    @classmethod
    def _scripting_command_name(cls):
        "The name of the scripting command to use. Defaults to the class name."
        return cls.__name__

    @classmethod
    def user_name(cls):
        "The visual name of the command (i.e. for user interfaces)."
        return cls.__name__


def do(*commands: Command, intercommand_delay=0.001) -> list[str]:
    "Execute a sequence of commands."
    results: list[str] = []
    for command in commands[:1]:
        results.append(pyaudacity.do(command.command))

    for command in commands[1:]:
        time.sleep(intercommand_delay)
        results.append(pyaudacity.do(command.command))

    return results


Bool = Annotated[
    bool,
    PlainSerializer(lambda x: int(x), return_type=int),
]


_command_classes: list[Type[Command]] = []


def all_command_classes():
    "All registered Command subclasses."
    return list(_command_classes)


def register_command(cls):
    "Class decorator to register Command subclass."
    _command_classes.append(cls)
    return cls
