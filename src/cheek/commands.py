from enum import Enum

from .command_base import (Bool, Command, all_command_classes, do,
                           register_command)


@register_command
class Amplify(Command):
    "Increases or decreases the volume of the audio you have selected"
    Ratio: float = 0.9
    AllowClipping: Bool = False


@register_command
class AutoDuck(Command):
    'Reduces (ducks) the volume of one or more tracks whenever the volume of a specified "control" track reaches a particular level'
    DuckAmountDb: float = -12
    InnerFadeDownLen: float = 0
    InnerFadeUpLen: float = 0
    OuterFadeDownLen: float = 0.5
    OuterFadeUpLen: float = 0.5
    ThresholdDb: float = -30
    MaximumPause: float = 1


@register_command
class BassAndTreble(Command):
    "Simple tone control effect"
    Bass: float = 0
    Treble: float = 0
    Gain: float = 0
    Link_Sliders: Bool = False


@register_command
class ChangePitch(Command):
    "Changes the pitch of a track without changing its tempo"
    Percentage: float = 0
    SBSMS: Bool = False


@register_command
class ChangeSpeedAndPitch(Command):
    "Changes the speed of a track, also changing its pitch"
    Percentage: float = 0


@register_command
class ChangeTempo(Command):
    "Changes the tempo of a selection without changing its pitch"
    Percentage: float = 0
    SBSMS: Bool = False


class ChirpWaveform(Enum):
    Sine = "Sine"
    Square = "Square"
    Sawtooth = "Sawtooth"
    Square__no_alias = "Square, no alias"
    Triangle = "Triangle"


class ChirpInterpolation(Enum):
    Linear = "Linear"
    Logarithmic = "Logarithmic"


@register_command
class Chirp(Command):
    "Generates an ascending or descending tone of one of four types"
    StartFreq: float = 440
    EndFreq: float = 1320
    StartAmp: float = 0.8
    EndAmp: float = 0.1
    Waveform: ChirpWaveform = ChirpWaveform.Sine
    Interpolation: ChirpInterpolation = ChirpInterpolation.Linear


@register_command
class ClickRemoval(Command):
    "Click Removal is designed to remove clicks on audio tracks"
    Threshold: int = 200
    Width: int = 20


@register_command
class Compressor(Command):
    "Compresses the dynamic range of audio"
    Threshold: float = -12
    NoiseFloor: float = -40
    Ratio: float = 2
    AttackTime: float = 0.2
    ReleaseTime: float = 1
    Normalize: Bool = True
    UsePeak: Bool = False


@register_command
class DtmfTones(Command):
    "Generates dual-tone multi-frequency (DTMF) tones like those produced by the keypad on telephones"
    Sequence: str = "audacity"
    Duty_Cycle: float = 55
    Amplitude: float = 0.8


class DistortionType(Enum):
    Hard_Clipping = "Hard Clipping"
    Soft_Clipping = "Soft Clipping"
    Soft_Overdrive = "Soft Overdrive"
    Medium_Overdrive = "Medium Overdrive"
    Hard_Overdrive = "Hard Overdrive"
    Cubic_Curve__odd_harmonics_ = "Cubic Curve (odd harmonics)"
    Even_Harmonics = "Even Harmonics"
    Expand_and_Compress = "Expand and Compress"
    Leveller = "Leveller"
    Rectifier_Distortion = "Rectifier Distortion"
    Hard_Limiter_1413 = "Hard Limiter 1413"


@register_command
class Distortion(Command):
    "Waveshaping distortion effect"
    Type: DistortionType = DistortionType.Hard_Clipping
    DC_Block: Bool = False
    Threshold_dB: float = -6
    Noise_Floor: float = -70
    Parameter_1: float = 50
    Parameter_2: float = 50
    Repeats: int = 1


@register_command
class Echo(Command):
    "Repeats the selected audio again and again"
    Delay: float = 1
    Decay: float = 0.5


@register_command
class FadeIn(Command):
    "Applies a linear fade-in to the selected audio"


@register_command
class FadeOut(Command):
    "Applies a linear fade-out to the selected audio"


class FilterCurveInterpolationMethod(Enum):
    B_spline = "B-spline"
    Cosine = "Cosine"
    Cubic = "Cubic"


@register_command
class FilterCurve(Command):
    "Adjusts the volume levels of particular frequencies"
    FilterLength: int = 8191
    InterpolateLin: Bool = False
    InterpolationMethod: FilterCurveInterpolationMethod = FilterCurveInterpolationMethod.B_spline


