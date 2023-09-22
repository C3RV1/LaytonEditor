from PySide6 import QtCore, QtWidgets, QtGui
from gui.ui.SoundFixWidget import SoundProfileUI
from formats.dlz_types.SoundFix import SoundFixEntry, SoundFixDlz
from ..SettingsManager import SettingsManager


class SoundFixModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(SoundFixModel, self).__init__()
        self.snd_dlz: SoundFixDlz = None

    def set_snd_dlz(self, snd_dlz: SoundFixDlz):
        self.layoutAboutToBeChanged.emit()
        self.snd_dlz = snd_dlz
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.snd_dlz)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        key = list(self.snd_dlz.keys())[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return f"Profile {key}"
        elif role == QtCore.Qt.ItemDataRole.EditRole:
            return str(key)
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return self.snd_dlz[key]
        return None


class SoundFixEditor(SoundProfileUI):
    def __init__(self):
        super(SoundFixEditor, self).__init__()
        self.snd_dlz: SoundFixDlz = None
        self.sound_fix_entry: SoundFixEntry = None
        self.sound_profile_model = SoundFixModel()
        if not SettingsManager().advanced_mode:
            self.form_layout.removeRow(self.unk0_spin)
            self.form_layout.removeRow(self.unk1_spin)

    def sound_profiles_list_selection(self, selected: QtCore.QModelIndex):
        if selected.isValid():
            self.form_widget.show()
            self.sound_fix_entry: SoundFixEntry = selected.data(QtCore.Qt.ItemDataRole.UserRole)
            self.music_id_spin.setValue(self.sound_fix_entry.music_id)
            if SettingsManager().advanced_mode:
                self.unk0_spin.setValue(self.sound_fix_entry.unk0)
                self.unk1_spin.setValue(self.sound_fix_entry.unk1)
        else:
            self.form_widget.hide()
            self.sound_fix_entry = None

    def set_snd_profile(self, snd_dlz: SoundFixDlz):
        self.snd_dlz = snd_dlz
        self.sound_profile_model.set_snd_dlz(snd_dlz)
        self.sound_profiles_list.setModel(self.sound_profile_model)

    def music_id_spin_edit(self, value: int):
        self.sound_fix_entry.music_id = value

    def unk0_spin_edit(self, value: int):
        self.sound_fix_entry.unk0 = value

    def unk1_spin_edit(self, value: int):
        self.sound_fix_entry.unk1 = value

    def save_btn_click(self):
        self.snd_dlz.save()
