from cheek.cli import create_command_from_kwargs
from cheek.command_base import SetLabel, Open


def test_set_label():
    cmd = create_command_from_kwargs(
        SetLabel,
        {
            "label": 0,
            "text": "text",
            "start": 0,
            "end": 42
        }
    )
    assert cmd == SetLabel(
        Label=0,
        Text="text",
        Start=0,
        End=42
    )


def test_open():
    cmd = create_command_from_kwargs(
        Open,
        {
            "filename": "foo.txt",
            "addtohistory": True,
        }
    )
    assert cmd == Open(
        Filename="foo.txt",
        AddToHistory=True
    )