@register_command
class FindClipping(Command):
    "Creates labels where clipping is detected"
    Duty_Cycle_Start: int = 3
    Duty_Cycle_End: int = 3


class GraphicEqInterpolationMethod(Enum):
    B_spline = "B-spline"
    Cosine = "Cosine"
    Cubic = "Cubic"


@register_command
class GraphicEq(Command):
    "Adjusts the volume levels of particular frequencies"
    FilterLength: int = 8191
    InterpolateLin: Bool = False
    InterpolationMethod: GraphicEqInterpolationMethod = GraphicEqInterpolationMethod.B_spline


@register_command
class Invert(Command):
    "Flips the audio samples upside-down, reversing their polarity"


@register_command
class LoudnessNormalization(Command):
    "Sets the loudness of one or more tracks"
    StereoIndependent: Bool = False
    LUFSLevel: float = -23
    RMSLevel: float = -20
    DualMono: Bool = True
    NormalizeTo: int = 0


@register_command
class NoiseReduction(Command):
    "Removes background noise such as fans, tape noise, or hums"


class NoiseType(Enum):
    White = "White"
    Pink = "Pink"
    Brownian = "Brownian"


@register_command
class Noise(Command):
    "Generates one of three different types of noise"
    Type: NoiseType = NoiseType.White
    Amplitude: float = 0.8


@register_command
class Normalize(Command):
    "Sets the peak amplitude of one or more tracks"
    PeakLevel: float = -1
    ApplyGain: Bool = True
    RemoveDcOffset: Bool = True
    StereoIndependent: Bool = False


@register_command
class Paulstretch(Command):
    'Paulstretch is only for an extreme time-stretch or "stasis" effect'
    Stretch_Factor: float = 10
    Time_Resolution: float = 0.25


@register_command
class Phaser(Command):
    "Combines phase-shifted signals with the original signal"
    Stages: int = 2
    DryWet: int = 128
    Freq: float = 0.4
    Phase: float = 0
    Depth: int = 100
    Feedback: int = 0
    Gain: float = -6


@register_command
class Repair(Command):
    "Sets the peak amplitude of a one or more tracks"


@register_command
class Repeat(Command):
    "Repeats the selection the specified number of times"
    Count: int = 1


@register_command
class Reverb(Command):
    'Adds ambience or a "hall effect"'
    RoomSize: float = 75
    Delay: float = 10
    Reverberance: float = 50
    HfDamping: float = 50
    ToneLow: float = 100
    ToneHigh: float = 100
    WetGain: float = -1
    DryGain: float = -1
    StereoWidth: float = 100
    WetOnly: Bool = False


@register_command
class Reverse(Command):
    "Reverses the selected audio"


@register_command
class Silence(Command):
    "Creates audio of zero amplitude"


@register_command
class SlidingStretch(Command):
    "Allows continuous changes to the tempo and/or pitch"
    RatePercentChangeStart: float = 0
    RatePercentChangeEnd: float = 0
    PitchHalfStepsStart: float = 0
    PitchHalfStepsEnd: float = 0
    PitchPercentChangeStart: float = 0
    PitchPercentChangeEnd: float = 0


@register_command
class StereoToMono(Command):
    "Converts stereo tracks to mono"


class ToneWaveform(Enum):
    Sine = "Sine"
    Square = "Square"
    Sawtooth = "Sawtooth"
    Square__no_alias = "Square, no alias"
    Triangle = "Triangle"


class ToneInterpolation(Enum):
    Linear = "Linear"
    Logarithmic = "Logarithmic"


@register_command
class Tone(Command):
    "Generates a constant frequency tone of one of four types"
    Frequency: float = 440
    Amplitude: float = 0.8
    Waveform: ToneWaveform = ToneWaveform.Sine
    Interpolation: ToneInterpolation = ToneInterpolation.Linear


class TruncateSilenceAction(Enum):
    Truncate_Detected_Silence = "Truncate Detected Silence"
    Compress_Excess_Silence = "Compress Excess Silence"


@register_command
class TruncateSilence(Command):
    "Automatically reduces the length of passages where the volume is below a specified level"
    Threshold: float = -20
    Action: TruncateSilenceAction = TruncateSilenceAction.Truncate_Detected_Silence
    Minimum: float = 0.5
    Truncate: float = 0.5
    Compress: float = 50
    Independent: Bool = False


