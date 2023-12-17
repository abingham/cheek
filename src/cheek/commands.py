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


@register_command
class New(Command):
    """Creates a new empty project window, to start working on new or
    imported tracks.

    NOTE: The macros issued from pyaudacity always apply to the last Audacity
    window opened. There's no way to pick which Audacity window macros are
    applied to."""


# The open() function uses the OpenProject2 macro, not the Open macro which only opens the Open dialog.
@register_command
class Open(Command):
    "Opens a project."
    Filename: str | None = None
    AddToHistory: Bool = False
    # TODO: Raise exception if filename not found.

    @classmethod
    def _scripting_command_name(cls):
        return "OpenProject2"


@register_command
class Close(Command):
    """Closes the current project window, prompting you to save your work if you have not saved."""


class NoiseType(Enum):
    WHITE = "White"
    PINK = "Pink"
    BROWNIAN = "Brownian"


class ToneWaveform(Enum):
    SINE = "Sine"
    SQUARE = "Square"
    SAWTOOTH = "Sawtooth"
    SQUARE_NO_ALIAS = "Square, no alias"
    TRIANGLE = "Triangle"  # Note: This option doesn't appear in the scripting documentation but does in the UI.


class PluckFade(Enum):
    ABRUPT = "Abrupt"
    GRADUAL = "Gradual"


class RhythmTrackBeatSound(Enum):
    METRONOME_TICK = "Metronome Tick"
    PING_SHORT = "Ping (short)"
    PING_LONG = "Ping (long)"
    COWBELL = "Cowbell"
    RESONANT_NOISE = "Resonant Noise"
    NOISE_CLICK = "Noise Click"
    DRIP_SHORT = "Drip (short)"
    DRIP_LONG = "Drip (long)"


@register_command
class SetEnvelope(Command):
    """Modify an envelope by specifying a track or channel and a time within it. You cannot yet delete individual envelope points, but can delete the whole envelope using Delete=1."""


@register_command
class SetLabel(Command):
    """Modifies an existing label.

    Audacity Documentation: Modifies an existing label. You must give it the label number.
    """

    Label: int = 0
    Text: str | None = None
    Start: float | None = None
    End: float | None = None
    Selected: Bool | None = None


@register_command
class SaveProject(Command):
    """Various ways to save a project."""


@register_command
class ExportAudio(Command):
    """Export audio files in various formats."""


@register_command
class PageSetup(Command):
    """Opens the standard Page Setup dialog box prior to printing"""


@register_command
class Print(Command):
    """Prints all the waveforms in the current project window (and the contents of Label Tracks or other tracks), with the Timeline above. Everything is printed to one page."""


@register_command
class Exit(Command):
    """Closes all project windows and exits Audacity. If there are any unsaved changes to your project, Audacity will ask if you want to save them."""


@register_command
class Save(Command):
    """Saves the current Audacity project .AUP3 file."""


@register_command
class SaveAs(Command):
    """Same as "Save Project" above, but allows you to save a copy of an open project to a different name or location"""


@register_command
class SaveCopy(Command):
    """Saves the current Audacity project .AUP3 file."""


@register_command
class SaveCompressed(Command):
    """Saves in the audacity .aup3 project file format, but compressed (Suitable for mailing)"""


@register_command
class ExportLabels(Command):
    """Exports audio at one or more labels to file(s)."""


@register_command
class ExportMIDI(Command):
    """Exports MIDI (note tracks) to a MIDI file."""


@register_command
class ImportAudio(Command):
    """Similar to 'Open', except that the file is added as a new track to your existing project."""


@register_command
class ImportLabels(Command):
    """Launches a file selection window where you can choose to import a single text file into the project containing point or region labels. For more information about the syntax for labels files, see Importing and Exporting Labels."""


@register_command
class ImportMIDI(Command):
    """Imports a MIDI (MIDI or MID extension) or Allegro (GRO) file to a Note Track where simple cut-and-paste edits can be performed. The result can be exported with the File > Export> > Export MIDI command. Note: Currently, MIDI and Allegro files cannot be played."""


@register_command
class ImportRaw(Command):
    """Attempts to import an uncompressed audio file that might be "raw" data without any headers to define its format, might have incorrect headers or be otherwise partially corrupted, or might be in a format that Audacity is unable to recognize. Raw data in textual format cannot be imported."""


@register_command
class Undo(Command):
    """Undoes the most recent editing action."""


@register_command
class Redo(Command):
    """Redoes the most recently undone editing action."""


@register_command
class Cut(Command):
    """Removes the selected audio data and/or labels and places these on the Audacity clipboard. By default, any audio or labels to right of the selection are shifted to the left."""


@register_command
class Delete(Command):
    """Removes the selected audio data and/or labels without copying these to the Audacity clipboard. By default, any audio or labels to right of the selection are shifted to the left."""


@register_command
class Copy(Command):
    """Copies the selected audio data to the Audacity clipboard without removing it from the project."""


@register_command
class Paste(Command):
    """Inserts whatever is on the Audacity clipboard at the position of the selection cursor in the project, replacing whatever audio data is currently selected, if any."""


@register_command
class Duplicate(Command):
    """Creates a new track containing only the current selection as a new clip."""


@register_command
class EditMetaData(Command):
    """The Metadata Editor modifies information about a track, such as the artist and genre.  Typically used with MP3 files."""


@register_command
class Preferences(Command):
    """Preferences let you change most of the default behaviors and settings of Audacity. On Mac, Preferences are in the Audacity Menu and the default shortcut is ⌘  + ,."""


@register_command
class SplitCut(Command):
    """Same as Cut, but none of the audio data or labels to right of the selection are shifted."""


@register_command
class SplitDelete(Command):
    """Same as Delete, but none of the audio data or labels to right of the selection are shifted."""


@register_command
class Silence(Command):
    """Replaces the currently selected audio with absolute silence. Does not affect label tracks."""


@register_command
class Trim(Command):
    """Deletes all audio but the selection.  If there are other separate clips in the same track these are not removed or shifted unless trimming the entire length of a clip or clips. Does not affect label tracks."""


@register_command
class Split(Command):
    """Splits the current clip into two clips at the cursor point, or into three clips at the selection boundaries."""


@register_command
class SplitNew(Command):
    """Does a Split Cut on the current selection in the current track, then creates a new track and pastes the selection into the new track."""


@register_command
class Join(Command):
    """If you select an area that overlaps one or more clips, they are all joined into one large clip. Regions in-between clips become silence."""


@register_command
class Disjoin(Command):
    """In a selection region that includes absolute silences, creates individual non-silent clips between the regions of silence. The silence becomes blank space between the clips."""


@register_command
class EditLabels(Command):
    """Brings up a dialog box showing all of your labels in a keyboard-accessible tabular view. Handy buttons in the dialog let you insert or delete a label, or import and export labels to a file. See Label Editor for more details."""


@register_command
class AddLabel(Command):
    """Creates a new, empty label at the cursor or at the selection region."""


@register_command
class AddLabelPlaying(Command):
    """Creates a new, empty label at the current playback or recording position."""


@register_command
class PasteNewLabel(Command):
    """Pastes the text on the Audacity clipboard at the cursor position in the currently selected label track. If there is no selection in the label track a point label is created. If a region is selected in the label track a region label is created. If no label track is selected one is created, and a new label is created."""


@register_command
class TypeToCreateLabel(Command):
    """When a label track has the yellow focus border, if this option is on, just type to create a label.  Otherwise you must create a label first."""


@register_command
class CutLabels(Command):
    """Same as the Cut command, but operates on labeled audio regions."""


@register_command
class DeleteLabels(Command):
    """Same as the Delete command, but operates on labeled audio regions."""


@register_command
class SplitCutLabels(Command):
    """Same as the Split Cut command, but operates on labeled audio regions."""


@register_command
class SplitDeleteLabels(Command):
    """Same as the Split Delete command, but operates on labeled audio regions."""


@register_command
class SilenceLabels(Command):
    """Same as the Silence Audio command, but operates on labeled audio regions."""


@register_command
class CopyLabels(Command):
    """Same as the Copy command, but operates on labeled audio regions."""


@register_command
class SplitLabels(Command):
    """Same as the Split command, but operates on labeled audio regions or points."""


@register_command
class JoinLabels(Command):
    """Same as the Join command, but operates on labeled audio regions or points. You may need to select the audio and use Edit > Clip Boundaries > Join, to join all regions or points."""


@register_command
class DisjoinLabels(Command):
    """Same as the Detach at Silences command, but operates on labeled audio regions."""


@register_command
class SelectAll(Command):
    """Selects all of the audio in all of the tracks."""


@register_command
class SelectNone(Command):
    """Deselects all of the audio in all of the tracks."""


@register_command
class SelCursorStoredCursor(Command):
    """Selects from the position of the cursor to the previously stored cursor position"""


