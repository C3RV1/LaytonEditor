from gui.ui.event.command.FadeCommand import FadeCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event


class FadeCommand(CommandEditor, FadeCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        self.fade_type.setCurrentIndex(0 if command.command in [0x2, 0x32, 0x80, 0x81, 0x88] else 1)
        fade_screens = 0
        if command.command in [0x2, 0x3, 0x72, 0x80]:
            fade_screens = 2  # both screens
        elif command.command in [0x32, 0x33, 0x7f, 0x81]:
            fade_screens = 0  # btm screen
        elif command.command in [0x87, 0x88]:
            fade_screens = 1  # top screen
        self.fade_screens.setCurrentIndex(fade_screens)

        if command.command not in [0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
            self.default_duration.setChecked(True)
            self.fade_duration.setEnabled(False)
        else:
            self.default_duration.setChecked(False)
            self.fade_duration.setValue(command.params[0])