@register_command
class Wahwah(Command):
    "Rapid tone quality variations, like that guitar sound so popular in the 1970's"
    Freq: float = 1.5
    Phase: float = 0
    Depth: int = 70
    Resonance: float = 2.5
    Offset: int = 30
    Gain: float = -6


@register_command
class Aubandpass(Command):
    "n/a"


@register_command
class Audelay(Command):
    "n/a"


@register_command
class Audistortion(Command):
    "n/a"


@register_command
class Audynamicsprocessor(Command):
    "n/a"


@register_command
class Aufilter(Command):
    "n/a"


@register_command
class Augraphiceq(Command):
    "n/a"


@register_command
class Auhighshelffilter(Command):
    "n/a"


@register_command
class Auhipass(Command):
    "n/a"


@register_command
class Aulowshelffilter(Command):
    "n/a"


@register_command
class Aulowpass(Command):
    "n/a"


@register_command
class Aumatrixreverb(Command):
    "n/a"


@register_command
class Aumultibandcompressor(Command):
    "n/a"


@register_command
class Aunbandeq(Command):
    "n/a"


@register_command
class Aunetsend(Command):
    "n/a"


@register_command
class Aunewpitch(Command):
    "n/a"


@register_command
class Auparametriceq(Command):
    "n/a"


@register_command
class Aupeaklimiter(Command):
    "n/a"


@register_command
class Aupitch(Command):
    "n/a"


@register_command
class Aureverb2(Command):
    "n/a"


@register_command
class Aurogerbeep(Command):
    "n/a"


@register_command
class Auroundtripaac(Command):
    "n/a"


@register_command
class Ausampledelay(Command):
    "n/a"


@register_command
class Ausoundfieldpanner(Command):
    "n/a"


@register_command
class Auspatialmixer(Command):
    "n/a"


@register_command
class Ausphericalheadpanner(Command):
    "n/a"


@register_command
class Auvectorpanner(Command):
    "n/a"


@register_command
class Hrtfpanner(Command):
    "n/a"


@register_command
class BeatFinder(Command):
    "GNU General Public License v2.0"
    THRESVAL: int = 0


@register_command
class NyquistPrompt(Command):
    "n/a"


@register_command
class ClipFix(Command):
    "GNU General Public License v2.0"
    THRESHOLD: float = 0
    GAIN: float = 0


class PluckFADE(Enum):
    Abrupt = "Abrupt"
    Gradual = "Gradual"


@register_command
class Pluck(Command):
    "GNU General Public License v2.0"
    PITCH: int = 0
    FADE: PluckFADE = PluckFADE.Abrupt
    DUR: float = 0


class RhythmTrackCLICK_TYPE(Enum):
    Metronome = "Metronome"
    Ping__short_ = "Ping (short)"
    Ping__long_ = "Ping (long)"
    Cowbell = "Cowbell"
    ResonantNoise = "ResonantNoise"
    NoiseClick = "NoiseClick"
    Drip__short_ = "Drip (short)"
    Drip__long_ = "Drip (long)"


@register_command
class RhythmTrack(Command):
    "GNU General Public License v2.0"
    TEMPO: float = 0
    TIMESIG: int = 0
    SWING: float = 0
    BARS: int = 0
    CLICK_TRACK_DUR: float = 0
    OFFSET: float = 0
    CLICK_TYPE: RhythmTrackCLICK_TYPE = RhythmTrackCLICK_TYPE.Metronome
    HIGH: int = 0
    LOW: int = 0


class High_passFilterROLLOFF(Enum):
    dB6 = "dB6"
    dB12 = "dB12"
    dB24 = "dB24"
    dB36 = "dB36"
    dB48 = "dB48"


@register_command
class High_passFilter(Command):
    "GNU General Public License v2.0"
    FREQUENCY: float = 0
    ROLLOFF: High_passFilterROLLOFF = High_passFilterROLLOFF.dB6


class Low_passFilterROLLOFF(Enum):
    dB6 = "dB6"
    dB12 = "dB12"
    dB24 = "dB24"
    dB36 = "dB36"
    dB48 = "dB48"


@register_command
class Low_passFilter(Command):
    "GNU General Public License v2.0"
    FREQUENCY: float = 0
    ROLLOFF: Low_passFilterROLLOFF = Low_passFilterROLLOFF.dB6


class VocoderMST(Enum):
    BothChannels = "BothChannels"
    RightOnly = "RightOnly"


