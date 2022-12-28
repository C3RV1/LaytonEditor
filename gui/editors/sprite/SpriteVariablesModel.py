from PySide6 import QtCore, QtWidgets, QtGui
from formats.graphics.ani import AniSprite, Animation


class VariablesModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(VariablesModel, self).__init__(*args, **kwargs)
        self.sprite: AniSprite = None

    def set_sprite(self, sprite: AniSprite):
        self.layoutAboutToBeChanged.emit()
        self.sprite = sprite
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return 9
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 9

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Vertical:
            return [
                "Child Image",
                f"Variable {section - 1}"
            ][min(section, 1)]
        return ["Variable Name", f"Value {section - 1}"][min(section, 1)]

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        if index.row() == 0:
            if index.column() == 0:
                return "child_image"
            elif index.column() == 1:
                return self.sprite.child_image
            return None
        if index.column() == 0:
            return self.sprite.variable_labels[index.row() - 1]
        return self.sprite.variable_data[index.row() - 1][index.column() - 1]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(VariablesModel, self).flags(index)
        if index.row() == 0:
            if index.column() == 1:
                default_flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        else:
            default_flags |= QtCore.Qt.ItemFlag.ItemIsEditable
        return default_flags

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if index.row() == 0:
            self.sprite.child_image = value
        elif index.column() == 0:
            self.sprite.variable_labels[index.row() - 1] = value
        else:
            self.sprite.variable_data[index.row() - 1][index.column() - 1] = value
        return True
