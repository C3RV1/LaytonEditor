from PySide6 import QtCore, QtWidgets, QtGui
from gui.ui.SoundProfileWidget import SoundProfileUI
from formats.dlz import SoundProfile, SoundProfileDlz


class SoundProfileModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(SoundProfileModel, self).__init__()
        self.snd_dlz: SoundProfileDlz = None

    def set_snd_dlz(self, snd_dlz: SoundProfileDlz):
        self.layoutAboutToBeChanged.emit()
        self.snd_dlz = snd_dlz
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.snd_dlz)

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None
        key = self.snd_dlz.index_key(index.row())
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return f"Profile {key}"
        elif role == QtCore.Qt.ItemDataRole.EditRole:
            return str(key)
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return self.snd_dlz[key]
        return None


class SoundProfileEditor(SoundProfileUI):
    def __init__(self):
        super(SoundProfileEditor, self).__init__()
        self.snd_dlz: SoundProfileDlz = None
        self.sound_profile: SoundProfile = None
        self.sound_profile_model = SoundProfileModel()

    def sound_profiles_list_selection(self, selected: QtCore.QModelIndex):
        if selected.isValid():
            self.form_widget.show()
            self.sound_profile: SoundProfile = selected.data(QtCore.Qt.ItemDataRole.UserRole)
            self.music_id_spin.setValue(self.sound_profile.music_id)
            self.unk0_spin.setValue(self.sound_profile.unk0)
            self.unk1_spin.setValue(self.sound_profile.unk1)
        else:
            self.form_widget.hide()
            self.sound_profile = None

    def set_snd_profile(self, snd_dlz: SoundProfileDlz):
        self.snd_dlz = snd_dlz
        self.sound_profile_model.set_snd_dlz(snd_dlz)
        self.sound_profiles_list.setModel(self.sound_profile_model)

    def music_id_spin_edit(self, value: int):
        self.sound_profile.music_id = value

    def unk0_spin_edit(self, value: int):
        self.sound_profile.unk0 = value

    def unk1_spin_edit(self, value: int):
        self.sound_profile.unk1 = value

    def save_btn_click(self):
        self.snd_dlz.save()
