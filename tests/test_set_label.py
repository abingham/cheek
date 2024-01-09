from pydantic import ValidationError
from cheek.commands import SetLabel
import pytest

def test_basic_command():
    c = SetLabel(Label=42, Text="fnord", Start=1.234, Selected=True)
    command = c.command
    assert command == 'SetLabel: Label="42" Text="fnord" Start="1.234" Selected="1"'


def test_rejects_non_int_label():
    with pytest.raises(ValidationError) as e:
        SetLabel(Label="forty two")






