from gui.tabs.BaseTab import BaseTab
from gui.EditorTree import OneCategoryEditorTree
from gui.editor_categories.Filesystem import FilesystemCategory


class FilesystemTab(BaseTab):
    def __init__(self, rom, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rom = rom

        self.tree_model = OneCategoryEditorTree(
            FilesystemCategory()
        )
        self.tree_model.set_rom(rom)
        self.file_tree.setModel(self.tree_model)

