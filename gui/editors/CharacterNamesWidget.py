from gui.ui.CharacterNamesWidget import CharacterNamesWidgetUI
from PySide6 import QtCore, QtWidgets
from ..SettingsManager import SettingsManager
from formats.graphics.ani import AniSprite
from formats.filesystem import NintendoDSRom
import pygame as pg
import k4pg
from pg_utils.rom.loaders import FontLoaderROM
import numpy as np
from PIL import Image


class CharacterNamesEditor(CharacterNamesWidgetUI):
    def __init__(self, rom: NintendoDSRom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom: NintendoDSRom = rom

        self.setup_table(SettingsManager().character_id_to_name)

        self.setFixedSize(QtCore.QSize(600, 600))
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.setWindowTitle("Character ID to Name Table")
        self.show()

    def setup_table(self, names_dict):
        self.table_widget.clear()
        self.table_widget.setColumnCount(2)
        self.table_widget.setColumnWidth(1, 200)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Create Name Sprite"])
        self.table_widget.setRowCount(256)
        self.table_widget.setVerticalHeaderLabels([str(i) for i in range(256)])
        for char_id in range(256):
            table_widget_item = QtWidgets.QTableWidgetItem()
            table_widget_item.setData(QtCore.Qt.ItemDataRole.DisplayRole, names_dict.get(char_id, ""))
            self.table_widget.setItem(char_id, 0, table_widget_item)

            if char_id != 23:
                if self.rom is None:
                    create_btn = QtWidgets.QPushButton("Needs an open ROM")
                    create_btn.setEnabled(False)
                else:
                    create_btn = QtWidgets.QPushButton("Generate")
                create_btn.clicked.connect(
                    lambda *_args, l_char_id=char_id, button=create_btn: self.generate_name_sprite(l_char_id, button)
                )
                self.table_widget.setCellWidget(char_id, 1, create_btn)
            else:
                template_text = QtWidgets.QLabel("Used as template")
                self.table_widget.setCellWidget(char_id, 1, template_text)

    def generate_name_sprite(self, char_id, button: QtWidgets.QPushButton):
        if self.rom is None:
            return
        template_sprite = AniSprite(filename=f"/data_lt2/ani/eventchr/{self.rom.lang}/chr23_n.arc",
                                    rom=self.rom)

        name = self.table_widget.item(char_id, 0).data(QtCore.Qt.ItemDataRole.DisplayRole)

        # convert image to pygame surface
        array_surf = template_sprite.palette[template_sprite.images[0]][:, :, :-1]
        array_surf = np.swapaxes(array_surf, 0, 1)
        img_surf = pg.surfarray.make_surface(array_surf)
        img_surf.set_colorkey(pg.Color(0, 255, 0))

        font_supportive_dummy = k4pg.FontSupportive()
        font_loader = FontLoaderROM(self.rom, base_path_rom="/data_lt2/font")
        font_loader.load("fontq", 12, font_supportive_dummy)

        font = font_supportive_dummy.get_font()
        render_white, _ = font.render(name, pg.Color(255, 255, 255), None, antialiasing=True)
        render_black, _ = font.render(name, pg.Color(0, 0, 0), None, antialiasing=True)

        w, h = render_white.get_size()
        total_w, total_h = img_surf.get_size()

        pos_x, pos_y = (total_w - w) // 2, 12 - h
        # outline
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    continue
                img_surf.blit(render_black, (pos_x + x, pos_y + y))
        img_surf.blit(render_white, (pos_x, pos_y))

        img_string = pg.image.tobytes(img_surf, "RGBA")
        pil_image = Image.frombytes("RGBA", img_surf.get_size(), img_string)
        template_sprite.replace_image_pil(0, pil_image)
        template_sprite.save(filename=f"/data_lt2/ani/eventchr/{self.rom.lang}/chr{char_id}_n.arc",
                             rom=self.rom)
        button.setText("Done!")

    def save_clicked(self):
        name_dict = {}
        for char_id in range(256):
            name = self.table_widget.item(char_id, 0).data(QtCore.Qt.ItemDataRole.DisplayRole)
            if name == "":
                continue
            name_dict[char_id] = name
        SettingsManager().character_id_to_name = name_dict
        SettingsManager().save_character_names()

    def reset_clicked(self):
        self.setup_table(SettingsManager.original_character_names())