@register_command
class StoreCursorPosition(Command):
    """Stores the current cursor position for use in a later selection"""


@register_command
class ZeroCross(Command):
    """Moves the edges of a selection region (or the cursor position) slightly so they are at a rising zero crossing point."""


@register_command
class SelAllTracks(Command):
    """Extends the current selection up and/or down into all tracks in the project."""


@register_command
class SelSyncLockTracks(Command):
    """Extends the current selection up and/or down into all sync-locked tracks in the currently selected track group."""


@register_command
class SetLeftSelection(Command):
    """When Audacity is playing, recording or paused, sets the left boundary of a potential selection by moving the cursor to the current position of the green playback cursor (or red recording cursor). Otherwise, opens the "Set Left Selection Boundary" dialog for adjusting the time position of the left-hand selection boundary. If there is no selection, moving the time digits backwards creates a selection ending at the former cursor position, and moving the time digits forwards provides a way to move the cursor forwards to an exact point."""


@register_command
class SetRightSelection(Command):
    """When Audacity is playing, recording or paused, sets the right boundary of the selection, thus drawing the selection from the cursor position to the current position of the green playback cursor (or red recording cursor).  Otherwise, opens the "Set Right Selection Boundary" dialog for adjusting the time position of the right-hand selection boundary. If there is no selection, moving the time digits forwards creates a selection starting at the former cursor position, and moving the time digits backwards provides a way to move the cursor backwards to an exact point."""


@register_command
class SelTrackStartToCursor(Command):
    """Selects a region in the selected track(s) from the start of the track to the cursor position."""


@register_command
class SelCursorToTrackEnd(Command):
    """Selects a region in the selected track(s) from the cursor position to the end of the track."""


@register_command
class SelTrackStartToEnd(Command):
    """Selects a region in the selected track(s) from the start of the track to the end of the track."""


@register_command
class SelSave(Command):
    """Stores the end points of a selection for later reuse."""


@register_command
class SelRestore(Command):
    """Retrieves the end points of a previously stored selection."""


@register_command
class ToggleSpectralSelection(Command):
    """Changes between selecting a time range and selecting the last selected spectral selection in that time range. This command toggles the spectral selection even if not in Spectrogram view, but you must be in Spectrogram view to use the spectral selection in one of the Spectral edit effects."""


@register_command
class NextHigherPeakFrequency(Command):
    """When in Spectrogram view, snaps the center frequency to the next higher frequency peak, moving the spectral selection upwards."""


@register_command
class NextLowerPeakFrequency(Command):
    """When in Spectrogram views snaps the center frequency to the next lower frequency peak, moving the spectral selection downwards."""


@register_command
class SelPrevClipBoundaryToCursor(Command):
    """Selects from the current cursor position back to the right-hand edge of the previous clip."""


@register_command
class SelCursorToNextClipBoundary(Command):
    """Selects from the current cursor position forward to the left-hand edge of the next clip."""


@register_command
class SelPrevClip(Command):
    """Moves the selection to the previous clip."""


@register_command
class SelNextClip(Command):
    """Moves the selection to the next clip."""


@register_command
class UndoHistory(Command):
    """Brings up the History window which can then be left open while using Audacity normally. History lists all undoable actions performed in the current project, including importing."""


@register_command
class Karaoke(Command):
    """Brings up the Karaoke window, which displays the labels in a "bouncing ball" scrolling display"""


@register_command
class MixerBoard(Command):
    """Mixer is an alternative view to the audio tracks in the main tracks window. Analogous to a hardware mixer board, each audio track is displayed in a Track Strip."""


@register_command
class ShowExtraMenus(Command):
    """Shows extra menus with many extra less-used commands."""


@register_command
class ShowClipping(Command):
    """Option to show or not show audio that is too loud (in red) on the wave form."""


@register_command
class ZoomIn(Command):
    """Zooms in on the horizontal axis of the audio displaying more detail over a shorter length of time."""


@register_command
class ZoomNormal(Command):
    """Zooms to the default view which displays about one inch per second."""


@register_command
class ZoomOut(Command):
    """Zooms out displaying less detail over a greater length of time."""


@register_command
class ZoomSel(Command):
    """Zooms in or out so that the selected audio fills the width of the window."""


@register_command
class ZoomToggle(Command):
    """Changes the zoom back and forth between two preset levels."""


@register_command
class AdvancedVZoom(Command):
    """Enable for left-click gestures in the vertical scale to control zooming."""


@register_command
class FitInWindow(Command):
    """Zooms out until the entire project just fits in the window."""


@register_command
class FitV(Command):
    """Adjusts the height of all the tracks until they fit in the project window."""


@register_command
class CollapseAllTracks(Command):
    """Collapses all tracks to take up the minimum amount of space."""


@register_command
class ExpandAllTracks(Command):
    """Expands all collapsed tracks to their original size before the last collapse."""


@register_command
class SkipSelStart(Command):
    """When there is a selection, moves the cursor to the start of the selection and removes the selection."""


@register_command
class SkipSelEnd(Command):
    """When there is a selection, moves the cursor to the end of the selection and removes the selection."""


@register_command
class ResetToolbars(Command):
    """Using this command positions all toolbars in default location and size as they were when Audacity was first installed"""


@register_command
class ShowTransportTB(Command):
    """Controls playback and recording and skips to start or end of project when neither playing or recording"""


@register_command
class ShowToolsTB(Command):
    """Chooses various tools for selection, volume adjustment, zooming and time-shifting of audio"""


@register_command
class ShowRecordMeterTB(Command):
    """Displays recording levels and toggles input monitoring when not recording"""


@register_command
class ShowPlayMeterTB(Command):
    """Displays playback levels"""


@register_command
class ShowMixerTB(Command):
    """Adjusts the recording and playback volumes of the devices currently selected in Device Toolbar"""


@register_command
class ShowEditTB(Command):
    """Cut, copy, paste, trim audio, silence audio, undo, redo, zoom tools"""


@register_command
class ShowTranscriptionTB(Command):
    """Plays audio at a slower or faster speed than normal, affecting pitch"""


@register_command
class ShowScrubbingTB(Command):
    """Controls playback and recording and skips to start or end of project when neither playing or recording"""


@register_command
class ShowDeviceTB(Command):
    """Selects audio host, recording device, number of recording channels and playback device"""


@register_command
class ShowSelectionTB(Command):
    """Adjusts cursor and region position by keyboard input"""


@register_command
class ShowSpectralSelectionTB(Command):
    """Displays and lets you adjust the current spectral (frequency) selection without having to be in Spectrogram view"""


@register_command
class RescanDevices(Command):
    """Rescan for audio devices connected to your computer, and update the playback and recording dropdown menus in Device Toolbar"""


@register_command
class PlayStop(Command):
    """Starts and stops playback or stops a recording (stopping does not change the restart position). Therefore using any play or record command after stopping with "Play/Stop" will start playback or recording from the same Timeline position it last started from. You can also assign separate shortcuts for Play and Stop."""


@register_command
class PlayStopSelect(Command):
    """Starts playback like "Play/Stop", but stopping playback sets the restart position to the stop point. When stopped, this command is the same as "Play/Stop". When playing, this command stops playback and moves the cursor (or the start of the selection) to the position where playback stopped."""


@register_command
class Pause(Command):
    """Temporarily pauses playing or recording without losing your place."""


@register_command
class Record1stChoice(Command):
    """Starts recording at the end of the currently selected track(s)."""


@register_command
class Record2ndChoice(Command):
    """Recording begins on a new track at either the current cursor location or at the beginning of the current selection."""


@register_command
class TimerRecord(Command):
    """Brings up the Timer Record dialog."""


@register_command
class PunchAndRoll(Command):
    """Re-record over audio, with a pre-roll of audio that comes before."""


@register_command
class Scrub(Command):
    """Scrubbing is the action of moving the mouse pointer right or left so as to adjust the position, speed or direction of playback, listening to the audio at the same time."""


@register_command
class Seek(Command):
    """Seeking is similar to Scrubbing except that it is playback with skips, similar to using the seek button on a CD player."""


@register_command
class ToggleScrubRuler(Command):
    """Shows (or hides) the scrub ruler, which is just below the timeline."""


@register_command
class CursSelStart(Command):
    """Moves the left edge of the current selection to the center of the screen, without changing the zoom level."""


@register_command
class CursSelEnd(Command):
    """Moves the right edge of the current selection to the center of the screen, without changing the zoom level."""


@register_command
class CursTrackStart(Command):
    """Moves the cursor to the start of the selected track."""


@register_command
class CursTrackEnd(Command):
    """Moves the cursor to the end of the selected track."""


@register_command
class CursPrevClipBoundary(Command):
    """Moves the cursor position back to the right-hand edge of the previous clip"""


@register_command
class CursNextClipBoundary(Command):
    """Moves the cursor position forward to the left-hand edge of the next clip"""


