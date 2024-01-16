"""Command line interface for cheek.
"""

import logging
from types import NoneType, UnionType
from typing import Any, Type

import click
import pydantic.fields

import cheek.commands

log = logging.getLogger()

# TODO: Need better handling of enum parameter types. We should detect them
# when building the CLI and create the appropriate type of click option
# that takes the possible enum values into account.
#
# A good example of one of these is `Chirp`.


def field_info_to_python_type(field_info: pydantic.fields.FieldInfo):
    "Determine the click type from a pydantic FieldInfo."
    ann = field_info.annotation

    assert ann is not None, "Should not have None field type"

    # TODO: Handle Optional[X]. Also, understand when we see it.
    # if "Optional" in str(ann):
    #     breakpoint()

    # If ann is a Union, we return the first non-NoneType type.
    # TODO: What's the right way to iterate a union's types?
    if isinstance(ann, UnionType):
        for utype in ann.__args__:
            if utype is not NoneType:
                return utype
        assert False, "Union type should have non-None element."

    return ann


def create_command_from_kwargs(
    command_class: Type[cheek.command_base.Command], kwargs: dict[str, Any]
) -> cheek.command_base.Command:
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


def create_click_param(field_name: str, field_info: pydantic.fields.FieldInfo) -> click.Parameter:
    "Create a click Parameter from a pydantic field."
    python_type = field_info_to_python_type(field_info)
    return click.Option(
        [f"--{field_name}"],
        type=python_type,
        default=field_info.default,
        required=field_info.is_required(),
        show_default=True,
    )


def create_click_callback(command_class):
    "Create a callback for a click command from a Command class."

    def cmd_func(**kwargs):
        command_instance = create_command_from_kwargs(command_class, kwargs)
        log.info(command_instance)
        results = cheek.command_base.do(command_instance)
        print(results)

    return cmd_func


def create_cli():
    """Build the command group for the CLI.

    Returns:
        click.Group: The command group.
    """

    cli = click.Group()

    # For each registered Command subclass, construct a CLI command.
    for command_class in cheek.commands.all_command_classes():
        # TODO: For enum parameter types, we need to create a click.Choice or something like that.

        # Loop over command.model_fields to figure out CLI arguments. Do this in reverse so that the innermost
        # decoration represents the last argument.
        click_params = [
            create_click_param(field_name, field_info)
            for field_name, field_info in reversed(command_class.model_fields.items())
        ]

        click_command = click.Command(
            name=command_class.user_name(),
            callback=create_click_callback(command_class),
            params=click_params,
        )

        cli.add_command(click_command)

    return cli


def main():
    cli = create_cli()
    cli()


if __name__ == "__main__":
    # TODO: Make this configurable
    logging.basicConfig(level=logging.INFO)
    main()
