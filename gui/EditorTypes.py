from typing import List, Tuple, Callable, Any, TYPE_CHECKING, Union

from PySide6 import QtCore
from formats.filesystem import NintendoDSRom

if TYPE_CHECKING:
    from EditorTree import AbstractEditorTree


class EditorObject:
    category: 'AbstractEditorTree'

    def name_str(self):
        return type(self).__name__

    def category_str(self):
        return type(self.category).__name__


class EditorCategory(EditorObject):
    def __init__(self):
        self.name = ""
        self.category = self
        self.rom: NintendoDSRom = None

    def name_str(self):
        return f"Category {self.name}"

    def set_rom(self, rom):
        self.rom = rom
        self.reset_file_system()

    def reset_file_system(self):
        pass

    def row_count(self, index: QtCore.QModelIndex, model: 'AbstractEditorTree') -> int:
        return 0

    def column_count(self, _index: QtCore.QModelIndex, _model: 'AbstractEditorTree') -> int:
        return 1

    def index(self, row: int, column: int, parent: QtCore.QModelIndex,
              model: 'AbstractEditorTree') -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex, category_index: QtCore.QModelIndex,
               model: 'AbstractEditorTree') -> QtCore.QModelIndex:
        return QtCore.QModelIndex()

    def data(self, index: QtCore.QModelIndex, role, model: 'AbstractEditorTree'):
        return QtCore.QModelIndex()

    def decorative(self):
        return None

    def get_context_menu(self, index: QtCore.QModelIndex,
                         refresh_function: Callable) -> List[Union[Tuple[str, Callable], None]]:
        return []

    def flags(self, index: QtCore.QModelIndex, model: 'AbstractEditorTree') -> QtCore.Qt.ItemFlag:
        return QtCore.QAbstractItemModel.flags(model, index)

    def set_data(self, index: QtCore.QModelIndex, value: Any, role, model: 'AbstractEditorTree') -> bool:
        return False