@register_command
class CursProjectStart(Command):
    """Moves the cursor to the beginning of the project."""


@register_command
class CursProjectEnd(Command):
    """Moves the cursor to the end of the project."""


@register_command
class SoundActivationLevel(Command):
    """Sets the activation level above which Sound Activated Recording will record."""


@register_command
class SoundActivation(Command):
    """Toggles on and off the Sound Activated Recording option."""


@register_command
class PinnedHead(Command):
    """You can change Audacity to play and record with a fixed head pinned to the Timeline.  You can adjust the position of the fixed head by dragging it"""


@register_command
class Overdub(Command):
    """Toggles on and off the Hear other tracks during recording (overdub) option."""


@register_command
class SWPlaythrough(Command):
    """Toggles on and off the Enable audible input monitoring (Software Playthrough) option."""


@register_command
class Resample(Command):
    """Allows you to resample the selected track(s) to a new sample rate for use in the project"""


@register_command
class RemoveTracks(Command):
    """Removes the selected track(s) from the project. Even if only part of a track is selected, the entire track is removed."""


@register_command
class SyncLock(Command):
    """Ensures that length changes occurring anywhere in a defined group of tracks also take place in all audio or label tracks in that group."""


@register_command
class NewMonoTrack(Command):
    """Creates a new empty mono audio track."""


@register_command
class NewStereoTrack(Command):
    """Adds an empty stereo track to the project"""


@register_command
class NewLabelTrack(Command):
    """Adds an empty label track to the project"""


@register_command
class NewTimeTrack(Command):
    """Adds an empty time track to the project.  Time tracks are used to speed up and slow down audio."""


@register_command
class StereoToMono(Command):
    """Converts the selected stereo track(s) into the same number of mono tracks, combining left and right channels equally by averaging the volume of both channels."""


@register_command
class MixAndRender(Command):
    """Mixes down all selected tracks to a single mono or stereo track, rendering to the waveform all real-time transformations that had been applied (such as track gain, panning, amplitude envelopes or a change in Project Sample Rate)."""


@register_command
class MixAndRenderToNewTrack(Command):
    """Same as Tracks > Mix and Render except that the original tracks are preserved rather than being replaced by the resulting "Mix" track."""


@register_command
class MuteAllTracks(Command):
    """Mutes all the audio tracks in the project as if you had used the mute buttons from the Track Control Panel on each track."""


@register_command
class UnmuteAllTracks(Command):
    """Unmutes all the audio tracks in the project as if you had released the mute buttons from the Track Control Panel on each track."""


@register_command
class MuteTracks(Command):
    """Mutes the selected tracks."""


@register_command
class UnmuteTracks(Command):
    """Unmutes the selected tracks."""


@register_command
class PanLeft(Command):
    """Pan selected audio to left speaker"""


@register_command
class PanRight(Command):
    """Pan selected audio centrally."""


@register_command
class PanCenter(Command):
    """Pan selected audio to right speaker."""


@register_command
class Align_EndToEnd(Command):
    """Aligns the selected tracks one after the other, based on their top-to-bottom order in the project window."""


@register_command
class Align_Together(Command):
    """Align the selected tracks so that they start at the same (averaged) start time."""


@register_command
class Align_StartToZero(Command):
    """Aligns the start of selected tracks with the start of the project."""


@register_command
class Align_StartToSelStart(Command):
    """Aligns the start of selected tracks with the current cursor position or with the start of the current selection."""


@register_command
class Align_StartToSelEnd(Command):
    """Aligns the start of selected tracks with the end of the current selection."""


@register_command
class Align_EndToSelStart(Command):
    """Aligns the end of selected tracks with the current cursor position or with the start of the current selection."""


@register_command
class Align_EndToSelEnd(Command):
    """Aligns the end of selected tracks with the end of the current selection."""


@register_command
class MoveSelectionWithTracks(Command):
    """Toggles on/off the selection moving with the realigned tracks, or staying put."""


@register_command
class SortByTime(Command):
    """Sort tracks in order of start time."""


@register_command
class SortByName(Command):
    """Sort tracks in order by name."""


@register_command
class ManageGenerators(Command):
    """Selecting this option from the Effect Menu (or the Generate Menu or Analyze Menu) takes you to a dialog where you can enable or disable particular Effects, Generators and Analyzers in Audacity. Even if you do not add any third-party plugins, you can use this to make the Effect menu shorter or longer as required.  For details see Plugin Manager."""


@register_command
class BuiltIin(Command):
    """Shows the list of available Audacity built-in effects but only if the user has effects "Grouped by Type" in Effects Preferences."""


@register_command
class Nyquist(Command):
    """Shows the list of available Nyquist effects but only if the user has effects "Grouped by Type" in Effects Preferences."""


class ChirpWaveform(Enum):
    SINE = "Sine"
    SQUARE = "Square"
    SAWTOOTH = "Sawtooth"
    SQUARE_NO_ALIAS = "Square, no alias"
    TRIANGLE = "Triangle"  # Note: This option doesn't appear in the scripting documentation but does in the UI.


class ChirpInterpolation(Enum):
    LINEAR = "Linear"
    LOGARITHMIC = "Logarithmic"


@register_command
class Chirp(Command):
    """Generates four different types of tone waveforms like the Tone Generator, but additionally allows setting of the starting and ending amplitude and frequency."""

    StartFreq: float = 440
    EndFreq: float = 1320
    StartAmp: float = 0.8
    EndAmp: float = 0.1
    Waveform: ChirpWaveform = ChirpWaveform.SINE
    Interpolation: ChirpInterpolation = ChirpInterpolation.LINEAR


@register_command
class DtmfTones(Command):
    """Generates dual-tone multi-frequency (DTMF) tones like those produced by the keypad on telephones."""

    # TODO
    # string Sequence, (default:audacity)
    # double Duty Cycle, (default:55)
    # double Amplitude, (default:0.8)


@register_command
class Noise(Command):
    """Generates 'white', 'pink' or 'brown' noise."""

    # TODO
    # enum Type, (default:White)
    #  White
    #  Pink
    #  Brownian
    # double Amplitude, (default:0.8)


@register_command
class Tone(Command):
    """Generates one of four different tone waveforms: Sine, Square, Sawtooth or Square (no alias), and a frequency between 1 Hz and half the current [[Audio Settings Preferences|Project Sample Rate."""

    # TODO
    # double Frequency, (default:440)
    # double Amplitude, (default:0.8)
    # enum Waveform, (default:Sine)

    #  Sine
    #  Square
    #  Sawtooth
    #  Square, no alias
    # enum Interpolation, (default:Linear)

    #  Linear
    #  Logarithmic


@register_command
class Pluck(Command):
    """A synthesized pluck tone with abrupt or gradual fade-out, and selectable pitch corresponding to a MIDI note."""

    # TODO
    # int pitch, (default:0)
    # enum fade, (default:Abrupt)

    #  Abrupt
    #  Gradual
    # double dur, (default:0)


@register_command
class RhythmTrack(Command):
    """Generates a track with regularly spaced sounds at a specified tempo and number of beats per measure (bar)."""

    # TODO
    # double tempo, (default:0)
    # int timesig, (default:0)
    # double swing, (default:0)
    # int bars, (default:0)
    # double click-track-dur, (default:0)
    # double offset, (default:0)
    # enum click-type, (default:Metronome)

    #  Metronome
    #  Ping (short)
    #  Ping (long)
    #  Cowbell
    #  ResonantNoise
    #  NoiseClick
    #  Drip (short)
    #  Drip (long)
    # int high, (default:0)
    # int low, (default:0)


@register_command
class RissetDrum(Command):
    """Produces a realistic drum sound."""

    # TODO
    # double freq, (default:0)
    # double decay, (default:0)
    # double cf, (default:0)
    # double bw, (default:0)
    # double noise, (default:0)
    # double gain, (default:0)


@register_command
class ManageEffects(Command):
    """Selecting this option from the Effect Menu (or the Generate Menu or Analyze Menu) takes you to a dialog where you can enable or disable particular Effects, Generators and Analyzers in Audacity. Even if you do not add any third-party plugins, you can use this to make the Effect menu shorter or longer as required.  For details see Plugin Manager."""


@register_command
class RepeatLastEffect(Command):
    """Repeats the last used effect at its last used settings and without displaying any dialog."""


@register_command
class LADSPA(Command):
    """Shows the list of available LADSPA effects but only if the user has effects "Grouped by Type" in Effects Preferences."""


@register_command
class Amplify(Command):
    """Increases or decreases the volume of the audio you have selected."""

    # TODO
    # float Ratio, (default:0.9)
    # bool AllowClipping, (default:False)


