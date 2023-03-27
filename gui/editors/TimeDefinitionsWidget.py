from PySide6 import QtCore, QtWidgets, QtGui
from gui.ui.TimeDefinitionsWidget import TimeDefinitionsUI
from formats.dlz import TimeDefinitionsDlz


class TimeDefinitionsModel(QtCore.QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.time_def_dlz: TimeDefinitionsDlz = None

    def set_time_dlz(self, time_def_dlz: TimeDefinitionsDlz):
        self.layoutAboutToBeChanged.emit()
        self.time_def_dlz = time_def_dlz
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.time_def_dlz)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        key = self.time_def_dlz.index_key(index.row())
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return f"Time Definition {key}"
        elif role == QtCore.Qt.ItemDataRole.EditRole:
            return str(key)
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return key
        return None


class TimeDefinitionsEditor(TimeDefinitionsUI):
    def __init__(self):
        super().__init__()
        self.time_def_dlz: TimeDefinitionsDlz = None
        self.time_def_model = TimeDefinitionsModel()
        self.time_def_editing: int = None

    def set_time_dlz(self, time_def_dlz: TimeDefinitionsDlz):
        self.time_def_dlz = time_def_dlz
        self.time_def_model.set_time_dlz(time_def_dlz)
        self.time_def_list.setModel(self.time_def_model)

    def time_def_list_selection(self, selected: QtCore.QModelIndex):
        if selected.isValid():
            self.form_widget.show()
            self.time_def_editing: int = selected.data(QtCore.Qt.ItemDataRole.UserRole)
            self.time_def_spin.setValue(self.time_def_dlz[self.time_def_editing])
        else:
            self.form_widget.hide()
            self.time_def_editing = None

    def save_btn_click(self):
        self.time_def_dlz.save()

    def time_def_spin_edit(self, value: int):
        if self.time_def_editing is None:
            return
        self.time_def_dlz[self.time_def_editing] = value
