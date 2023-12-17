"""Command line interface for cheek.
"""

import logging
from types import NoneType, UnionType
from typing import Any, Type

import click
import pydantic.fields

import cheek.commands

log = logging.getLogger()


def field_info_to_click_type(field_info: pydantic.fields.FieldInfo):
    "Determine the click type from a pydantic FieldInfo."
    ann = field_info.annotation

    assert ann is not None, "Should not have None field type"

    # If ann is a Union, we return the first non-NoneType type.
    # TODO: What's the right way to iterate a union's types?
    if isinstance(ann, UnionType):
        for utype in ann.__args__:
            if utype is not NoneType:
                return utype
        assert False, "Union type should have non-None element."

    return ann


def construct_command_from_kwargs(
    command_class: Type[cheek.commands.Command], kwargs: dict[str, Any]
) -> cheek.commands.Command:
    """Construct a Command instance from click kwargs.

    Click produces kwargs which are all lower-case. This function
    maps those back to the real kwarg names as expected by the
    Command instances. It then constructs a Command using these
    translated argument names and values.

    Args:
        command_class (Command): The command to construct.
        kwargs (dict[str, Any]): The kwargs provided by click.

    Returns:
        _type_: _description_
    """
    name_map = {field_name.lower(): field_name for field_name in command_class.model_fields}
    command_kwargs = {name_map[name]: value for name, value in kwargs.items()}

    command_instance = command_class(**command_kwargs)
    return command_instance


def build_cli():
    """Build the command group for the CLI.

    Returns:
        click.Group: The command group.
    """

    @click.group
    def cli():
        pass

    # For each registered Command subclass, construct a CLI command.
    for command_class in cheek.commands.all_command_classes():

        @cli.command(name=command_class._command_name())
        def cmd(**kwargs):
            command_instance = construct_command_from_kwargs(command_class, kwargs)
            log.info(command_instance)
            results = cheek.commands.do(command_instance)
            print(results)

        # TODO: Is there are more imperative way to use click to build the CLI?

        # Loop over command.model_fields to figure out CLI arguments. Do this in reverse so that the innermost
        # decoration represents the last argument.
        for field_name, field_info in reversed(command_class.model_fields.items()):
            click_type = field_info_to_click_type(field_info)
            cmd = click.option(
                f"--{field_name}",
                type=click_type,
                default=field_info.default,
                required=field_info.is_required(),
                show_default=True
            )(cmd)

    return cli


if __name__ == "__main__":
    # TODO: Make this configurable
    logging.basicConfig(level=logging.INFO)

    build_cli()()
