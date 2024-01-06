import bs4

from cheek.extract.arg import Arg
from cheek.extract.command import Command


def test_extract_int_arg():
    html = "<i>int <b>Arg</b>, (default:0)</i>"
    soup = bs4.BeautifulSoup(html, features="html.parser")
    arg = Arg.from_html(soup)
    assert arg.name == "Arg"
    assert arg.type == "int"
    assert arg.default == "0"


def test_extract_double_arg():
    html = "<i>double <b>Arg</b>, (default:4.2)</i>"
    soup = bs4.BeautifulSoup(html, features="html.parser")
    arg = Arg.from_html(soup)
    assert arg.name == "Arg"
    assert arg.type == "double"
    assert arg.default == "4.2"


def test_extract_string_arg():
    html = "<i>string <b>Arg</b>, (default:foo)</i>"
    soup = bs4.BeautifulSoup(html, features="html.parser")
    arg = Arg.from_html(soup)
    assert arg.name == "Arg"
    assert arg.type == "string"
    assert arg.default == "foo"


def test_extract_bool_arg():
    html = "<i>bool <b>Arg</b>, (default:False)</i>"
    soup = bs4.BeautifulSoup(html, features="html.parser")
    arg = Arg.from_html(soup)
    assert arg.name == "Arg"
    assert arg.type == "bool"
    assert arg.default == "False"


def test_extract_enum_arg():
    html = "<i>enum <b>Waveform</b>, (default:Sine)</i><br>"
    soup = bs4.BeautifulSoup(html, features="html.parser")
    arg = Arg.from_html(soup)
    assert arg.name == "Waveform"
    assert arg.type == "enum"
    assert arg.default == "Sine"


def test_extract_SetLabel():
    html = """<tr>
        <td><b>SetLabel:</b>
        </td>
        <td><a href="https://manual.audacityteam.org/man/extra_menu_scriptables_i.html#set_label" title="Extra Menu: Scriptables I">Set Label</a>
        </td>
        <td><i>int <b>Label</b>, (default:0)</i><br>
        <p><i>string <b>Text</b>, (default:unchanged)</i><br>
        <i>double <b>Start</b>, (default:unchanged)</i><br>
        <i>double <b>End</b>, (default:unchanged)</i><br>
        <i>bool <b>Selected</b>, (default:unchanged)</i><br>
        </p>
        </td>
        <td>Modifies an existing label.  You must give it the label number.
        </td></tr>"""
    soup = bs4.BeautifulSoup(html, features="html.parser")
    command = Command.from_html(soup)
    assert command.name == "SetLabel"
    assert command.doc == "Modifies an existing label.  You must give it the label number."
    assert command.args == [
        Arg(name="Label", type="int", default="0"),
        Arg(name="Text", type="string", default=None),
        Arg(name="Start", type="double", default=None),
        Arg(name="End", type="double", default=None),
        Arg(name="Selected", type="bool", default=None),
    ]


def test_extract_Noise():
    html = """<tr>
        <td><b>Noise:</b>
        </td>
        <td><a href="https://manual.audacityteam.org/man/generate_menu.html#noise" title="Generate Menu">Noise</a>
        </td>
        <td><i>enum <b>Type</b>, (default:White)</i><br>
        <ul><li> White</li>
        <li> Pink</li>
        <li> Brownian</li></ul>
        <p><i>double <b>Amplitude</b>, (default:0.8)</i><br>
        </p>
        </td>
        <td>Generates 'white', 'pink' or 'brown' noise.
        </td></tr>
    """
    soup = bs4.BeautifulSoup(html, features="html.parser")
    command = Command.from_html(soup)


def test_extract_Chirp():
    html = """<tr>
        <td><b>Chirp:</b>
        </td>
        <td><a href="https://manual.audacityteam.org/man/generate_menu.html#chirp" title="Generate Menu">Chirp</a>
        </td>
        <td><i>double <b>StartFreq</b>, (default:440)</i><br>
        <p><i>double <b>EndFreq</b>, (default:1320)</i><br>
        <i>double <b>StartAmp</b>, (default:0.8)</i><br>
        <i>double <b>EndAmp</b>, (default:0.1)</i><br>
        <i>enum <b>Waveform</b>, (default:Sine)</i><br>
        </p>
        <ul><li> Sine</li>
        <li> Square</li>
        <li> Sawtooth</li>
        <li> Square, no alias</li></ul>
        <p><i>enum <b>Interpolation</b>, (default:Linear)</i><br>
        </p>
        <ul><li> Linear</li>
        <li> Logarithmic</li></ul>
        </td>
        <td>Generates four different types of tone waveforms like the <a href="https://manual.audacityteam.org/man/scripting_reference.html#Tone">Tone Generator</a>, but additionally allows setting of the starting and ending amplitude and frequency.
        </td></tr>
    """
    soup = bs4.BeautifulSoup(html, features="html.parser")
    command = Command.from_html(soup)
    assert command.name == "Chirp"
    assert (
        command.doc
        == "Generates four different types of tone waveforms like the Tone Generator, but additionally allows setting of the starting and ending amplitude and frequency."
    )
    assert command.args == [
        Arg(name="StartFreq", type="double", default="440"),
        Arg(name="EndFreq", type="double", default="1320"),
        Arg(name="StartAmp", type="double", default="0.8"),
        Arg(name="EndAmp", type="double", default="0.1"),
        Arg(name="Waveform", type="enum", default="Sine", enum_values=["Sine", "Square", "Sawtooth", "Square, no alias"]),
        Arg(name="Interpolation", type="enum", default="Linear", enum_values=["Linear", "Logarithmic"]),
    ]