@register_command
class AutoDuck(Command):
    """Reduces (ducks) the volume of one or more tracks whenever the volume of a specified "control" track reaches a particular level. Typically used to make a music track softer whenever speech in a commentary track is heard."""

    # TODO
    # double DuckAmountDb, (default:-12)
    # double InnerFadeDownLen, (default:0)
    # double InnerFadeUpLen, (default:0)
    # double OuterFadeDownLen, (default:0.5)
    # double OuterFadeUpLen, (default:0.5)
    # double ThresholdDb, (default:-30)
    # double MaximumPause, (default:1)


@register_command
class BassAndTreble(Command):
    """Increases or decreases the lower  frequencies  and higher frequencies of your audio independently; behaves just like the bass and treble controls on a stereo system."""

    # TODO
    # double Bass, (default:0)
    # double Treble, (default:0)
    # double Gain, (default:0)
    # bool Link Sliders, (default:False)


@register_command
class ChangePitch(Command):
    """Change the pitch of a selection without changing its tempo."""

    # TODO
    # double Percentage, (default:0)
    # bool SBSMS, (default:False)


@register_command
class ChangeSpeed(Command):
    """Change the speed of a selection, also changing its pitch."""

    # TODO
    # double Percentage, (default:0)


@register_command
class ChangeTempo(Command):
    """Change the tempo and length (duration) of a selection without changing its pitch."""

    # TODO
    # double Percentage, (default:0)
    # bool SBSMS, (default:False)


@register_command
class ClickRemoval(Command):
    """Click Removal is designed to remove clicks on audio tracks and is especially suited to declicking recordings made from vinyl records."""

    # TODO
    # int Threshold, (default:200)
    # int Width, (default:20)


@register_command
class Compressor(Command):
    """Compresses the dynamic range by two alternative methods. The default "RMS" method makes the louder parts softer, but leaves the quieter audio alone. The alternative "peaks" method makes the entire audio louder, but amplifies the louder parts less than the quieter parts. Make-up gain can be applied to either method, making the result as loud as possible without clipping, but not changing the dynamic range further."""

    # TODO
    # double Threshold, (default:-12)
    # double NoiseFloor, (default:-40)
    # double Ratio, (default:2)
    # double AttackTime, (default:0.2)
    # double ReleaseTime, (default:1)
    # bool Normalize, (default:True)
    # bool UsePeak, (default:False)


@register_command
class Distortion(Command):
    """Use the Distortion effect to make the audio sound distorted. By distorting the waveform the frequency content is changed, which will often make the sound "crunchy" or "abrasive".  Technically this effect is a waveshaper. The result of waveshaping is equivalent to applying non-linear amplification to the audio waveform. Preset shaping functions are provided, each of which produces a different type of distortion."""

    # TODO
    # enum Type, (default:Hard Clipping)
    #  Hard Clipping
    #  Soft Clipping
    #  Soft Overdrive
    #  Medium Overdrive
    #  Hard Overdrive
    #  Cubic Curve (odd harmonics)
    #  Even Harmonics
    #  Expand and Compress
    #  Leveller
    #  Rectifier Distortion
    #  Hard Limiter 1413
    # bool DC Block, (default:False)
    # double Threshold dB, (default:-6)
    # double Noise Floor, (default:-70)
    # double Parameter 1, (default:50)
    # double Parameter 2, (default:50)
    # int Repeats, (default:1)


@register_command
class Echo(Command):
    """Repeats the selected audio again and again, normally softer each time and normally not blended into the original sound until some time after it starts. The delay time between each repeat is fixed, with no pause in between each repeat. For a more configurable echo effect with a variable delay time and pitch-changed echoes, see Delay."""

    # TODO
    # float Delay, (default:1)
    # float Decay, (default:0.5)


@register_command
class FadeIn(Command):
    """Applies a linear fade-in to the selected audio - the rapidity of the fade-in depends entirely on the length of the selection it is applied to.  For a more customizable logarithmic fade, use the Envelope Tool on the Tools Toolbar."""


@register_command
class FadeOut(Command):
    """Applies a linear fade-out to the selected audio - the rapidity of the fade-out depends entirely on the length of the selection it is applied to.  For a more customizable logarithmic fade, use the Envelope Tool on the Tools Toolbar."""


@register_command
class FilterCurve(Command):
    """Adjusts the volume levels of particular frequencies"""

    # TODO
    # size_t FilterLength, (default:8191)
    # bool InterpolateLin, (default:False)
    # enum InterpolationMethod, (default:B-spline)

    #  B-spline
    #  Cosine
    #  Cubic
    # double f0, (default:0)
    # double v0, (default:0)


@register_command
class GraphicEq(Command):
    """Adjusts the volume levels of particular frequencies"""

    # TODO
    # size_t FilterLength, (default:8191)
    # bool InterpolateLin, (default:False)
    # enum InterpolationMethod, (default:B-spline)

    #  B-spline
    #  Cosine
    #  Cubic
    # double f0, (default:0)
    # double v0, (default:0)


@register_command
class Invert(Command):
    """This effect flips the audio samples upside-down.  This normally does not affect the sound of the audio at all.  It is occasionally useful for vocal removal."""


@register_command
class LoudnessNormalization(Command):
    """Changes the perceived loudness of the audio."""

    # TODO
    # bool StereoIndependent, (default:False)
    # double LUFSLevel, (default:-23)
    # double RMSLevel, (default:-20)
    # bool DualMono, (default:True)
    # int NormalizeTo, (default:0)


@register_command
class NoiseReduction(Command):
    """This effect is ideal for reducing constant background noise such as fans, tape noise, or hums.  It will not work very well for removing talking or music in the background.  More details hereThis effect is not currently available from scripting."""


@register_command
class Normalize(Command):
    """Use the Normalize effect to set the maximum amplitude of a track, equalize the amplitudes of the left and right channels of a stereo track and optionally remove any DC offset from the track"""

    # TODO
    # double PeakLevel, (default:-1)
    # bool ApplyGain, (default:True)
    # bool RemoveDcOffset, (default:True)
    # bool StereoIndependent, (default:False)


@register_command
class Paulstretch(Command):
    """Use Paulstretch only for an extreme time-stretch or "stasis" effect, This may be useful for synthesizer pad sounds, identifying performance glitches or just creating interesting aural textures. Use Change Tempo or Sliding Time Scale rather than Paulstretch for tasks like slowing down a song to a "practice" tempo."""

    # TODO
    # float Stretch Factor, (default:10)
    # float Time Resolution, (default:0.25)


@register_command
class Phaser(Command):
    """The name "Phaser" comes from "Phase Shifter", because it works by combining phase-shifted signals with the original signal.  The movement of the phase-shifted signals is controlled using a Low Frequency Oscillator (LFO)."""

    # TODO
    # int Stages, (default:2)
    # int DryWet, (default:128)
    # double Freq, (default:0.4)
    # double Phase, (default:0)
    # int Depth, (default:100)
    # int Feedback, (default:0)
    # double Gain, (default:-6)


@register_command
class Repair(Command):
    """Fix one particular short click, pop or other glitch no more than 128 samples long."""


@register_command
class Repeat(Command):
    """Repeats the selection the specified number of times."""

    # TODO
    # int Count, (default:1)


@register_command
class Reverb(Command):
    """A configurable stereo reverberation effect with built-in and user-added presets. It can be used to add ambience (an impression of the space in which a sound occurs) to a mono sound. Also use it to increase reverberation in stereo audio that sounds too "dry" or "close"."""

    # TODO
    # double RoomSize, (default:75)
    # double Delay, (default:10)
    # double Reverberance, (default:50)
    # double HfDamping, (default:50)
    # double ToneLow, (default:100)
    # double ToneHigh, (default:100)
    # double WetGain, (default:-1)
    # double DryGain, (default:-1)
    # double StereoWidth, (default:100)
    # bool WetOnly, (default:False)


@register_command
class Reverse(Command):
    """Reverses the selected audio; after the effect the end of the audio will be heard first and the beginning last."""


@register_command
class SlidingStretch(Command):
    """This effect allows you to make a continuous change to the tempo and/or pitch of a selection by choosing initial and/or final change values."""

    # TODO
    # double RatePercentChangeStart, (default:0)
    # double RatePercentChangeEnd, (default:0)
    # double PitchHalfStepsStart, (default:0)
    # double PitchHalfStepsEnd, (default:0)
    # double PitchPercentChangeStart, (default:0)
    # double PitchPercentChangeEnd, (default:0)


@register_command
class TruncateSilence(Command):
    """Automatically try to find and eliminate audible silences. Do not use this with faded audio."""

    # TODO
    # double Threshold, (default:-20)
    # enum Action, (default:Truncate Detected Silence)

    #  Truncate Detected Silence
    #  Compress Excess Silence
    # double Minimum, (default:0.5)
    # double Truncate, (default:0.5)
    # double Compress, (default:50)
    # bool Independent, (default:False)


@register_command
class Wahwah(Command):
    """Rapid tone quality variations, like that guitar sound so popular in the 1970's."""

    # TODO
    # double Freq, (default:1.5)
    # double Phase, (default:0)
    # int Depth, (default:70)
    # double Resonance, (default:2.5)
    # int Offset, (default:30)
    # double Gain, (default:-6)


