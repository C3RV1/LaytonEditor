from gui.ui.command_editor.commands.event.Fade import FadeUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class Fade(CommandEditorEvent, FadeUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(Fade, self).set_command(command, event=event, **kwargs)
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

    def save(self):
        fade_in = self.fade_type.currentData(QtCore.Qt.ItemDataRole.UserRole)
        fade_screens = self.fade_screens.currentData(QtCore.Qt.ItemDataRole.UserRole)
        if self.default_duration.isChecked():
            fade_duration = None
        else:
            fade_duration = self.fade_duration.value()

        if fade_in is True:  # [0x2, 0x32, 0x80, 0x81, 0x88]
            if fade_screens == 2:  # [0x2, 0x80]
                if fade_duration is None:  # [0x2]
                    self.command.command = 0x2
                else:  # [0x80]
                    self.command.command = 0x80
            elif fade_screens == 0:  # [0x32, 0x81]
                if fade_duration is None:
                    self.command.command = 0x32
                else:
                    self.command.command = 0x81
            elif fade_screens == 1:  # [0x88]
                self.command.command = 0x88
                if fade_duration is None:
                    fade_duration = 42
        else:  # [0x3, 0x33, 0x72, 0x7f, 0x87]
            if fade_screens == 2:  # [0x3, 0x72]
                if fade_duration is None:  # [0x3]
                    self.command.command = 0x3
                else:  # [0x72]
                    self.command.command = 0x72
            elif fade_screens == 0:  # [0x33, 0x7f]
                if fade_duration is None:
                    self.command.command = 0x33
                else:
                    self.command.command = 0x7f
            elif fade_screens == 1:  # [0x87]
                self.command.command = 0x87
                if fade_duration is None:
                    fade_duration = 42
        if self.command.command in [0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
            self.command.params = [fade_duration]
        else:
            self.command.params = []

    def default_duration_edit(self, state: int):
        state = QtCore.Qt.CheckState(state)
        if state == QtCore.Qt.CheckState.Checked:
            self.fade_duration.setEnabled(False)
        else:
            self.fade_duration.setEnabled(True)

