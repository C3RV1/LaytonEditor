import re
from typing import Dict

from ..EditorTypes import EditorObject, EditorCategory
from formats.filesystem import Folder, Archive
from formats.place import Place
from PySide6 import QtCore


class PlaceVersion(EditorObject):
    def __init__(self, category, top, version, archive):
        self.category = category
        self.top = top
        self.version = version
        self.archive: Archive = archive

    def name_str(self):
        return f"Place {self.top} {self.version}"

    def data(self):
        return f"Version {self.version}"

    def get_place(self):
        return Place(filename=f"n_place{self.top}_{self.version}.dat", rom=self.archive)


class PlaceTop(EditorObject):
    def __init__(self, category, top):
        self.category = category
        self.top = top
        self.versions = []

    def name_str(self):
        return f"PlaceTop {self.top}"

    def add_version(self, version: PlaceVersion):
        self.versions.append(version)
        self.versions.sort(key=lambda x: x.version)

    def child_count(self):
        return len(self.versions)

    def child(self, row):
        if 0 > row or row >= self.child_count():
            return None
        return self.versions[row]

    def data(self):
        return f"Place {self.top}"


class PlaceCategory(EditorCategory):
    def __init__(self):
        super(PlaceCategory, self).__init__()
        self._place_nodes: Dict[int, PlaceTop] = {}
        self.name = "Places"

    def reset_file_system(self):
        self._place_nodes = {}

    @property
    def place_nodes(self):
        if len(self._place_nodes) == 0:
            self.generate_place_nodes()
        return self._place_nodes

    def generate_place_nodes(self):
        place_folder: Folder = self.rom.filenames["/data_lt2/place"]
        for filename in place_folder.files:
            filename: str
            if not re.match("plc_data[1-2].plz", filename):
                continue
            archive = self.rom.get_archive(f"/data_lt2/place/{filename}")
            for filename_ in archive.filenames:
                if match := re.match("n_place([0-9]+)_([0-9]+).dat", filename_):
                    top = int(match.group(1))
                    version = int(match.group(2))
                    if top not in self._place_nodes:
                        self._place_nodes[top] = PlaceTop(self, top)
                    version_obj = PlaceVersion(self, top, version, archive)
                    self._place_nodes[top].add_version(version_obj)

    def row_count(self, index: QtCore.QModelIndex, model) -> int:
        if index.internalPointer() is self:
            return len(list(self.place_nodes.keys()))
        node = index.internalPointer()
        if isinstance(node, PlaceTop):
            return node.child_count()
        return 0

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model) -> QtCore.QModelIndex:
        parent_node = parent.internalPointer()

        if isinstance(parent_node, PlaceVersion):
            return QtCore.QModelIndex

        if parent_node is self:
            keys = sorted(list(self.place_nodes.keys()))
            if 0 > row or row >= len(keys):
                return QtCore.QModelIndex()
            return model.createIndex(row, column, self.place_nodes[keys[row]])

        parent_node: PlaceTop
        child = parent_node.child(row)
        if child:
            return model.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QModelIndex,
               model) -> QtCore.QModelIndex:
        node = index.internalPointer()
        if node is self:
            return QtCore.QModelIndex()
        if isinstance(node, PlaceTop):
            return category_index

        node: PlaceVersion
        keys = sorted(list(self.place_nodes.keys()))
        row = keys.index(node.top)
        top = self.place_nodes[node.top]
        return model.createIndex(row, 0, top)

    def data(self, index: QtCore.QModelIndex, role, model: 'EditorTree'):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None
        node = index.internalPointer()
        return node.data()

