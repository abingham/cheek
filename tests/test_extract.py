from cheek.extract.arg import Arg
from cheek.extract.command import Command


def test_extract_int_arg():
    spec = {
        "key": "Arg",
        "type": "int",
        "default": 0,
    }
    arg = Arg.from_spec(spec)
    assert arg.name == "Arg"
    assert arg.type == "int"
    assert arg.default == 0


def test_extract_double_arg():
    spec = {
        "key": "Arg",
        "type": "double",
        "default": 4.2,
    }
    arg = Arg.from_spec(spec)
    assert arg.name == "Arg"
    assert arg.type == "double"
    assert arg.default == 4.2


def test_extract_string_arg():
    spec = {
        "key": "Arg",
        "type": "string",
        "default": "foo",
    }
    arg = Arg.from_spec(spec)
    assert arg.name == "Arg"
    assert arg.type == "string"
    assert arg.default == "foo"


def test_extract_bool_arg():
    spec = {
        "key": "Arg",
        "type": "bool",
        "default": "False",
    }
    arg = Arg.from_spec(spec)
    assert arg.name == "Arg"
    assert arg.type == "bool"
    assert arg.default == "False"


def test_extract_enum_arg():
    spec = {
        "key": "Waveform",
        "type": "enum",
        "default": "Sine",
    }
    arg = Arg.from_spec(spec)
    assert arg.name == "Waveform"
    assert arg.type == "enum"
    assert arg.default == "Sine"


def test_extract_SetLabel():
    spec = {
        "id": "SetLabel",
        "name": "Set Label",
        "params": [
            {"key": "Label", "type": "int", "default": 0},
            {"key": "Text", "type": "string", "default": "unchanged"},
            {"key": "Start", "type": "double", "default": "unchanged"},
            {"key": "End", "type": "double", "default": "unchanged"},
            {"key": "Selected", "type": "bool", "default": "unchanged"},
        ],
        "url": "Extra_Menu:_Scriptables_I#set_label",
        "tip": "Sets various values for a label.",
    }
    command = Command.from_spec(spec)
    assert command.name == "SetLabel"
    assert command.doc == "Sets various values for a label."
    assert command.args == [
        Arg(name="Label", type="int", default=0),
        Arg(name="Text", type="string", default=None),
        Arg(name="Start", type="double", default=None),
        Arg(name="End", type="double", default=None),
        Arg(name="Selected", type="bool", default=None),
    ]


def test_extract_Noise():
    spec = {
        "id": "Noise",
        "name": "Noise",
        "params": [
            {
                "key": "Type",
                "type": "enum",
                "default": "White",
                "enum": ["White", "Pink", "Brownian"],
            },
            {"key": "Amplitude", "type": "double", "default": 0.8},
        ],
        "url": "Noise",
        "tip": "Generates one of three different types of noise",
    }
    command = Command.from_spec(spec)


def test_extract_Chirp():
    spec = {
        "id": "Chirp",
        "name": "Chirp",
        "params": [
            {"key": "StartFreq", "type": "double", "default": 440},
            {"key": "EndFreq", "type": "double", "default": 1320},
            {"key": "StartAmp", "type": "double", "default": 0.8},
            {"key": "EndAmp", "type": "double", "default": 0.1},
            {
                "key": "Waveform",
                "type": "enum",
                "default": "Sine",
                "enum": ["Sine", "Square", "Sawtooth", "Square, no alias", "Triangle"],
            },
            {
                "key": "Interpolation",
                "type": "enum",
                "default": "Linear",
                "enum": ["Linear", "Logarithmic"],
            },
        ],
        "url": "Chirp",
        "tip": "Generates an ascending or descending tone of one of four types",
    }
    command = Command.from_spec(spec)
    assert command.name == "Chirp"
    assert (
        command.doc
        == "Generates an ascending or descending tone of one of four types"
    )
    assert command.args == [
        Arg(name="StartFreq", type="double", default=440),
        Arg(name="EndFreq", type="double", default=1320),
        Arg(name="StartAmp", type="double", default=0.8),
        Arg(name="EndAmp", type="double", default=0.1),
        Arg(
            name="Waveform",
            type="enum",
            default="Sine",
            enum_values=["Sine", "Square", "Sawtooth", "Square, no alias", "Triangle"],
        ),
        Arg(
            name="Interpolation",
            type="enum",
            default="Linear",
            enum_values=["Linear", "Logarithmic"],
        ),
    ]
