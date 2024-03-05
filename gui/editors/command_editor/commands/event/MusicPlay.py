from gui.ui.command_editor.commands.event.MusicPlay import MusicPlayUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class MusicPlay(CommandEditorEvent, MusicPlayUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(MusicPlay, self).set_command(command, event=event, **kwargs)
        if command.command == 0x8c:
            self.variation_checkbox.setChecked(True)
            self.fade_in_frames.setEnabled(False)
        else:
            self.variation_checkbox.setChecked(False)
            self.fade_in_frames.setEnabled(True)
            self.fade_in_frames.setValue(command.params[2])

        self.music_id.setValue(command.params[0])
        self.volume.setValue(command.params[1])

    def save(self):
        if self.variation_checkbox.isChecked():
            self.command.command = 0x8c
            self.command.params = [
                self.music_id.value(),
                self.volume.value(),
                2
            ]
        else:
            self.command.command = 0x62
            self.command.params = [
                self.music_id.value(),
                self.volume.value(),
                self.fade_in_frames.value()
            ]
        super().save()

    def variation_edit(self, state: int):
        state = QtCore.Qt.CheckState(state)
        if state == QtCore.Qt.CheckState.Checked:
            self.fade_in_frames.setEnabled(False)
        else:
            self.fade_in_frames.setEnabled(True)
