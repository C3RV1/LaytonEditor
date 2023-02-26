from gui.ui.event.command.WaitCommand import WaitCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class WaitCommand(CommandEditor, WaitCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(WaitCommand, self).set_command(command, event)
        self.tap_checkbox.setChecked(command.command in [0x69, 0x6c])
        if command.command in [0x31, 0x6c]:
            self.frames_checkbox.setChecked(True)
            self.frame_value.setValue(self.command.params[0])
        else:
            self.frames_checkbox.setChecked(False)
            self.frame_value.setEnabled(False)

    def save(self):
        if self.tap_checkbox.isChecked():
            if self.frames_checkbox.isChecked():
                self.command.command = 0x6c
                self.command.params = [self.frame_value.value()]
                return
            self.command.command = 0x69
            self.command.params = []
            return
        self.command.command = 0x31
        self.command.params = [self.frame_value.value()]

    def tap_edit(self, state: int):
        state = QtCore.Qt.CheckState(state)
        if state == QtCore.Qt.CheckState.Unchecked:
            self.frames_checkbox.setChecked(True)
            self.frame_value.setEnabled(True)

    def frames_edit(self, state: int):
        state = QtCore.Qt.CheckState(state)
        if state == QtCore.Qt.CheckState.Unchecked:
            self.tap_checkbox.setChecked(True)
            self.frame_value.setEnabled(False)
        else:
            self.frame_value.setEnabled(True)
