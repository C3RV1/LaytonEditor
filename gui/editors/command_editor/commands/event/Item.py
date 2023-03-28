from gui.ui.command_editor.commands.event.Item import ItemUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore


class Item(CommandEditorEvent, ItemUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(Item, self).set_command(command, event=event, **kwargs)
        if command.command == 0x77:
            self.mode.setCurrentIndex(0)
        else:
            self.mode.setCurrentIndex(1)

        self.item_id.setValue(command.params[0])

    def save(self):
        self.command.command = self.mode.currentData(QtCore.Qt.ItemDataRole.UserRole)
        self.command.params = [self.item_id.value()]