@register_command
class AdjustableFade(Command):
    """enables you to control the shape of the fade (non-linear fading) to be applied by adjusting various parameters; allows partial (that is not from or to zero) fades up or down."""

    # TODO
    # enum type, (default:Up)
    #  Up
    #  Down
    #  SCurveUp
    #  SCurveDown
    # double curve, (default:0)
    # enum units, (default:Percent)

    #  Percent
    #  dB
    # double gain0, (default:0)
    # double gain1, (default:0)
    # enum preset, (default:None)

    #  None
    #  LinearIn
    #  LinearOut
    #  ExponentialIn
    #  ExponentialOut
    #  LogarithmicIn
    #  LogarithmicOut
    #  RoundedIn
    #  RoundedOut
    #  CosineIn
    #  CosineOut
    #  SCurveIn
    #  SCurveOut


@register_command
class ClipFix(Command):
    """Clip Fix attempts to reconstruct clipped regions by interpolating the lost signal."""

    # TODO
    # double threshold, (default:0)
    # double gain, (default:0)


@register_command
class CrossfadeClips(Command):
    """Use Crossfade Clips to apply a simple crossfade to a selected pair of clips in a single audio track."""

    # TODO
    #


@register_command
class CrossfadeTracks(Command):
    """Use Crossfade Tracks to make a smooth transition between two overlapping tracks one above the other. Place the track to be faded out above the track to be faded in then select the overlapping region in both tracks and apply the effect."""

    # TODO
    # enum type, (default:ConstantGain)
    #  ConstantGain
    #  ConstantPower1
    #  ConstantPower2
    #  CustomCurve
    # double curve, (default:0)
    # enum direction, (default:Automatic)

    #  Automatic
    #  OutIn
    #  InOut


@register_command
class Delay(Command):
    """A configurable delay effect with variable delay time and pitch shifting of the delays."""

    # TODO
    # enum delay-type, (default:Regular)
    #  Regular
    #  BouncingBall
    #  ReverseBouncingBall
    # double dgain, (default:0)
    # double delay, (default:0)
    # enum pitch-type, (default:PitchTempo)

    #  PitchTempo
    #  LQPitchShift
    # double shift, (default:0)
    # int number, (default:0)
    # enum constrain, (default:Yes)

    #  Yes
    #  No


@register_command
class HighPassFilter(Command):
    """Passes frequencies above its cutoff frequency and attenuates frequencies below its cutoff frequency."""

    # TODO
    # double frequency, (default:0)
    # enum rolloff, (default:dB6)

    #  dB6
    #  dB12
    #  dB24
    #  dB36
    #  dB48


@register_command
class Limiter(Command):
    """Limiter passes signals below a specified input level unaffected or gently reduced, while preventing the peaks of stronger signals from exceeding this threshold.  Mastering engineers often use this type of dynamic range compression combined with make-up gain to increase the perceived loudness of an audio recording during the audio mastering process."""

    # TODO
    # enum type, (default:SoftLimit)
    #  SoftLimit
    #  HardLimit
    #  SoftClip
    #  HardClip
    # double gain-L, (default:0)
    # double gain-R, (default:0)
    # double thresh, (default:0)
    # double hold, (default:0)
    # enum makeup, (default:No)

    #  No
    #  Yes


@register_command
class LowPassFilter(Command):
    """Passes frequencies below its cutoff frequency and attenuates frequencies above its cutoff frequency."""

    # TODO
    # double frequency, (default:0)
    # enum rolloff, (default:dB6)

    #  dB6
    #  dB12
    #  dB24
    #  dB36
    #  dB48


@register_command
class NotchFilter(Command):
    """Greatly attenuate ("notch out"), a narrow frequency band. This is a good way to remove mains hum or a whistle confined to a specific frequency with minimal damage to the remainder of the audio."""

    # TODO
    # double frequency, (default:0)
    # double q, (default:0)


@register_command
class SpectralEditMultiTool(Command):
    """When the selected track is in spectrogram or spectrogram log(f) view, applies a  notch filter, high pass filter or low pass filter according to the spectral selection made. This effect can also be used to change the audio quality as an alternative to using Equalization."""

    # TODO
    #


@register_command
class SpectralEditParametricEq(Command):
    """When the selected track is in spectrogram or spectrogram log(f) view and the spectral selection has a center frequency and an upper and lower boundary, performs the specified band cut or band boost. This can be used as an alternative to Equalization or may also be useful to repair damaged audio by reducing frequency spikes or boosting other frequencies to mask spikes."""

    # TODO
    # double control-gain, (default:0)


@register_command
class SpectralEditShelves(Command):
    """When the selected track is in spectrogram or spectrogram log(f) view, applies either a low- or high-frequency shelving filter or both filters, according to the spectral selection made. This can be used as an alternative to Equalization or may also be useful to repair damaged audio by reducing frequency spikes or boosting other frequencies to mask spikes."""

    # TODO
    # double control-gain, (default:0)


@register_command
class StudioFadeOut(Command):
    """Applies a more musical fade out to the selected audio, giving a more pleasing sounding result."""

    # TODO
    #


@register_command
class Tremolo(Command):
    """Modulates the volume of the selection at the depth and rate selected in the dialog. The same as the tremolo effect familiar to guitar and keyboard players."""

    # TODO
    # enum wave, (default:Sine)
    #  Sine
    #  Triangle
    #  Sawtooth
    #  InverseSawtooth
    #  Square
    # int phase, (default:0)
    # int wet, (default:0)
    # double lfo, (default:0)


@register_command
class VocalReductionAndIsolation(Command):
    """Attempts to remove or isolate center-panned audio from a stereo track.  Most  "Remove" options in this effect preserve the stereo image."""

    # TODO
    # enum action, (default:RemoveToMono)
    #  RemoveToMono
    #  Remove
    #  Isolate
    #  IsolateInvert
    #  RemoveCenterToMono
    #  RemoveCenter
    #  IsolateCenter
    #  IsolateCenterInvert
    #  Analyze
    # double strength, (default:0)
    # double low-transition, (default:0)
    # double high-transition, (default:0)


@register_command
class Vocoder(Command):
    """Synthesizes audio (usually a voice) in the left channel of a stereo track with a carrier wave (typically white noise) in the right channel to produce a modified version of the left channel. Vocoding a normal voice with white noise will produce a robot-like voice for special effects."""

    # TODO
    # double dst, (default:0)
    # enum mst, (default:BothChannels)

    #  BothChannels
    #  RightOnly
    # int bands, (default:0)
    # double track-vl, (default:0)
    # double noise-vl, (default:0)
    # double radar-vl, (default:0)
    # double radar-f, (default:0)


@register_command
class ManageAnalyzers(Command):
    """Selecting this option from the Effect Menu (or the Generate Menu or Analyze Menu) takes you to a dialog where you can enable or disable particular Effects, Generators and Analyzers in Audacity. Even if you do not add any third-party plugins, you can use this to make the Effect menu shorter or longer as required.  For details see Plugin Manager."""


@register_command
class ContrastAnalyser(Command):
    """Analyzes a single mono or stereo speech track to determine the average RMS difference in volume (contrast) between foreground speech and background music, audience noise or similar. The purpose is to determine if the speech will be intelligible to the hard of hearing."""


@register_command
class PlotSpectrum(Command):
    """Takes the selected audio (which is a set of sound pressure values at points in time) and converts it to a graph of frequencies against amplitudes."""


@register_command
class FindClipping(Command):
    """Displays runs of clipped samples in a Label Track, as a screen-reader accessible alternative to View > Show Clipping in Waveform. A run must include at least one clipped sample, but may include unclipped samples too."""

    # TODO
    # int Duty Cycle Start, (default:3)
    # int Duty Cycle End, (default:3)


@register_command
class BeatFinder(Command):
    """Attempts to place labels at beats which are much louder than the surrounding audio. It's a fairly rough and ready tool, and will not necessarily work well on a typical modern pop music track with compressed dynamic range. If you do not get enough beats detected, try reducing the "Threshold Percentage" setting."""

    # TODO
    # int thresval, (default:0)


@register_command
class LabelSounds(Command):
    """Divides up a track by placing labels for areas of sound that are separated by silence."""

    # TODO
    # double threshold, (default:0)
    # enum measurement, (default:peak)

    #  peak
    #  avg
    #  rms
    # double sil-dur, (default:0)
    # double snd-dur, (default:0)
    # enum type, (default:before)

    #  before
    #  after
    #  around
    #  between
    # double pre-offset, (default:0)
    # double post-offset, (default:0)
    # string text, (default:"")


