from .event.Fade import Fade
from .Unknown import Unknown
from .event.BackgroundLoad import BackgroundLoad
from .event.SetID import SetID
from .event.SetMode import SetMode
from .event.Wait import Wait
from .event.CharacterVisibility import CharacterVisibility
from .event.Dialogue import Dialogue
from .event.CharacterSlot import CharacterSlot
from .event.ShowChapter import ShowChapter
from .event.SetVoice import SetVoice
from .event.CharacterAnimation import CharacterAnimation
from .event.CharacterShake import CharacterShake
from .event.SFX import SFX
from .event.Companion import Companion
from .event.Mystery import Mystery
from .event.Item import Item
from .event.UnlockJournal import UnlockJournal
from .event.UnlockMinigame import UnlockMinigame
from .event.BackgroundTint import BackgroundTint
from .event.BackgroundShake import BackgroundShake
from .event.StartTea import StartTea
from .event.SaveProgress import SaveProgress
from .event.MusicFade import MusicFade
from .event.MusicPlay import MusicPlay

from formats.gds import GDSCommand
from PySide6 import QtWidgets
from .CommandEditor import CommandEditor


def get_event_command_widget(command: GDSCommand, **kwargs) -> [CommandEditor]:
    if command.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
        widget = Fade()
    elif command.command == 0x4:
        widget = Dialogue()
    elif command.command in [0x21, 0x22]:
        widget = BackgroundLoad()
    elif command.command in [0x5, 0x8, 0x9, 0xb]:
        widget = SetID()
    elif command.command in [0x6, 0x7]:
        widget = SetMode()
    elif command.command in [0x31, 0x69, 0x6c, 0x8e]:
        widget = Wait()
    elif command.command in [0x2a, 0x2b, 0x2c]:
        widget = CharacterVisibility()
    elif command.command == 0x2d:
        widget = ShowChapter()
    elif command.command == 0x30:
        widget = CharacterSlot()
    elif command.command == 0x37:
        widget = BackgroundTint()
    elif command.command == 0x3f:
        widget = CharacterAnimation()
    elif command.command == 0x5c:
        widget = SetVoice()
    elif command.command in [0x5d, 0x5e]:
        widget = SFX()
    elif command.command in [0x62, 0x8c]:
        widget = MusicPlay()
    elif command.command in [0x6a, 0x6b]:
        widget = BackgroundShake()
    elif command.command == 0x70:
        widget = UnlockJournal()
    elif command.command in [0x71, 0x7d]:
        widget = Mystery()
    elif command.command == 0x73:
        widget = StartTea()
    elif command.command in [0x77, 0x7a]:
        widget = Item()
    elif command.command == 0x7b:
        widget = SaveProgress()
    elif command.command == 0x79:
        widget = UnlockMinigame()
    elif command.command == 0x7e:
        widget = CharacterShake()
    elif command.command in [0x96, 0x97]:
        widget = Companion()
    elif command.command in [0x8a, 0x8b]:
        widget = MusicFade()
    elif command.command in [0x82, 0x89, 0xa1]:
        widget = QtWidgets.QWidget()
    else:
        widget = Unknown()
    if isinstance(widget, CommandEditor):
        widget.set_command(command, **kwargs)
    return widget