@register_command
class Vocoder(Command):
    "GNU General Public License v2.0"
    DST: float = 0
    MST: VocoderMST = VocoderMST.BothChannels
    BANDS: int = 0
    TRACK_VL: float = 0
    NOISE_VL: float = 0
    RADAR_VL: float = 0
    RADAR_F: float = 0


@register_command
class SpectralEditMultiTool(Command):
    "GNU General Public License v2.0"


@register_command
class SpectralEditParametricEq(Command):
    "GNU General Public License v2.0"
    CONTROL_GAIN: float = 0


@register_command
class SpectralEditShelves(Command):
    "GNU General Public License v2.0 or later"
    CONTROL_GAIN: float = 0


class VocalReductionAndIsolationACTION(Enum):
    RemoveToMono = "RemoveToMono"
    Remove = "Remove"
    Isolate = "Isolate"
    IsolateInvert = "IsolateInvert"
    RemoveCenterToMono = "RemoveCenterToMono"
    RemoveCenter = "RemoveCenter"
    IsolateCenter = "IsolateCenter"
    IsolateCenterInvert = "IsolateCenterInvert"
    Analyze = "Analyze"


@register_command
class VocalReductionAndIsolation(Command):
    "GNU General Public License v2.0"
    ACTION: VocalReductionAndIsolationACTION = VocalReductionAndIsolationACTION.RemoveToMono
    STRENGTH: float = 0
    LOW_TRANSITION: float = 0
    HIGH_TRANSITION: float = 0


@register_command
class NotchFilter(Command):
    "GNU General Public License v2.0 or later"
    FREQUENCY: float = 0
    Q: float = 0


class AdjustableFadeTYPE(Enum):
    Up = "Up"
    Down = "Down"
    SCurveUp = "SCurveUp"
    SCurveDown = "SCurveDown"


class AdjustableFadeUNITS(Enum):
    Percent = "Percent"
    dB = "dB"


class AdjustableFadePRESET(Enum):
    None_ = "None"
    LinearIn = "LinearIn"
    LinearOut = "LinearOut"
    ExponentialIn = "ExponentialIn"
    ExponentialOut = "ExponentialOut"
    LogarithmicIn = "LogarithmicIn"
    LogarithmicOut = "LogarithmicOut"
    RoundedIn = "RoundedIn"
    RoundedOut = "RoundedOut"
    CosineIn = "CosineIn"
    CosineOut = "CosineOut"
    SCurveIn = "SCurveIn"
    SCurveOut = "SCurveOut"


@register_command
class AdjustableFade(Command):
    "GNU General Public License v2.0 or later"
    TYPE: AdjustableFadeTYPE = AdjustableFadeTYPE.Up
    CURVE: float = 0
    UNITS: AdjustableFadeUNITS = AdjustableFadeUNITS.Percent
    GAIN0: float = 0
    GAIN1: float = 0
    PRESET: AdjustableFadePRESET = AdjustableFadePRESET.None_


@register_command
class CrossfadeClips(Command):
    "GNU General Public License v2.0 or later"


class CrossfadeTracksTYPE(Enum):
    ConstantGain = "ConstantGain"
    ConstantPower1 = "ConstantPower1"
    ConstantPower2 = "ConstantPower2"
    CustomCurve = "CustomCurve"


class CrossfadeTracksDIRECTION(Enum):
    Automatic = "Automatic"
    OutIn = "OutIn"
    InOut = "InOut"


@register_command
class CrossfadeTracks(Command):
    "GNU General Public License v2.0 or later"
    TYPE: CrossfadeTracksTYPE = CrossfadeTracksTYPE.ConstantGain
    CURVE: float = 0
    DIRECTION: CrossfadeTracksDIRECTION = CrossfadeTracksDIRECTION.Automatic


class DelayDELAY_TYPE(Enum):
    Regular = "Regular"
    BouncingBall = "BouncingBall"
    ReverseBouncingBall = "ReverseBouncingBall"


class DelayPITCH_TYPE(Enum):
    PitchTempo = "PitchTempo"
    LQPitchShift = "LQPitchShift"
    HQPitchShift = "HQPitchShift"


class DelayCONSTRAIN(Enum):
    Yes = "Yes"
    No = "No"


@register_command
class Delay(Command):
    "GNU General Public License v2.0"
    DELAY_TYPE: DelayDELAY_TYPE = DelayDELAY_TYPE.Regular
    DGAIN: float = 0
    DELAY: float = 0
    PITCH_TYPE: DelayPITCH_TYPE = DelayPITCH_TYPE.PitchTempo
    SHIFT: float = 0
    NUMBER: int = 0
    CONSTRAIN: DelayCONSTRAIN = DelayCONSTRAIN.Yes