@register_command
class ManageTools(Command):
    """Selecting this option from the Effect Menu (or the Generate Menu or Analyze Menu) takes you to a dialog where you can enable or disable particular Effects, Generators and Analyzers in Audacity. Even if you do not add any third-party plugins, you can use this to make the Effect menu shorter or longer as required.  For details see Plugin Manager."""


@register_command
class ManageMacros(Command):
    """Creates a new macro or edits an existing macro."""


@register_command
class ApplyMacro(Command):
    """Displays a menu with list of all your Macros. Selecting any of these Macros by clicking on it will cause that Macro to be applied to the current project."""


@register_command
class Screenshot(Command):
    """A tool, mainly used in documentation, to capture screenshots of Audacity."""

    # TODO
    # string Path, (default:)
    # enum CaptureWhat, (default:Window)

    #  Window
    #  FullWindow
    #  WindowPlus
    #  Fullscreen
    #  Toolbars
    #  Effects
    #  Scriptables
    #  Preferences
    #  Selectionbar
    #  SpectralSelection
    #  Timer
    #  Tools
    #  Transport
    #  Mixer
    #  Meter
    #  PlayMeter
    #  RecordMeter
    #  Edit
    #  Device
    #  Scrub
    #  Play-at-Speed
    #  Trackpanel
    #  Ruler
    #  Tracks
    #  FirstTrack
    #  FirstTwoTracks
    #  FirstThreeTracks
    #  FirstFourTracks
    #  SecondTrack
    #  TracksPlus
    #  FirstTrackPlus
    #  AllTracks
    #  AllTracksPlus
    # enum Background, (default:None)

    #  Blue
    #  White
    #  None
    # bool ToTop, (default:True)


@register_command
class Benchmark(Command):
    """A tool for measuring the performance of one part of Audacity."""


@register_command
class NyquistPrompt(Command):
    """Brings up a dialog where you can enter Nyquist commands. Nyquist is a programming language for generating, processing and analyzing audio."""

    # TODO
    # string Command, (default:)
    # int Version, (default:3)


@register_command
class NyquistPlugInInstaller(Command):
    """A  Nyquist plugin that simplifies the installation of other Nyquist plugins."""

    # TODO
    # string files, (default:)
    # enum overwrite, (default:Disallow)

    #  Disallow
    #  Allow


@register_command
class RegularIntervalLabels(Command):
    """Places labels in a long track so as to divide it into smaller, equally sized  segments."""

    # TODO
    # enum mode, (default:Both)
    #  Both
    #  Number
    #  Interval
    # int totalnum, (default:0)
    # double interval, (default:0)
    # double region, (default:0)
    # enum adjust, (default:No)

    #  No
    #  Yes
    # string labeltext, (default:)
    # enum zeros, (default:TextOnly)

    #  TextOnly
    #  OneBefore
    #  TwoBefore
    #  ThreeBefore
    #  OneAfter
    #  TwoAfter
    #  ThreeAfter
    # int firstnum, (default:0)
    # enum verbose, (default:Details)

    #  Details
    #  Warnings
    #  None


@register_command
class SampleDataExport(Command):
    """Reads the values of successive samples from the selected audio and prints this data to a plain text, CSV or HTML file."""

    # TODO
    # int number, (default:0)
    # enum units, (default:dB)

    #  dB
    #  Linear
    # string filename, (default:)
    # enum fileformat, (default:None)

    #  None
    #  Count
    #  Time
    # enum header, (default:None)

    #  None
    #  Minimal
    #  Standard
    #  All
    # string optext, (default:)
    # enum channel-layout, (default:SameLine)

    #  SameLine
    #  Alternate
    #  LFirst
    # enum messages, (default:Yes)

    #  Yes
    #  Errors
    #  None


@register_command
class SampleDataImport(Command):
    """Reads numeric values from a plain ASCII text file and creates a PCM sample for each numeric value read."""

    # TODO
    # string filename, (default:)
    # enum bad-data, (default:ThrowError)

    #  ThrowError
    #  ReadAsZero


@register_command
class ApplyMacrosPalette(Command):
    """Displays a menu with list of all your Macros which can be applied to the current project or to audio files.."""


@register_command
class Macro_FadeEnds(Command):
    """Fades in the first second and fades out the last second of a track."""


@register_command
class Macro_MP3Conversion(Command):
    """Converts MP3."""


@register_command
class FullScreenOnOff(Command):
    """Toggle full screen mode with no title bar"""


@register_command
class Play(Command):
    """Play (or stop) audio"""


@register_command
class Stop(Command):
    """Stop audio"""


@register_command
class PlayOneSec(Command):
    """Plays for one second centered on the current mouse pointer position (not from the current cursor position). See this page for an example."""


@register_command
class PlayToSelection(Command):
    """Plays to or from the current mouse pointer position to or from the start or end of the selection, depending on the pointer position. See this page for more details."""


@register_command
class PlayBeforeSelectionStart(Command):
    """Plays a short period before the start of the selected audio, the period before shares the setting of the cut preview."""


@register_command
class PlayAfterSelectionStart(Command):
    """Plays a short period after the start of the selected audio, the period after shares the setting of the cut preview."""


@register_command
class PlayBeforeSelectionEnd(Command):
    """Plays a short period before the end of the selected audio, the period before shares the setting of the cut preview."""


@register_command
class PlayAfterSelectionEnd(Command):
    """Plays a short period after the end of the selected audio, the period after shares the setting of the cut preview."""


@register_command
class PlayBeforeAndAfterSelectionStart(Command):
    """Plays a short period  before and after the start of the selected audio, the periods before and after share the setting of the cut preview."""


@register_command
class PlayBeforeAndAfterSelectionEnd(Command):
    """Plays a short period  before and after the end of the selected audio, the periods before and after share the setting of the cut preview."""


@register_command
class PlayCutPreview(Command):
    """Plays audio excluding the selection"""


@register_command
class ScrubBackwards(Command):
    """Does nothing, is there so that users can know what the default shortcut key is, and so they can change it in Shortcuts Preferences if they want to."""


@register_command
class ScrubForwards(Command):
    """Does nothing, is there so that users can know what the default shortcut key is, and so they can change it in Shortcuts Preferences if they want to."""


@register_command
class SelectTool(Command):
    """Chooses Selection tool."""


@register_command
class EnvelopeTool(Command):
    """Chooses Envelope tool."""


@register_command
class DrawTool(Command):
    """Chooses Draw tool."""


@register_command
class MultiTool(Command):
    """Chooses the Multi-Tool"""


@register_command
class PrevTool(Command):
    """Cycles backwards through the tools, starting from the currently selected tool: starting from Selection, it would navigate to Multi-tool to Zoom to Draw to Envelope to Selection."""


@register_command
class NextTool(Command):
    """Cycles forwards through the tools, starting from the currently selected tool: starting from Selection, it would navigate to Envelope to Draw to Zoom to Multi-tool to Selection."""


@register_command
class OutputGain(Command):
    """Displays the Playback Volume dialog. You can type a new value for the playback volume (between 0 and 1), or press Tab, then use the left and right arrow keys to adjust the slider."""


@register_command
class OutputGainInc(Command):
    """Each key press will increase the playback volume by 0.1."""


@register_command
class OutputGainDec(Command):
    """Each key press will decrease the playback volume by 0.1."""


@register_command
class InputGain(Command):
    """Displays the Recording Volume dialog. You can type a new value for the recording volume (between 0 and 1), or press Tab, then use the left and right arrow keys to adjust the slider."""


@register_command
class InputGainInc(Command):
    """Each key press will increase the recording volume by 0.1."""


@register_command
class InputGainDec(Command):
    """Each key press will decrease the recording volume by 0.1."""


@register_command
class DeleteKey(Command):
    """Deletes the selection. When focus is in Selection Toolbar, BACKSPACE is not a shortcut but navigates back to the previous digit and sets it to zero."""


@register_command
class DeleteKey2(Command):
    """Deletes the selection."""


@register_command
class TimeShiftLeft(Command):
    """Moves the currently focused audio track (or a separate clip in that track which contains the editing cursor or selection region) one screen pixel to left."""


@register_command
class TimeShiftRight(Command):
    """Moves the currently focused audio track (or a separate clip in that track which contains the editing cursor or selection region) one screen pixel to right."""


@register_command
class PlayAtSpeed(Command):
    """Play audio at a faster or slower speed"""


@register_command
class PlayAtSpeedLooped(Command):
    """Combines looped play and play at speed"""


@register_command
class PlayAtSpeedCutPreview(Command):
    """Combines cut preview and play at speed"""


@register_command
class SetPlaySpeed(Command):
    """Displays the Playback Speed dialog. You can type a new value for the playback volume (between 0 and 1), or press Tab, then use the left and right arrow keys to adjust the slider."""


@register_command
class PlaySpeedInc(Command):
    """Each key press will increase the playback speed by 0.1."""


@register_command
class PlaySpeedDec(Command):
    """Each key press will decrease the playback speed by 0.1."""


