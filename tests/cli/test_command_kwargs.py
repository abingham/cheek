from cheek.cli import create_command_from_kwargs
from cheek.commands import SetLabel, OpenProject2


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
        OpenProject2,
        {
            "filename": "foo.txt",
            "addtohistory": True,
        }
    )
    assert cmd == OpenProject2(
        Filename="foo.txt",
        AddToHistory=True
    )

