from typing import List, Tuple, Callable, Any, TYPE_CHECKING

from PySide6 import QtCore
from formats.filesystem import NintendoDSRom

if TYPE_CHECKING:
    from EditorTree import EditorTree


class EditorObject:
    category: 'EditorCategory'


class EditorCategory(EditorObject):
    def __init__(self):
        self.name = ""
        self.category = self
        self.rom: NintendoDSRom = None

    def set_rom(self, rom):
        self.rom = rom
        self.reset_file_system()

    def reset_file_system(self):
        pass

    def row_count(self, index: QtCore.QModelIndex, model: 'EditorTree') -> int:
        return 0

    def column_count(self, index: QtCore.QModelIndex, model: 'EditorTree') -> int:
        return 1

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: 'EditorTree') -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QAbstractItemModel,
               model: 'EditorTree') -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    def data(self, index: QtCore.QModelIndex, role, model: 'EditorTree'):
        return QtCore.QModelIndex()

    def get_context_menu(self, index: QtCore.QModelIndex) -> List[Tuple[str, Callable]]:
        return []

    def flags(self, index: QtCore.QModelIndex, model: 'EditorTree') -> QtCore.Qt.ItemFlag:
        return QtCore.QAbstractItemModel.flags(model, index)

    def set_data(self, index: QtCore.QModelIndex, value: Any, role, model: 'EditorTree') -> bool:
        return False
