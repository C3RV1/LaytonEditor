import re

from PySide6 import QtCore
from ..EditorTypes import EditorCategory, EditorObject
from formats.filesystem import Folder
from formats.puzzle import Puzzle
from formats import conf


class PuzzleNode(EditorObject):
    def __init__(self, category, internal_id):
        self.category = category
        self.internal_id = internal_id

    def name_str(self):
        return f"Puzzle {self.internal_id}"

    def data(self):
        return f"Puzzle {self.internal_id}"

    def get_puzzle(self) -> Puzzle:
        pz = Puzzle(self.category.rom, self.internal_id)
        pz.load_from_rom()
        return pz


class PuzzleCategory(EditorCategory):
    def __init__(self):
        super(PuzzleCategory, self).__init__()
        self.name = "Puzzles"
        self._puzzle_nodes = {}

    def reset_file_system(self):
        self._puzzle_nodes = {}

    @property
    def puzzle_nodes(self):
        if len(self._puzzle_nodes) == 0:
            self.generate_puzzle_nodes()
        return self._puzzle_nodes

    def generate_puzzle_nodes(self):
        puzzle_folder: Folder = self.rom.filenames[f"/data_lt2/nazo/{self.rom.lang}"]
        for filename in puzzle_folder.files:
            filename: str
            if not re.match("nazo[1-3].plz", filename):
                continue
            archive = self.rom.get_archive(f"/data_lt2/nazo/{self.rom.lang}/{filename}")
            for filename_ in archive.filenames:
                if match := re.match("n([0-9]+).dat", filename_):
                    internal_id = int(match.group(1))
                    if internal_id not in self._puzzle_nodes:
                        self._puzzle_nodes[internal_id] = PuzzleNode(self, internal_id)

    def row_count(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel):
        if index.internalPointer() is not self:
            return 0
        return len(self.puzzle_nodes)

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel):
        if parent.internalPointer() is not self:
            return QtCore.QModelIndex()
        key = sorted(list(self.puzzle_nodes.keys()))[row]
        child = self.puzzle_nodes[key]
        return model.createIndex(row, column, child)

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QModelIndex,
               model: QtCore.QAbstractItemModel):
        if index.internalPointer() is self:
            return QtCore.QModelIndex()
        return category_index

    def data(self, index: QtCore.QModelIndex, role, model: QtCore.QAbstractItemModel):
        if index.isValid() and role == QtCore.Qt.DisplayRole and index .internalPointer() is not self:
            return index.internalPointer().data()
        return None
