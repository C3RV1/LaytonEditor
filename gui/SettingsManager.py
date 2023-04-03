import json
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
            self.advanced_mode = True if str(self.qt_setting.value("advancedMode", "False")) == "True" else False
            self.cid_to_name_json = str(self.qt_setting.value("cidToName", ""))
            if self.cid_to_name_json == "":
                self.character_id_to_name = self.original_character_names()
            else:
                cid_to_name: dict = json.loads(self.cid_to_name_json)
                self.character_id_to_name = {}
                for key, item in cid_to_name.items():
                    self.character_id_to_name[int(key)] = item
            SettingsManager.__inited = True

    @staticmethod
    def original_character_names():
        character_id_to_name = {}
        with open("data_permanent/character_names.json", "r") as character_names_f:
            data: dict = json.load(character_names_f)
            for key, value in data.items():
                character_id_to_name[int(key)] = value
        return character_id_to_name

    def save_character_names(self):
        self.qt_setting.setValue("cidToName", json.dumps(self.character_id_to_name))

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

    def toggle_advanced_mode(self, advanced_mode):
        # Don't set here as it won't affect whole program
        # Instead, require restart
        # self.advanced_mode = not self.advanced_mode
        self.qt_setting.setValue("advancedMode", str(advanced_mode))