class EqXmlToTxtConverterFXNAME(Enum):
    Graphic = "Graphic"
    FilterCurve = "FilterCurve"


class EqXmlToTxtConverterOVERWRITE(Enum):
    Append = "Append"
    Overwrite = "Overwrite"
    Error = "Error"


@register_command
class EqXmlToTxtConverter(Command):
    "GNU General Public License v2.0 or later"
    FXNAME: EqXmlToTxtConverterFXNAME = EqXmlToTxtConverterFXNAME.Graphic
    INFILE: str = ""
    OVERWRITE: EqXmlToTxtConverterOVERWRITE = EqXmlToTxtConverterOVERWRITE.Append


class LabelSoundsMEASUREMENT(Enum):
    peak = "peak"
    avg = "avg"
    rms = "rms"


class LabelSoundsTYPE(Enum):
    before = "before"
    after = "after"
    around = "around"
    between = "between"


@register_command
class LabelSounds(Command):
    "GNU General Public License v2.0 or later"
    THRESHOLD: float = 0
    MEASUREMENT: LabelSoundsMEASUREMENT = LabelSoundsMEASUREMENT.peak
    SIL_DUR: float = 0
    SND_DUR: float = 0
    TYPE: LabelSoundsTYPE = LabelSoundsTYPE.before
    PRE_OFFSET: float = 0
    POST_OFFSET: float = 0
    TEXT: str = ""


class LimiterTYPE(Enum):
    SoftLimit = "SoftLimit"
    HardLimit = "HardLimit"
    SoftClip = "SoftClip"
    HardClip = "HardClip"


class LimiterMAKEUP(Enum):
    No = "No"
    Yes = "Yes"


@register_command
class Limiter(Command):
    "GNU General Public License v2.0 or later"
    TYPE: LimiterTYPE = LimiterTYPE.SoftLimit
    GAIN_L: float = 0
    GAIN_R: float = 0
    THRESH: float = 0
    HOLD: float = 0
    MAKEUP: LimiterMAKEUP = LimiterMAKEUP.No


@register_command
class MeasureRms(Command):
    "GNU General Public License v2.0 or later"


class NoiseGateMODE(Enum):
    Gate = "Gate"
    Analyze = "Analyze"


class NoiseGateSTEREO_LINK(Enum):
    LinkStereo = "LinkStereo"
    DoNotLink = "DoNotLink"


@register_command
class NoiseGate(Command):
    "GNU General Public License v2.0 or later"
    MODE: NoiseGateMODE = NoiseGateMODE.Gate
    STEREO_LINK: NoiseGateSTEREO_LINK = NoiseGateSTEREO_LINK.LinkStereo
    THRESHOLD: float = 0
    GATE_FREQ: float = 0
    LEVEL_REDUCTION: float = 0
    ATTACK: float = 0
    HOLD: float = 0
    DECAY: float = 0


class NyquistPluginInstallerOVERWRITE(Enum):
    Disallow = "Disallow"
    Allow = "Allow"


@register_command
class NyquistPluginInstaller(Command):
    "GNU General Public License v2.0 or later"
    FILES: str = ""
    OVERWRITE: NyquistPluginInstallerOVERWRITE = NyquistPluginInstallerOVERWRITE.Disallow


class RegularIntervalLabelsMODE(Enum):
    Both = "Both"
    Number = "Number"
    Interval = "Interval"


class RegularIntervalLabelsADJUST(Enum):
    No = "No"
    Yes = "Yes"


class RegularIntervalLabelsZEROS(Enum):
    TextOnly = "TextOnly"
    OneBefore = "OneBefore"
    TwoBefore = "TwoBefore"
    ThreeBefore = "ThreeBefore"
    OneAfter = "OneAfter"
    TwoAfter = "TwoAfter"
    ThreeAfter = "ThreeAfter"


class RegularIntervalLabelsVERBOSE(Enum):
    Details = "Details"
    Warnings = "Warnings"
    None_ = "None"


@register_command
class RegularIntervalLabels(Command):
    "GNU General Public License v2.0 or later"
    MODE: RegularIntervalLabelsMODE = RegularIntervalLabelsMODE.Both
    TOTALNUM: int = 0
    INTERVAL: float = 0
    REGION: float = 0
    ADJUST: RegularIntervalLabelsADJUST = RegularIntervalLabelsADJUST.No
    LABELTEXT: str = ""
    ZEROS: RegularIntervalLabelsZEROS = RegularIntervalLabelsZEROS.TextOnly
    FIRSTNUM: int = 0
    VERBOSE: RegularIntervalLabelsVERBOSE = RegularIntervalLabelsVERBOSE.Details


