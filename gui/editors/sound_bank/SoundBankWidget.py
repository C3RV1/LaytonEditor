from gui.ui.sound_bank.SoundBankWidget import SoundBankWidgetUI
from formats.sound.swdl import SWDL
from .SampleEditWidget import SampleEditor
from .KeyGroupEditWidget import KeyGroupEditor
from .ProgramEditWidget import ProgramEditor
from PySide6 import QtCore


class SampleListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(SampleListModel, self).__init__()
        self.swdl: [SWDL] = None

    def set_swdl(self, swdl: SWDL):
        self.layoutAboutToBeChanged.emit()
        self.swdl = swdl
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self.swdl.samples)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return list(self.swdl.samples.values())[index.row()]
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        return f"Sample {list(self.swdl.samples.keys())[index.row()]}"


class ProgramListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(ProgramListModel, self).__init__()
        self.swdl: [SWDL] = None

    def set_swdl(self, swdl: SWDL):
        self.layoutAboutToBeChanged.emit()
        self.swdl = swdl
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self.swdl.programs)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return list(self.swdl.programs.values())[index.row()]
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        return f"Program {list(self.swdl.programs.keys())[index.row()]}"


class KeyGroupListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(KeyGroupListModel, self).__init__()
        self.swdl: [SWDL] = None

    def set_swdl(self, swdl: SWDL):
        self.layoutAboutToBeChanged.emit()
        self.swdl = swdl
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self.swdl.key_groups)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return list(self.swdl.key_groups.values())[index.row()]
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        return f"Key Group {list(self.swdl.key_groups.keys())[index.row()]}"


class SoundBankEditor(SoundBankWidgetUI):
    sample_edit: SampleEditor
    key_group_edit: KeyGroupEditor
    program_edit: ProgramEditor

    def __init__(self):
        super(SoundBankEditor, self).__init__()
        self.swdl: [SWDL] = None
        self.sample_model = SampleListModel()
        self.program_model = ProgramListModel()
        self.key_group_model = KeyGroupListModel()

    def set_swdl(self, swdl: SWDL):
        self.swdl = swdl

        self.sample_model.set_swdl(swdl)
        if not swdl.swd_header.is_sample_bank:
            self.program_model.set_swdl(swdl)
            self.key_group_model.set_swdl(swdl)

        self.sample_list.setModel(self.sample_model)
        if not swdl.swd_header.is_sample_bank:
            self.program_list.setModel(self.program_model)
            self.key_group_list.setModel(self.key_group_model)

        self.tab_widget.setTabEnabled(1, not swdl.swd_header.is_sample_bank)
        self.tab_widget.setTabEnabled(2, not swdl.swd_header.is_sample_bank)
        if swdl.swd_header.is_sample_bank:
            self.tab_widget.setCurrentIndex(0)

        self.sample_list.setCurrentIndex(QtCore.QModelIndex())
        self.key_group_list.setCurrentIndex(QtCore.QModelIndex())
        self.program_list.setCurrentIndex(QtCore.QModelIndex())

    def get_sample_edit_widget(self):
        return SampleEditor()

    def get_key_group_edit_widget(self):
        return KeyGroupEditor()

    def get_program_edit_widget(self):
        return ProgramEditor()

    def sample_list_selection(self, selected: QtCore.QModelIndex):
        if not selected.isValid():
            self.sample_edit.hide()
            return
        self.sample_edit.show()
        self.sample_edit.set_sample(selected.data(QtCore.Qt.ItemDataRole.UserRole))

    def key_group_list_selection(self, selected: QtCore.QModelIndex):
        if not selected.isValid():
            self.key_group_edit.hide()
            return
        self.key_group_edit.show()
        self.key_group_edit.set_key_group(selected.data(QtCore.Qt.ItemDataRole.UserRole))

    def program_list_selection(self, selected: QtCore.QModelIndex):
        if not selected.isValid():
            self.program_edit.hide()
            return
        self.program_edit.show()
        self.program_edit.set_program(selected.data(QtCore.Qt.ItemDataRole.UserRole))
