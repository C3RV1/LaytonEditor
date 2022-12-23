import os
from PySide6 import QtCore, QtGui, QtWidgets


class SettingsManager(object):
    __instance = None
    __inited = False

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not isinstance(SettingsManager.__instance, SettingsManager):
            SettingsManager.__instance = super(SettingsManager, cls).__new__(cls)
        return SettingsManager.__instance

    def __init__(self):
        if not SettingsManager.__inited:
            self.qt_setting = QtCore.QSettings("TeamTopHat", "LaytonEditor")
            self.rom_path = str(self.qt_setting.value("romPath", ""))
            self.export_path = str(self.qt_setting.value("exportPath", ""))
            self.import_path = str(self.qt_setting.value("importPath", ""))
            self.theme = str(self.qt_setting.value("theme", "dark"))
            SettingsManager.__inited = True

    def open_rom(self, parent: QtWidgets.QWidget) -> str:
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, "Open ROM", filter="NDS Rom (*.nds)",
                                                             dir=self.rom_path)
        if file_path != "":
            self.rom_path = os.path.dirname(file_path)
            self.qt_setting.setValue("romPath", self.rom_path)
        return file_path

    def save_rom(self, parent: QtWidgets.QWidget) -> str:
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(parent, "Save ROM", filter="NDS Rom (*.nds)",
                                                             dir=self.rom_path)
        if file_path != "":
            self.rom_path = os.path.dirname(file_path)
            self.qt_setting.setValue("romPath", self.rom_path)
        return file_path

    def import_file(self, parent: QtWidgets.QWidget, caption: str, ext_filter: str = "") -> str:
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, caption, filter=ext_filter,
                                                             dir=self.import_path)
        if file_path != "":
            self.import_path = os.path.dirname(file_path)
            self.qt_setting.setValue("importPath", self.import_path)
        return file_path

    def export_file(self, parent: QtWidgets.QWidget, caption: str, default_name: str, ext_filter: str = "") -> str:
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(parent, caption, filter=ext_filter,
                                                             dir=os.path.join(self.export_path, default_name))
        if file_path != "":
            self.export_path = os.path.dirname(file_path)
            self.qt_setting.setValue("exportPath", self.export_path)
        return file_path

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
        else:
            self.theme = "dark"
        self.qt_setting.setValue("theme", self.theme)
