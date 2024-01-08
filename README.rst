=====
cheek
=====

Python package for issuing scripting commands to Audacity.

This comprises a set of `Command` classes, each of which represents a single Audacity scripting command. These can
be issued to a running Audacity process with the `cheek.commands.do()` function.

There is also a command-line interface which has a subcomand for each scripting command. This allows you to drive Audacity
using a shell or other non-Python interface.

Command classes
===============

The scripting command classes are implemented in the `cheek.commands` submodule as subclasses of `cheek.commands.Command`. These 
use `pydantic` to express their arguments.

At the time of writing, not all Audacity scripting commands are fully implemented. In particular, those which require parameters
are not all done. Those without parameters are generally complete, though there may be bugs or gaps.

If you want to implement one of the incomplete classes, the main task is to define its parameters in terms of `pydantic` fields. You'll
find examples in the extant `Command` subclasses, e.g. `cheek.commands.SetLabel`.

Basic programmatic use of a command is something like this::

	from cheek.commands import AddLabel, SetLabel, do

	do(
	    AddLabel(),
	    SetLabel(Label=0, Text="Label text", Start=123.456)
	)

From the command line that might look like this::

	cheek AddLabel
	cheek SetLabel --Label 0 --Text "Label text" --Start 123.456

Tests
=====

There are a few tests, though we're very, very far from comprehensive. Really, since real testing would require determing that Audacity
was doing the right thing, it's probably not practical to really test this too fully. But if you've got ideas about testing, 
we could merge them in.

Re-generating the Command subclasses
====================================

We can use the output from the scripting command "GetInfo" to regenerate
all of the Command subclasses. Right now this is a bit rough, but here's
what to do. 

First, execute "GetInfo('Commands', 'JSON')" and capture the output. You can
do this with cheek itself, or pyaudacity, or whatever. The JSON you get is
likely to be invalid at first, so you'll need to clean it up. It should
be clear how to do this.

Save this cleaned-up JSON to a file, e.g. "commands.json". Then run::

	python -m cheek.extract commands.json > src/cheek/commands.py

That should do it. You may want to run this generated Python through
a formatter, though it should be valid Python as-is. Commit the new
commands.py to git and you'll have an updated command set.