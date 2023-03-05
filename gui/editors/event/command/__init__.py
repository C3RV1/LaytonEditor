from .Fade import Fade
from .Unknown import Unknown
from .CommandEditor import CommandEditor
from .BackgroundLoad import BackgroundLoad
from .SetID import SetID
from .SetMode import SetMode
from .Wait import Wait
from .CharacterVisibility import CharacterVisibility
from .Dialogue import Dialogue
from .CharacterSlot import CharacterSlot
from .ShowChapter import ShowChapter
from .SetVoice import SetVoice
from .CharacterAnimation import CharacterAnimation
from .CharacterShake import CharacterShake
from .SFX import SFX
from .Companion import Companion
from .Mystery import Mystery
from .Item import Item
from .UnlockJournal import UnlockJournal
from .UnlockMinigame import UnlockMinigame
from .BackgroundTint import BackgroundTint
from .BackgroundShake import BackgroundShake
from .StartTea import StartTea
from .SaveProgress import SaveProgress
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtWidgets


def get_command_widget(command: GDSCommand, event: Event) -> [CommandEditor]:
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
    elif command.command in [0x31, 0x69, 0x6c]:
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
    elif command.command in [0x82, 0x89, 0xa1]:
        widget = QtWidgets.QWidget()
    else:
        widget = Unknown()
    widget.set_command(command, event)
    return widget