@register_command
class SeekLeftShort(Command):
    """Skips the playback cursor back one second by default."""


@register_command
class SeekRightShort(Command):
    """Skips the playback cursor forward one second by default."""


@register_command
class SeekLeftLong(Command):
    """Skips the playback cursor back 15 seconds by default."""


@register_command
class SeekRightLong(Command):
    """Skips the playback cursor forward 15 seconds by default."""


@register_command
class InputDevice(Command):
    """Displays the Select recording Device dialog for choosing the recording device, but only if the "Recording Device" dropdown menu in Device Toolbar has entries for devices. Otherwise, an recording error message will be displayed."""


@register_command
class OutputDevice(Command):
    """Displays the Select Playback Device dialog for choosing the playback device, but only if the "Playback Device" dropdown menu in Device Toolbar has entries for devices. Otherwise, an error message will be displayed."""


@register_command
class AudioHost(Command):
    """Displays the Select Audio Host dialog for choosing the particular interface with which Audacity communicates with your chosen playback and recording devices."""


@register_command
class InputChannels(Command):
    """Displays the Select Recording Channels dialog for choosing the number of channels to be recorded by the chosen recording device."""


@register_command
class SnapToOff(Command):
    """Equivalent to setting the Snap To control in Selection Toolbar to "Off"."""


@register_command
class SnapToNearest(Command):
    """Equivalent to setting the Snap To control in Selection Toolbar to "Nearest"."""


@register_command
class SnapToPrior(Command):
    """Equivalent to setting the Snap To control in Selection Toolbar to "Prior"."""


@register_command
class SelStart(Command):
    """Select from cursor to start of track"""


@register_command
class SelEnd(Command):
    """Select from cursor to end of track"""


@register_command
class SelExtLeft(Command):
    """Increases the size of the selection by extending it to the left. The amount of increase is dependent on the zoom level. If there is no selection one is created starting at the cursor position."""


@register_command
class SelExtRight(Command):
    """Increases the size of the selection by extending it to the right. The amount of increase is dependent on the zoom level. If there is no selection one is created starting at the cursor position."""


@register_command
class SelSetExtLeft(Command):
    """Extend selection left a little (is this a duplicate?)"""


@register_command
class SelSetExtRight(Command):
    """Extend selection right a litlle (is this a duplicate?)"""


@register_command
class SelCntrLeft(Command):
    """Decreases the size of the selection by contracting it from the right. The amount of decrease is dependent on the zoom level. If there is no selection no action is taken."""


@register_command
class SelCntrRight(Command):
    """Decreases the size of the selection by contracting it from the left. The amount of decrease is dependent on the zoom level. If there is no selection no action is taken."""


@register_command
class MoveToPrevLabel(Command):
    """Moves selection to the previous label"""


@register_command
class MoveToNextLabel(Command):
    """Moves selection to the next label"""


@register_command
class MinutesandSeconds(Command):
    """Changes the Timeline display format to Minutes and Seconds (default setting)."""


@register_command
class BeatsandMeasures(Command):
    """Changes the Timeline display format to Beats and Measures."""


@register_command
class PrevFrame(Command):
    """Move backward through currently focused toolbar in Upper Toolbar dock area, Track View and currently focused toolbar in Lower Toolbar dock area.  Each use moves the keyboard focus as indicated."""


@register_command
class NextFrame(Command):
    """Move forward through currently focused toolbar in Upper Toolbar dock area, Track View and currently focused toolbar in Lower Toolbar dock area.  Each use moves the keyboard focus as indicated."""


@register_command
class PrevTrack(Command):
    """Focus one track up"""


@register_command
class NextTrack(Command):
    """Focus one track down"""


@register_command
class FirstTrack(Command):
    """Focus on first track"""


@register_command
class LastTrack(Command):
    """Focus on last track"""


@register_command
class ShiftUp(Command):
    """Focus one track up and select it"""


@register_command
class ShiftDown(Command):
    """Focus one track down and select it"""


@register_command
class Toggle(Command):
    """Toggle focus on current track"""


@register_command
class ToggleAlt(Command):
    """Toggle focus on current track"""


@register_command
class CursorLeft(Command):
    """When not playing audio, moves the editing cursor one screen pixel to left. When a Snap option is chosen, moves the cursor to the preceding unit of time as determined by the current selection format. If the key is held down, the cursor speed depends on the length of the tracks. When playing audio, moves the playback cursor as described at "Cursor Short Jump Left" """


@register_command
class CursorRight(Command):
    """When not playing audio, moves the editing cursor one screen pixel to right. When a Snap option is chosen, moves the cursor to the following unit of time as determined by the current selection format. If the key is held down, the cursor speed depends on the length of the tracks. When playing audio, moves the playback cursor as described at "Cursor Short Jump Right" """


@register_command
class CursorShortJumpLeft(Command):
    """When not playing audio, moves the editing cursor one second left by default. When playing audio, moves the playback cursor one second left by default. The default value can be changed by adjusting the "Short Period" under "Seek Time when playing" in Playback Preferences."""


@register_command
class CursorShortJumpRight(Command):
    """When not playing audio, moves the editing cursor one second right by default. When playing audio, moves the playback cursor one second right by default. The default value can be changed by adjusting the "Short Period" under "Seek Time when playing" in Playback Preferences."""


@register_command
class CursorLongJumpLeft(Command):
    """When not playing audio, moves the editing cursor 15 seconds left by default. When playing audio, moves the playback cursor 15 seconds left by default. The default value can be changed by adjusting the "Long Period" under "Seek Time when playing" in Playback Preferences."""


@register_command
class CursorLongJumpRight(Command):
    """When not playing audio, moves the editing cursor 15 seconds right by default. When playing audio, moves the playback cursor 15 seconds right by default. The default value can be changed by adjusting the "Long Period" under "Seek Time when playing" in Playback Preferences."""


@register_command
class ClipLeft(Command):
    """Moves the currently focused audio track (or a separate clip in that track which contains the editing cursor or selection region) one screen pixel to left."""


@register_command
class ClipRight(Command):
    """Moves the currently focused audio track (or a separate clip in that track which contains the editing cursor or selection region) one screen pixel to right."""


@register_command
class TrackPan(Command):
    """Brings up the Pan dialog for the focused track where you can enter a pan value, or use the slider for finer control of panning than is available when using the track pan slider."""


@register_command
class TrackPanLeft(Command):
    """Controls the pan slider on the focused track. Each keypress changes the pan value by 10% left."""


@register_command
class TrackPanRight(Command):
    """Controls the pan slider on the focused track. Each keypress changes the pan value by 10% right."""


@register_command
class TrackGain(Command):
    """Brings up the Gain dialog for the focused track where you can enter a gain value, or use the slider for finer control of gain than is available when using the track pan slider."""


@register_command
class TrackGainInc(Command):
    """Controls the gain slider on the focused track. Each keypress increases the gain value by 1 dB."""


@register_command
class TrackGainDec(Command):
    """Controls the gain slider on the focused track. Each keypress decreases the gain value by 1 dB."""


@register_command
class TrackMenu(Command):
    """Opens the Audio Track Dropdown Menu on the focused audio track or other track type. In the audio track dropdown, use Up, and Down, arrow keys to navigate the menu and Enter, to select a menu item. Use Right, arrow to open the "Set Sample Format" and "Set Rate" choices or Left, arrow to leave those choices."""


@register_command
class TrackMute(Command):
    """Toggles the Mute button on the focused track."""


@register_command
class TrackSolo(Command):
    """Toggles the Solo button on the focused track."""


@register_command
class TrackClose(Command):
    """Close (remove) the focused track only."""


@register_command
class TrackMoveUp(Command):
    """Moves the focused track up by one track and moves the focus there."""


@register_command
class TrackMoveDown(Command):
    """Moves the focused track down by one track and moves the focus there."""


@register_command
class TrackMoveTop(Command):
    """Moves the focused track up to the top of the track table and moves the focus there."""


@register_command
class TrackMoveBottom(Command):
    """Moves the focused track down to the bottom of the track table and moves the focus there."""


@register_command
class SelectTime(Command):
    """Modifies the temporal selection.  Start and End are time.  FromEnd allows selection from the end, which is handy to fade in and fade out a track."""

    # TODO
    # double Start, (default:unchanged)
    # double End, (default:unchanged)
    # enum RelativeTo, (default:unchanged)

    #  ProjectStart
    #  Project
    #  ProjectEnd
    #  SelectionStart
    #  Selection
    #  SelectionEnd


@register_command
class SelectFrequencies(Command):
    """Modifies what frequencies are selected.  High and Low are for spectral selection."""

    # TODO
    # double High, (default:unchanged)
    # double Low, (default:unchanged)


@register_command
class SelectTracks(Command):
    """Modifies which tracks are selected.  First and Last are track numbers.  High and Low are for spectral selection.  The Mode parameter allows complex selections, e.g adding or removing tracks from the current selection."""

    # TODO
    # double Track, (default:unchanged)
    # double TrackCount, (default:unchanged)
    # enum Mode, (default:unchanged)

    #  Set
    #  Add
    #  Remove


