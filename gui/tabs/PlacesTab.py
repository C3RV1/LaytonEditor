import logging

from PySide6 import QtCore, QtWidgets

from formats.placeflag import PlaceFlag
from gui.EditorTypes import EditorObject
from gui.tabs.BaseTab import BaseTab
from gui.EditorTree import OneCategoryEditorTree
from gui.editor_categories import *
from gui.editors import *

from formats.filesystem import NintendoDSRom
from formats.dlz_types.ChapterInf import ChapterInfDlz, ChapterInfEntry
from formats.storyflag2 import StoryFlag2, StoryStepEntry
from previewers import PlacePreview


# TODO: Automatic event viewed flag management


class PlacesTab(BaseTab):
    def __init__(self, rom, pg_previewer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom: NintendoDSRom = rom

        self.pg_previewer = pg_previewer
        data_plz = self.rom.get_archive("/data_lt2/place/data.plz")
        self.story_flag2 = StoryFlag2(filename="storyflag2.dat", rom=data_plz)
        self.place_flag = PlaceFlag(filename="placeflag.dat", rom=data_plz)
        self.chp_inf = ChapterInfDlz(filename="/data_lt2/rc/chp_inf.dlz", rom=self.rom)

        self.place_category = PlaceCategory(self.place_flag)
        self.tree_model = OneCategoryEditorTree(self.place_category)
        self.tree_model.set_rom(self.rom)
        self.file_tree.setModel(self.tree_model)

        self.h_layout.removeWidget(self.file_tree)
        self.h_layout.removeWidget(self.empty_editor)

        self.v_layout = QtWidgets.QVBoxLayout()

        self.story_step_form = QtWidgets.QFormLayout()
        self.v_layout.addLayout(self.story_step_form, 1)

        self.story_step_combo = QtWidgets.QComboBox()
        self.story_step_form.addRow("Story Step", self.story_step_combo)

        self.include_default = QtWidgets.QCheckBox("Include versions 0")
        self.include_default.stateChanged.connect(self.include_defaults_change)

        self.story_step_chapter = QtWidgets.QSpinBox()
        self.story_step_chapter.setRange(10000, 40000)

        self.uses_second_chapter = QtWidgets.QCheckBox("Change Story So Far after watching it")

        self.story_step_chapter2 = QtWidgets.QSpinBox()
        self.story_step_chapter2.setRange(10000, 40000)
        self.story_step_chapter2.setEnabled(False)

        self.v_layout.addWidget(self.file_tree, 3)

        self.h_layout.addLayout(self.v_layout, 1)
        self.h_layout.addWidget(self.empty_editor, 3)

        self.populate_story_steps()

        self.place_editor = PlaceEditor(self)
        self.place_editor.hide()
        self.h_layout.addWidget(self.place_editor, 3)

        self.active_editor = self.empty_editor

        self.shown_story_step_info = False
        self.story_step_combo.currentIndexChanged.connect(self.story_step_combo_change)

    def populate_story_steps(self):
        self.story_step_combo.clear()
        self.story_step_combo.addItem("All", userData=None)

        for story_step in self.story_flag2:
            story_step: StoryStepEntry
            self.story_step_combo.addItem(
                str(story_step.step_id),
                userData=story_step
            )

        self.story_step_combo.setCurrentIndex(0)

    def story_step_combo_change(self, _index: int):
        self.update_filtering()

    def include_defaults_change(self, _state: int):
        self.update_filtering()

    def update_filtering(self):
        self.tree_model.layoutAboutToBeChanged.emit()

        data = self.story_step_combo.currentData(QtCore.Qt.ItemDataRole.UserRole)
        if data is None:
            self.place_category.filter_by_story_step(None, True)
            if self.shown_story_step_info:
                self.story_step_form.takeRow(self.include_default)
                self.story_step_form.takeRow(self.story_step_chapter)
                self.story_step_form.takeRow(self.uses_second_chapter)
                self.story_step_form.takeRow(self.story_step_chapter2)
                self.shown_story_step_info = False
        else:
            data: StoryStepEntry
            self.place_category.filter_by_story_step(data.step_id,
                                                     self.include_default.checkState() == QtCore.Qt.CheckState.Checked)
            if not self.shown_story_step_info:
                self.story_step_form.addWidget(self.include_default)
                self.story_step_form.addRow("The Story So Far", self.story_step_chapter)
                self.story_step_form.addWidget(self.uses_second_chapter)
                self.story_step_form.addRow("The Story So Far (2)", self.story_step_chapter2)
                self.shown_story_step_info = True
            chp_entry = self.chp_inf.get(data.step_id, None)
            if chp_entry is not None:
                chp_entry: ChapterInfEntry
                self.story_step_chapter.setValue(chp_entry.event_id)
                if chp_entry.event_viewed_flag != 0:
                    self.uses_second_chapter.setChecked(True)
                    self.story_step_chapter2.setEnabled(True)
                    self.story_step_chapter2.setValue(chp_entry.event_id_2)
                else:
                    self.uses_second_chapter.setChecked(False)
                    self.story_step_chapter2.setEnabled(False)
            else:
                logging.warning(f"ChapterInf for story step {data.step_id} not found.")

        self.tree_model.layoutChanged.emit()

    def tree_changed_selection(self, current: QtCore.QModelIndex, previous: QtCore.QModelIndex):
        node: EditorObject = current.internalPointer()
        if not node:
            return

        logging.info(f"Opening {node.name_str()}, category {node.category_str()}")

        self.active_editor.hide()
        self.active_editor = None

        set_previewer = False

        if isinstance(node, PlaceVersion):
            self.active_editor = self.place_editor
            place = node.get_place()
            self.place_editor.set_place(place)

            self.pg_previewer.start_renderer(PlacePreview(place))
            set_previewer = True

        if self.active_editor is None:
            self.active_editor = self.empty_editor

        if not set_previewer:
            self.pg_previewer.stop_renderer()

        self.active_editor.show()


