from gui.ui.command_editor.commands.event.Wait import WaitUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class Wait(CommandEditorEvent, WaitUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(Wait, self).set_command(command, event=event, **kwargs)
        if command.command == 0x8e:
            self.time_definition.setChecked(True)
            self.time_definition_id.setEnabled(True)
            self.time_definition_id.setValue(command.params[0])
            self.tap_checkbox.setEnabled(False)
            self.tap_checkbox.setChecked(True)
            self.frame_value.setEnabled(False)
            self.frames_checkbox.setEnabled(False)
        else:
            self.time_definition.setChecked(False)
            self.time_definition_id.setEnabled(False)
            self.tap_checkbox.setEnabled(True)
            self.tap_checkbox.setChecked(command.command in [0x69, 0x6c])
            self.frames_checkbox.setEnabled(True)
            if command.command in [0x31, 0x6c]:
                self.frames_checkbox.setChecked(True)
                self.frame_value.setEnabled(True)
                self.frame_value.setValue(self.command.params[0])
            else:
                self.frames_checkbox.setChecked(False)
                self.frame_value.setEnabled(False)

    def save(self):
        if self.time_definition.isChecked():
            self.command.command = 0x8e
            self.command.params = [self.time_definition_id.value()]
            return
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
        super().save()

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

    def time_definition_edit(self, state: int):
        state = QtCore.Qt.CheckState(state)
        if state == QtCore.Qt.CheckState.Checked:
            self.tap_checkbox.setEnabled(False)
            self.frames_checkbox.setEnabled(False)
            self.frame_value.setEnabled(False)
            self.time_definition_id.setEnabled(True)
        else:
            self.time_definition_id.setEnabled(False)
            self.tap_checkbox.setEnabled(True)
            self.frames_checkbox.setEnabled(True)
            self.frame_value.setEnabled(True)