class SampleDataExportUNITS(Enum):
    dB = "dB"
    Linear = "Linear"


class SampleDataExportFILEFORMAT(Enum):
    None_ = "None"
    Count = "Count"
    Time = "Time"


class SampleDataExportHEADER(Enum):
    None_ = "None"
    Minimal = "Minimal"
    Standard = "Standard"
    All = "All"


class SampleDataExportCHANNEL_LAYOUT(Enum):
    SameLine = "SameLine"
    Alternate = "Alternate"
    LFirst = "LFirst"


class SampleDataExportMESSAGES(Enum):
    Yes = "Yes"
    Errors = "Errors"
    None_ = "None"


@register_command
class SampleDataExport(Command):
    "GNU General Public License v2.0 or later"
    NUMBER: int = 0
    UNITS: SampleDataExportUNITS = SampleDataExportUNITS.dB
    FILENAME: str = ""
    FILEFORMAT: SampleDataExportFILEFORMAT = SampleDataExportFILEFORMAT.None_
    HEADER: SampleDataExportHEADER = SampleDataExportHEADER.None_
    OPTEXT: str = ""
    CHANNEL_LAYOUT: SampleDataExportCHANNEL_LAYOUT = SampleDataExportCHANNEL_LAYOUT.SameLine
    MESSAGES: SampleDataExportMESSAGES = SampleDataExportMESSAGES.Yes


class SampleDataImportBAD_DATA(Enum):
    ThrowError = "ThrowError"
    ReadAsZero = "ReadAsZero"


@register_command
class SampleDataImport(Command):
    "GNU General Public License v2.0 or later"
    FILENAME: str = ""
    BAD_DATA: SampleDataImportBAD_DATA = SampleDataImportBAD_DATA.ThrowError


class ShelfFilterTYPE(Enum):
    Low = "Low"
    High = "High"


@register_command
class ShelfFilter(Command):
    "GNU General Public License v2.0"
    TYPE: ShelfFilterTYPE = ShelfFilterTYPE.Low
    HZ: int = 0
    GAIN: int = 0


@register_command
class SpectralDelete(Command):
    "GNU General Public License v2.0 or later"


@register_command
class StudioFadeOut(Command):
    "GNU General Public License v2.0 or later"


class TremoloWAVE(Enum):
    Sine = "Sine"
    Triangle = "Triangle"
    Sawtooth = "Sawtooth"
    InverseSawtooth = "InverseSawtooth"
    Square = "Square"


@register_command
class Tremolo(Command):
    "GNU General Public License v2.0 or later"
    WAVE: TremoloWAVE = TremoloWAVE.Sine
    PHASE: int = 0
    WET: int = 0
    LFO: float = 0


@register_command
class RissetDrum(Command):
    "GNU General Public License v2.0 or later"
    FREQ: float = 0
    DECAY: float = 0
    CF: float = 0
    BW: float = 0
    NOISE: float = 0
    GAIN: float = 0


@register_command
class ClearLog(Command):
    "Clears the log contents."


@register_command
class Comment(Command):
    "For comments in a macro."
    _: str = ""


@register_command
class CompareAudio(Command):
    "Compares a range on two tracks."
    Threshold: float = 0


class DragRelativeTo(Enum):
    Panel = "Panel"
    App = "App"
    Track0 = "Track0"
    Track1 = "Track1"


@register_command
class Drag(Command):
    "Drags mouse from one place to another."
    Id: int | None = None
    Window: str | None = None
    FromX: float | None = None
    FromY: float | None = None
    ToX: float | None = None
    ToY: float | None = None
    RelativeTo: DragRelativeTo | None = None


@register_command
class Export2(Command):
    "Exports to a file."
    Filename: str = "/Users/austin/exported.wav"
    NumChannels: int = 1


class GetInfoType(Enum):
    Commands = "Commands"
    Menus = "Menus"
    Preferences = "Preferences"
    Tracks = "Tracks"
    Clips = "Clips"
    Envelopes = "Envelopes"
    Labels = "Labels"
    Boxes = "Boxes"


class GetInfoFormat(Enum):
    JSON = "JSON"
    LISP = "LISP"
    Brief = "Brief"