@register_command
class SetTrackStatus(Command):
    """Sets properties for a track or channel (or both).Name is used to set the name.  It is not used in choosing the track."""

    # TODO
    # string Name, (default:unchanged)
    # bool Selected, (default:unchanged)
    # bool Focused, (default:unchanged)


@register_command
class SetTrackAudio(Command):
    """Sets properties for a track or channel (or both).  Can set pan, gain, mute and solo."""

    # TODO
    # bool Mute, (default:unchanged)
    # bool Solo, (default:unchanged)
    # double Gain, (default:unchanged)
    # double Pan, (default:unchanged)


@register_command
class SetTrackVisuals(Command):
    """Sets visual properties for a track or channel (or both).  SpectralPrefs=1 sets the track to use general preferences, SpectralPrefs=1 per track prefs. When using general preferences, SetPreferences can be used to change a preference and so affect display of the track."""

    # TODO
    # int Height, (default:unchanged)
    # enum Display, (default:unchanged)

    #  Waveform
    #  Spectrogram
    #  Multi-view
    # enum Scale, (default:unchanged)

    #  Linear
    #  dB
    # enum Color, (default:unchanged)

    #  Color0
    #  Color1
    #  Color2
    #  Color3
    # enum VZoom, (default:unchanged)

    #  Reset
    #  Times2
    #  HalfWave
    # double VZoomHigh, (default:unchanged)
    # double VZoomLow, (default:unchanged)
    # bool SpecPrefs, (default:unchanged)
    # bool SpectralSel, (default:unchanged)
    # enum Scheme, (default:unchanged)

    #  Color (default)
    #  Color (classic)
    #  Grayscale
    #  Inverse Grayscale


@register_command
class GetPreference(Command):
    """Gets a single preference setting."""

    # TODO
    # string Name, (default:)


@register_command
class SetPreference(Command):
    """Sets a single preference setting.  Some settings such as them changes require a reload (use Reload=1), but this takes time and slows down a script."""

    # TODO
    # string Name, (default:)
    # string Value, (default:)
    # bool Reload, (default:False)


@register_command
class SetClip(Command):
    """Modify a clip by stating the track or channel a time within it. Color and start position can be set.  Try to avoid overlapping clips, as Audacity will allow it, but does not like them."""

    # TODO
    # double At, (default:unchanged)
    # enum Color, (default:unchanged)

    #  Color0
    #  Color1
    #  Color2
    #  Color3
    # double Start, (default:unchanged)


@register_command
class SetProject(Command):
    """Sets the project window to a particular location and size.  Can also change the caption - but that is cosmetic and may be overwritten again  later by Audacity."""

    # TODO
    # string Name, (default:unchanged)
    # double Rate, (default:unchanged)
    # int X, (default:unchanged)
    # int Y, (default:unchanged)
    # int Width, (default:unchanged)
    # int Height, (default:unchanged)


@register_command
class Select(Command):
    """Selects audio.  Start and End are time.  First and Last are track numbers.  High and Low are for spectral selection.  FromEnd allows selection from the end, which is handy to fade in and fade out a track.  The Mode parameter allows complex selections, e.g adding or removing tracks from the current selection."""

    # TODO
    # double Start, (default:unchanged)
    # double End, (default:unchanged)
    # enum RelativeTo, (default:unchanged)

    #  ProjectStart
    #  Project
    #  ProjectEnd
    #  SelectionStart
    #  Selection
    #  SelectionEnd
    # double High, (default:unchanged)
    # double Low, (default:unchanged)
    # double Track, (default:unchanged)
    # double TrackCount, (default:unchanged)
    # enum Mode, (default:unchanged)

    #  Set
    #  Add
    #  Remove


@register_command
class SetTrack(Command):
    """Sets properties for a track or channel (or both).  Setting one channel of a stereo track can lead to interesting results.  That's most used when setting relative sizing of the two channels.  SpectralPrefs=1 sets the track to use general preferences, SpectralPrefs=1 per track prefs. When using general preferences, SetPreferences can be used to change a preference and so affect display of the track.  Name is used to set the name.  It is not used in choosing the track."""

    # TODO
    # string Name, (default:unchanged)
    # bool Selected, (default:unchanged)
    # bool Focused, (default:unchanged)
    # bool Mute, (default:unchanged)
    # bool Solo, (default:unchanged)
    # double Gain, (default:unchanged)
    # double Pan, (default:unchanged)
    # int Height, (default:unchanged)
    # enum Display, (default:unchanged)

    #  Waveform
    #  Spectrogram
    # enum Scale, (default:unchanged)

    #  Linear
    #  dB
    # enum Color, (default:unchanged)

    #  Color0
    #  Color1
    #  Color2
    #  Color3
    # enum VZoom, (default:unchanged)

    #  Reset
    #  Times2
    #  HalfWave
    # double VZoomHigh, (default:unchanged)
    # double VZoomLow, (default:unchanged)
    # bool SpecPrefs, (default:unchanged)
    # bool SpectralSel, (default:unchanged)
    # bool GrayScale, (default:unchanged)


@register_command
class GetInfo(Command):
    """Gets information in a list in one of three formats."""

    # TODO
    # enum Type, (default:Commands)
    #  Commands
    #  Menus
    #  Preferences
    #  Tracks
    #  Clips
    #  Envelopes
    #  Labels
    #  Boxes
    # enum Format, (default:JSON)

    #  JSON
    #  LISP
    #  Brief


@register_command
class Message(Command):
    """Used in testing.  Sends the Text string back to you."""

    # TODO
    # string Text, (default:Some message)


@register_command
class Help(Command):
    """This is an extract from GetInfo Commands, with just one command."""

    # TODO
    # string Command, (default:Help)
    # enum Format, (default:JSON)

    #  JSON
    #  LISP
    #  Brief


@register_command
class Import2(Command):
    """Imports from a file.  The automation command uses a text box to get the file name rather than a normal file-open dialog."""

    # TODO
    # string Filename, (default:)


@register_command
class Export2(Command):
    """Exports selected audio to a named file.  This version of export has the full set of export options.  However, a current limitation is that the detailed option settings are always stored to and taken from saved preferences.  The net effect is that for a given format, the most recently used options for that format will be used. In the current implementation, NumChannels should be 1 (mono) or 2 (stereo)."""

    # TODO
    # string Filename, (default:exported.wav)
    # int NumChannels, (default:1)


@register_command
class OpenProject2(Command):
    """Opens a project."""

    # TODO
    # string Filename, (default:test.aup3)
    # bool AddToHistory, (default:false)


@register_command
class SaveProject2(Command):
    """Saves a project."""

    # TODO
    # string Filename, (default:name.aup3)
    # bool AddToHistory, (default:False)
    # bool Compress, (default:False)


@register_command
class Drag(Command):
    """Experimental command (called Drag in scripting) that moves the mouse.  An Id can be used to move the mouse into a button to get the hover effect.  Window names can be used instead.  If To is specified, the command does a drag, otherwise just a hover."""

    # TODO
    # int Id, (default:unchanged)
    # string Window, (default:unchanged)
    # double FromX, (default:unchanged)
    # double FromY, (default:unchanged)
    # double ToX, (default:unchanged)
    # double ToY, (default:unchanged)
    # enum RelativeTo, (default:unchanged)

    #  Panel
    #  App
    #  Track0
    #  Track1


@register_command
class CompareAudio(Command):
    """Compares selected range on two tracks.  Reports on the differences and similarities."""

    # TODO
    # float Threshold, (default:0)


@register_command
class QuickHelp(Command):
    """A brief version of help with some of the most essential information."""


@register_command
class Manual(Command):
    """Opens the manual in the default browser."""


@register_command
class Updates(Command):
    """Checks online to see if this is the latest version of Audacity."""


@register_command
class About(Command):
    """Brings a dialog with information about Audacity, such as who wrote it, what features are enabled and the GNU GPL v2 license."""


@register_command
class DeviceInfo(Command):
    """Shows technical information about your detected audio device(s)."""


@register_command
class MidiDeviceInfo(Command):
    """Shows technical information about your detected MIDI device(s)."""


@register_command
class Log(Command):
    """Launches the "Audacity Log" window, the log is largely a debugging aid, having timestamps for each entry"""


@register_command
class CrashReport(Command):
    """Selecting this will generate a Debug report which could be useful in aiding the developers to identify bugs in Audacity or in third-party plugins"""


@register_command
class CheckDeps(Command):
    """Lists any WAV or AIFF audio files that your project depends on, and allows you to copy these files into the project"""


@register_command
class PrevWindow(Command):
    """Navigates to the previous window."""


@register_command
class NextWindow(Command):
    """Navigates to the next window."""
