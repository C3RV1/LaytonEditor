from typing import List

from PySide6 import QtWidgets, QtGui, QtCore
from formats.gds import GDS, GDSCommand
from gui.SettingsManager import SettingsManager


class CommandListModel(QtCore.QAbstractListModel):
    def __init__(self, command_parsers, on_command_move=None):
        super(CommandListModel, self).__init__()
        self._gds: GDS = None
        self.cmd_data: dict = {}
        self._command_parsers = {}
        for cmd_list, cmd_parser in command_parsers:
            for cmd in cmd_list:
                self._command_parsers[cmd] = cmd_parser
        self.on_command_move = on_command_move
        self.settings_manager = SettingsManager()

    def set_gds_and_data(self, gds, **kwargs):
        self.layoutAboutToBeChanged.emit()
        self._gds = gds
        self.cmd_data = kwargs
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self._gds.commands)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        command: GDSCommand = self._gds.commands[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.parse_command(command) + "\n"
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return command
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super().flags(index)
        if not index.isValid():
            return default_flags | QtCore.Qt.ItemFlag.ItemIsDropEnabled
        return default_flags | QtCore.Qt.ItemFlag.ItemIsDragEnabled

    def supportedDropActions(self) -> QtCore.Qt.DropAction:
        return QtCore.Qt.DropAction.MoveAction

    def mimeData(self, indexes: List[QtCore.QModelIndex]) -> QtCore.QMimeData:
        mime_data = super().mimeData(indexes)
        if not indexes:
            return mime_data
        index = indexes[0].row()
        mime_data.setText(str(index))
        return mime_data

    def dropMimeData(self, data: QtCore.QMimeData, action: QtCore.Qt.DropAction, row: int, column: int,
                     parent: QtCore.QModelIndex) -> bool:
        if row == -1:
            return False
        src_row = int(data.text())
        if src_row < row:
            row -= 1
        if src_row == row:
            return False
        self.layoutAboutToBeChanged.emit()
        command = self._gds.commands[src_row]
        self._gds.commands.pop(src_row)
        self._gds.commands.insert(row, command)
        self.layoutChanged.emit()
        if self.on_command_move is not None:
            print("Moved")
            self.on_command_move()
        return True

    def parse_command(self, command: GDSCommand):
        def parse_unknown(_command: GDSCommand, **_kwargs):
            return f"Command {hex(command.command)}\n" \
                   f"Parameters: {command.params}"
        cmd_parser = self._command_parsers.get(command.command, parse_unknown)
        return cmd_parser(command, **self.cmd_data)