@register_command
class GetInfo(Command):
    "Gets information in JSON format."
    Type: GetInfoType = GetInfoType.Commands
    Format: GetInfoFormat = GetInfoFormat.JSON


@register_command
class GetPreference(Command):
    "Gets the value of a single preference."
    Name: str = ""


class HelpFormat(Enum):
    JSON = "JSON"
    LISP = "LISP"
    Brief = "Brief"


@register_command
class Help(Command):
    "Gives help on a command."
    Command: str = "Help"
    Format: HelpFormat = HelpFormat.JSON


@register_command
class Import2(Command):
    "Imports from a file."
    Filename: str = ""


@register_command
class Message(Command):
    "Echos a message."
    Text: str = "Some message"


@register_command
class OpenProject2(Command):
    "Opens a project."
    Filename: str = "test.aup3"
    AddToHistory: Bool | None = None


@register_command
class SaveCopy(Command):
    "Saves a copy of current project."
    Filename: str = "name.aup3"


@register_command
class SaveLog(Command):
    "Saves the log contents."
    Filename: str = "log.txt"


@register_command
class SaveProject2(Command):
    "Saves a project."
    Filename: str = "name.aup3"
    AddToHistory: Bool = False


class ScreenshotCaptureWhat(Enum):
    Window = "Window"
    FullWindow = "FullWindow"
    WindowPlus = "WindowPlus"
    Fullscreen = "Fullscreen"
    Toolbars = "Toolbars"
    Effects = "Effects"
    Scriptables = "Scriptables"
    Preferences = "Preferences"
    Trackpanel = "Trackpanel"
    Ruler = "Ruler"
    Tracks = "Tracks"
    FirstTrack = "FirstTrack"
    FirstTwoTracks = "FirstTwoTracks"
    FirstThreeTracks = "FirstThreeTracks"
    FirstFourTracks = "FirstFourTracks"
    SecondTrack = "SecondTrack"
    TracksPlus = "TracksPlus"
    FirstTrackPlus = "FirstTrackPlus"
    AllTracks = "AllTracks"
    AllTracksPlus = "AllTracksPlus"
    Audio_Setup = "Audio Setup"
    CombinedMeter = "CombinedMeter"
    Control = "Control"
    CutCopyPaste = "CutCopyPaste"
    Device = "Device"
    Edit = "Edit"
    PlayMeter = "PlayMeter"
    RecordMeter = "RecordMeter"
    Scrub = "Scrub"
    Selection = "Selection"
    Share_Audio = "Share Audio"
    Snapping = "Snapping"
    SpectralSelection = "SpectralSelection"
    Time = "Time"
    TimeSignature = "TimeSignature"
    Tools = "Tools"
    Transcription = "Transcription"


class ScreenshotBackground(Enum):
    Blue = "Blue"
    White = "White"
    None_ = "None"


@register_command
class Screenshot(Command):
    "Takes screenshots."
    Path: str = ""
    CaptureWhat: ScreenshotCaptureWhat = ScreenshotCaptureWhat.Window
    Background: ScreenshotBackground = ScreenshotBackground.None_
    ToTop: Bool = True


@register_command
class SelectFrequencies(Command):
    "Selects a frequency range."
    High: float | None = None
    Low: float | None = None


class SelectTimeRelativeTo(Enum):
    ProjectStart = "ProjectStart"
    Project = "Project"
    ProjectEnd = "ProjectEnd"
    SelectionStart = "SelectionStart"
    Selection = "Selection"
    SelectionEnd = "SelectionEnd"


@register_command
class SelectTime(Command):
    "Selects a time range."
    Start: float | None = None
    End: float | None = None
    RelativeTo: SelectTimeRelativeTo | None = None


class SelectTracksMode(Enum):
    Set = "Set"
    Add = "Add"
    Remove = "Remove"


@register_command
class SelectTracks(Command):
    "Selects a range of tracks."
    Track: float | None = None
    TrackCount: float | None = None
    Mode: SelectTracksMode | None = None


class SelectRelativeTo(Enum):
    ProjectStart = "ProjectStart"
    Project = "Project"
    ProjectEnd = "ProjectEnd"
    SelectionStart = "SelectionStart"
    Selection = "Selection"
    SelectionEnd = "SelectionEnd"


class SelectMode(Enum):
    Set = "Set"
    Add = "Add"
    Remove = "Remove"


@register_command
class Select(Command):
    "Selects Audio."
    Start: float | None = None
    End: float | None = None
    RelativeTo: SelectRelativeTo | None = None
    High: float | None = None
    Low: float | None = None
    Track: float | None = None
    TrackCount: float | None = None
    Mode: SelectMode | None = None


