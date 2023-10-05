import re
from typing import Dict

from formats.placeflag import PlaceFlag, PlaceFlagVersion
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
    def __init__(self, category, top, place_flag: PlaceFlag):
        self.category = category
        self.top = top
        self.versions = []
        self.filtered = []
        self.place_flag = place_flag

    def update_filtered(self, story_step_filter, include_defaults):
        self.filtered = self.versions.copy()
        if story_step_filter is None:
            return
        for version in self.versions:
            version: PlaceVersion
            pf_place = self.place_flag[self.top]
            pf_version: PlaceFlagVersion = pf_place[version.version]
            if not pf_version.check_range(story_step_filter, include_defaults):
                self.filtered.remove(version)

    def name_str(self):
        return f"PlaceTop {self.top}"

    def add_version(self, version: PlaceVersion):
        self.versions.append(version)
        self.versions.sort(key=lambda x: x.version)

    def child_count(self):
        return len(self.filtered)

    def child(self, row):
        if 0 > row or row >= self.child_count():
            return None
        return self.filtered[row]

    def data(self):
        return f"Place {self.top}"


class PlaceCategory(EditorCategory):
    def __init__(self, place_flag: PlaceFlag):
        super(PlaceCategory, self).__init__()
        self._place_nodes: Dict[int, PlaceTop] = {}
        self._filtered_nodes: Dict[int, PlaceTop] = {}
        self.name = "Places"
        self.place_flag = place_flag

    def reset_file_system(self):
        self._place_nodes = {}

    @property
    def place_nodes(self):
        if len(self._place_nodes) == 0:
            self.generate_place_nodes()
        return self._filtered_nodes

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
                        self._place_nodes[top] = PlaceTop(self, top, self.place_flag)
                    version_obj = PlaceVersion(self, top, version, archive)
                    self._place_nodes[top].add_version(version_obj)

        self.filter_by_story_step(None, True)

    def filter_by_story_step(self, story_step, include_defaults):
        for place_node in self._place_nodes.values():
            place_node.update_filtered(story_step, include_defaults)
        self._filtered_nodes = {}
        for key, node in self._place_nodes.items():
            if node.child_count() > 0:
                self._filtered_nodes[key] = node

    def row_count(self, index: QtCore.QModelIndex, model) -> int:
        if not index.isValid() or index.internalPointer() is self:
            return len(list(self.place_nodes.keys()))
        node = index.internalPointer()
        if isinstance(node, PlaceTop):
            return node.child_count()
        return 0

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model) -> QtCore.QModelIndex:
        if parent.internalPointer() is self or not parent.isValid():
            keys = sorted(list(self.place_nodes.keys()))
            if 0 > row or row >= len(keys):
                return QtCore.QModelIndex()
            return model.createIndex(row, column, self.place_nodes[keys[row]])

        parent_node = parent.internalPointer()
        if isinstance(parent_node, PlaceVersion):
            return QtCore.QModelIndex

        parent_node: PlaceTop
        child = parent_node.child(row)
        if child:
            return model.createIndex(row, column, child)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QModelIndex,
               model) -> QtCore.QModelIndex:
        if index.internalPointer() is self or not index.isValid():
            return QtCore.QModelIndex()
        node = index.internalPointer()
        if isinstance(node, PlaceTop):
            return category_index

        node: PlaceVersion
        keys = sorted(list(self.place_nodes.keys()))
        if node.top not in keys:
            return QtCore.QModelIndex()
        row = keys.index(node.top)
        top = self.place_nodes[node.top]
        return model.createIndex(row, 0, top)

    def data(self, index: QtCore.QModelIndex, role, model: 'EditorTree'):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None
        node = index.internalPointer()
        return node.data()

