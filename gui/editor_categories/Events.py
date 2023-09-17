import re
from typing import List, Dict

from PySide6 import QtCore
from ..EditorTypes import EditorCategory, EditorObject
from formats.filesystem import Folder
from formats.event import Event
from formats.dlz_types.EventLch import EventLchDlz


class EventNode(EditorObject):
    def __init__(self, category, top, btm):
        self.category: EventCategory = category
        self.top, self.btm = top, btm

    def name_str(self):
        return f"Event {self.top} {self.btm}"

    def data(self):
        event_id = str(self.top * 1000 + self.btm)
        name = self.category.event_names.get(self.top * 1000 + self.btm, "NO NAME")
        return f"Event {event_id.zfill(5)} [{name}]"

    def get_event(self) -> Event:
        ev = Event(self.category.rom)
        ev.event_id = self.top * 1000 + self.btm
        ev.load_from_rom()
        return ev


class EventTopNode(EditorObject):
    def __init__(self, category, number):
        self.category = category
        self.num = number
        self.event_nodes = []

    def name_str(self):
        return f"EventTop {self.num}"

    def child_count(self):
        return len(self.event_nodes)

    def add_event_node(self, node: EventNode):
        self.event_nodes.append(node)

    def data(self):
        return f"Events {self.num}..."


class EventCategory(EditorCategory):
    def __init__(self):
        super(EventCategory, self).__init__()
        self.name = "Events"
        self._event_top_nodes: Dict[int, EventTopNode] = {}
        self.event_names: Dict[int, str] = {}

    def reset_file_system(self):
        self._event_top_nodes = {}

    @property
    def event_top_nodes(self):
        if len(self._event_top_nodes) == 0:
            self.generate_event_nodes()
        return self._event_top_nodes

    def generate_event_nodes(self):
        event_folder: Folder = self.rom.filenames["/data_lt2/event"]
        for filename in event_folder.files:
            filename: str
            if not re.match("ev_d[0-9abc]+.plz", filename):
                continue
            archive = self.rom.get_archive(f"/data_lt2/event/{filename}")
            for filename_ in archive.filenames:
                if match := re.match("e([0-9]+)_([0-9]+).gds", filename_):
                    top = int(match.group(1))
                    btm = int(match.group(2))
                    if top not in self._event_top_nodes:
                        self._event_top_nodes[top] = EventTopNode(self, top)
                    new_node = EventNode(self, top, btm)
                    self._event_top_nodes[top].add_event_node(new_node)
        self.load_event_names()

    def load_event_names(self):
        self.event_names = {}
        dlz_file = EventLchDlz(f"/data_lt2/rc/{self.rom.lang}/ev_lch.dlz", rom=self.rom)
        self.event_names = {v[0]: v[1].event_name for v in dlz_file.items()}

    def row_count(self, index: QtCore.QModelIndex, model: QtCore.QAbstractItemModel):
        if index.internalPointer() != self:
            node = index.internalPointer()
            if isinstance(node, EventTopNode):
                return node.child_count()
            return 0
        return len(self.event_top_nodes)

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: QtCore.QAbstractItemModel):
        if parent.internalPointer() != self:
            parent_node = parent.internalPointer()
            if not isinstance(parent_node, EventTopNode):
                return QtCore.QModelIndex()
            return model.createIndex(row, column, parent_node.event_nodes[row])

        key = list(self.event_top_nodes.keys())[row]
        child = self.event_top_nodes[key]
        return model.createIndex(row, column, child)

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QAbstractItemModel,
               model: QtCore.QAbstractItemModel):
        if index.internalPointer() == self:
            return QtCore.QModelIndex()
        if isinstance(index.internalPointer(), EventTopNode):
            return category_index
        top_id = index.internalPointer().top
        return model.createIndex(list(self._event_top_nodes.keys()).index(top_id),
                                 0, self._event_top_nodes[top_id])

    def data(self, index: QtCore.QModelIndex, role, model: QtCore.QAbstractItemModel):
        if index.isValid() and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return index.internalPointer().data()
        return None