class SetClipColor(Enum):
    Color0 = "Color0"
    Color1 = "Color1"
    Color2 = "Color2"
    Color3 = "Color3"


@register_command
class SetClip(Command):
    "Sets various values for a clip."
    At: float | None = None
    Color: SetClipColor | None = None
    Start: float | None = None


@register_command
class SetEnvelope(Command):
    "Sets an envelope point position."
    Time: float | None = None
    Value: float | None = None
    Delete: Bool | None = None


@register_command
class SetLabel(Command):
    "Sets various values for a label."
    Label: int = 0
    Text: str | None = None
    Start: float | None = None
    End: float | None = None
    Selected: Bool | None = None


@register_command
class SetPreference(Command):
    "Sets the value of a single preference."
    Name: str = ""
    Value: str = ""
    Reload: Bool = False


@register_command
class SetProject(Command):
    "Sets various values for a project."
    Name: str | None = None
    Rate: float | None = None
    X: int | None = None
    Y: int | None = None
    Width: int | None = None
    Height: int | None = None


@register_command
class SetTrackAudio(Command):
    "Sets various values for a track."
    Mute: Bool | None = None
    Solo: Bool | None = None
    Gain: float | None = None
    Pan: float | None = None


@register_command
class SetTrackStatus(Command):
    "Sets various values for a track."
    Name: str | None = None
    Selected: Bool | None = None
    Focused: Bool | None = None


class SetTrackVisualsDisplay(Enum):
    Waveform = "Waveform"
    Spectrogram = "Spectrogram"
    Multiview = "Multiview"


class SetTrackVisualsScale(Enum):
    Linear = "Linear"
    dB = "dB"
    LinearDB = "LinearDB"


class SetTrackVisualsColor(Enum):
    Color0 = "Color0"
    Color1 = "Color1"
    Color2 = "Color2"
    Color3 = "Color3"


class SetTrackVisualsVZoom(Enum):
    Reset = "Reset"
    Times2 = "Times2"
    HalfWave = "HalfWave"


class SetTrackVisualsSpecColor(Enum):
    SpecColorNew = "SpecColorNew"
    SpecColorTheme = "SpecColorTheme"
    SpecGrayscale = "SpecGrayscale"
    SpecInvGrayscale = "SpecInvGrayscale"


@register_command
class SetTrackVisuals(Command):
    "Sets various values for a track."
    Height: int | None = None
    Display: SetTrackVisualsDisplay | None = None
    Scale: SetTrackVisualsScale | None = None
    Color: SetTrackVisualsColor | None = None
    VZoom: SetTrackVisualsVZoom | None = None
    VZoomHigh: float | None = None
    VZoomLow: float | None = None
    SpecPrefs: Bool | None = None
    SpectralSel: Bool | None = None
    SpecColor: SetTrackVisualsSpecColor | None = None


class SetTrackDisplay(Enum):
    Waveform = "Waveform"
    Spectrogram = "Spectrogram"
    Multiview = "Multiview"


class SetTrackScale(Enum):
    Linear = "Linear"
    dB = "dB"
    LinearDB = "LinearDB"


class SetTrackColor(Enum):
    Color0 = "Color0"
    Color1 = "Color1"
    Color2 = "Color2"
    Color3 = "Color3"


class SetTrackVZoom(Enum):
    Reset = "Reset"
    Times2 = "Times2"
    HalfWave = "HalfWave"


class SetTrackSpecColor(Enum):
    SpecColorNew = "SpecColorNew"
    SpecColorTheme = "SpecColorTheme"
    SpecGrayscale = "SpecGrayscale"
    SpecInvGrayscale = "SpecInvGrayscale"


@register_command
class SetTrack(Command):
    "Sets various values for a track."
    Name: str | None = None
    Selected: Bool | None = None
    Focused: Bool | None = None
    Mute: Bool | None = None
    Solo: Bool | None = None
    Gain: float | None = None
    Pan: float | None = None
    Height: int | None = None
    Display: SetTrackDisplay | None = None
    Scale: SetTrackScale | None = None
    Color: SetTrackColor | None = None
    VZoom: SetTrackVZoom | None = None
    VZoomHigh: float | None = None
    VZoomLow: float | None = None
    SpecPrefs: Bool | None = None
    SpectralSel: Bool | None = None
    SpecColor: SetTrackSpecColor | None = None
