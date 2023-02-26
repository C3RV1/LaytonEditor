from .FadeCommand import FadeCommand
from .CommandEditor import CommandEditor
from PySide6 import QtWidgets
from formats.gds import GDSCommand
from formats.event import Event


def get_command_widget(command: GDSCommand, event: Event):
    widget = None
    if command.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
        widget = FadeCommand()
    else:
        widget = QtWidgets.QWidget()
    if isinstance(widget, CommandEditor):
        widget.set_command(command, event)
    return widget
