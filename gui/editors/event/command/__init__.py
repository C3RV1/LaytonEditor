from .FadeCommand import FadeCommand
from .UnknownCommand import UnknownCommand
from .CommandEditor import CommandEditor
from .LoadBGCommand import LoadBGCommand
from .SetIDCommand import SetIDCommand
from .SetModeCommand import SetModeCommand
from .WaitCommand import WaitCommand
from .CharacterVisibilityCommand import CharacterVisibilityCommand
from .DialogueCommand import DialogueCommand
from .CharacterSlotCommand import CharacterSlotCommand
from formats.gds import GDSCommand
from formats.event import Event


def get_command_widget(command: GDSCommand, event: Event) -> CommandEditor:
    if command.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
        widget = FadeCommand()
    elif command.command == 0x4:
        widget = DialogueCommand()
    elif command.command in [0x21, 0x22]:
        widget = LoadBGCommand()
    elif command.command in [0x5, 0x8, 0x9, 0xb]:
        widget = SetIDCommand()
    elif command.command in [0x6, 0x7]:
        widget = SetModeCommand()
    elif command.command in [0x31, 0x69, 0x6c]:
        widget = WaitCommand()
    elif command.command in [0x2a, 0x2b, 0x2c]:
        widget = CharacterVisibilityCommand()
    elif command.command == 0x30:
        widget = CharacterSlotCommand()
    else:
        widget = UnknownCommand()
    widget.set_command(command, event)
    return widget
