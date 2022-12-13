from ..ui.PlaceWidget import PlaceWidgetUI
from formats.place import Place
from PySide6 import QtCore

from previewers import PlacePreview

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..MainEditor import MainEditor


class PlaceAbstractTableModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(PlaceAbstractTableModel, self).__init__(*args, **kwargs)
        self.place: Place = None

    def set_place(self, place: Place):
        self.layoutAboutToBeChanged.emit()
        self.place = place
        self.layoutChanged.emit()


class PropertiesModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return 5
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 1

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return "Value"
        return [
            "Index",
            "Map X",
            "Map Y",
            "Background Image Index",
            "Map Image Index",
            "Background Music Index?"
        ][section]

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        return [
            self.place.index,
            self.place.map_x,
            self.place.map_y,
            self.place.background_image_index,
            self.place.map_image_index,
            self.place.background_music_index
        ][index.row()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(PropertiesModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        if index.row() == 0:
            self.place.index = value
        elif index.row() == 1:
            self.place.map_x = value
        elif index.row() == 2:
            self.place.map_y = value
        elif index.row() == 3:
            self.place.background_image_index = value
        elif index.row() == 4:
            self.place.map_image_index = value
        elif index.row() == 5:
            self.place.background_music_index = value
        return True


class HintcoinModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.hintcoins)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 4

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Index", "Unk"][section]
        return f"Hintcoin {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        hintcoin = self.place.hintcoins[index.row()]
        return [
            hintcoin.x,
            hintcoin.y,
            hintcoin.index,
            hintcoin.unk
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(HintcoinModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        hintcoin = self.place.hintcoins[index.row()]
        if index.column() == 0:
            hintcoin.x = value
        elif index.column() == 1:
            hintcoin.y = value
        elif index.column() == 2:
            hintcoin.index = value
        elif index.column() == 3:
            hintcoin.unk = value
        return True


class SpritesModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.sprites)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 3

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Filename"][section]
        return f"Sprite {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        spr = self.place.sprites[index.row()]
        return [
            spr.x,
            spr.y,
            spr.filename
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(SpritesModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        spr = self.place.sprites[index.row()]
        if index.column() == 0:
            spr.x = value
        elif index.column() == 1:
            spr.y = value
        elif index.column() == 2:
            spr.filename = value
        return True


class ObjectsModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.objects)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 7

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height", "Character Index", "Event Index", "Unk"][section]
        return f"Object {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        obj = self.place.objects[index.row()]
        return [
            obj.x,
            obj.y,
            obj.width,
            obj.height,
            obj.character_index,
            obj.event_index,
            obj.unk
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(ObjectsModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        obj = self.place.objects[index.row()]
        if index.column() == 0:
            obj.x = value
        elif index.column() == 1:
            obj.y = value
        elif index.column() == 2:
            obj.width = value
        elif index.column() == 3:
            obj.height = value
        elif index.column() == 4:
            obj.character_index = value
        elif index.column() == 5:
            obj.event_index = value
        elif index.column() == 6:
            obj.unk = value
        return True


class CommentsModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.comments)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 7

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height", "Character Index", "Text Index", "Unk"][section]
        return f"Comment {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        comment = self.place.comments[index.row()]
        return [
            comment.x,
            comment.y,
            comment.width,
            comment.height,
            comment.character_index,
            comment.text_index,
            comment.unk
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(CommentsModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        comment = self.place.comments[index.row()]
        if index.column() == 0:
            comment.x = value
        elif index.column() == 1:
            comment.y = value
        elif index.column() == 2:
            comment.width = value
        elif index.column() == 3:
            comment.height = value
        elif index.column() == 4:
            comment.character_index = value
        elif index.column() == 5:
            comment.text_index = value
        elif index.column() == 6:
            comment.unk = value
        return True


class ExitsModel(PlaceAbstractTableModel):
    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if not parent.isValid():
            return len(self.place.exits)
        return 0

    def columnCount(self, parent: QtCore.QModelIndex) -> int:
        return 11

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return ["X", "Y", "Width", "Height", "Image Index", "Action",
                    "Unk0", "Unk1", "Unk2", "Unk3", "Event or Place Index"][section]
        return f"Exit {section}"

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid() or (role != QtCore.Qt.ItemDataRole.DisplayRole and
                                   role != QtCore.Qt.ItemDataRole.EditRole):
            return None
        exit_ = self.place.exits[index.row()]
        return [
            exit_.x,
            exit_.y,
            exit_.width,
            exit_.height,
            exit_.image_index,
            exit_.action,
            exit_.unk0,
            exit_.unk1,
            exit_.unk2,
            exit_.unk3,
            exit_.event_or_place_index,
        ][index.column()]

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
        default_flags = super(ExitsModel, self).flags(index)
        if not index.isValid():
            return default_flags
        return default_flags | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index: QtCore.QModelIndex, value, role: int = ...) -> bool:
        if not index.isValid():
            return False
        exit_ = self.place.exits[index.row()]
        if index.column() == 0:
            exit_.x = value
        elif index.column() == 1:
            exit_.y = value
        elif index.column() == 2:
            exit_.width = value
        elif index.column() == 3:
            exit_.height = value
        elif index.column() == 4:
            exit_.image_index = value
        elif index.column() == 5:
            exit_.action = value
        elif index.column() == 6:
            exit_.unk0 = value
        elif index.column() == 7:
            exit_.unk1 = value
        elif index.column() == 8:
            exit_.unk2 = value
        elif index.column() == 9:
            exit_.unk3 = value
        elif index.column() == 10:
            exit_.event_or_place_index = value
        return True


class PlaceEditor(PlaceWidgetUI):
    def __init__(self, main_editor: 'MainEditor', *args, **kwargs):
        super(PlaceEditor, self).__init__(*args, **kwargs)
        self.place = None
        self.main_editor = main_editor
        self.place_views = [
            self.place_properties_tab,
            self.hintcoins_tab,
            self.sprites_tab,
            self.objects_tab,
            self.comments_tab,
            self.exits_tab
        ]
        self.place_models = [
            PropertiesModel(),
            HintcoinModel(),
            SpritesModel(),
            ObjectsModel(),
            CommentsModel(),
            ExitsModel()
        ]

    def set_place(self, place: Place):
        self.place = place
        for view, model in zip(self.place_views, self.place_models):
            model.set_place(place)
            view.setModel(model)

    def preview_click(self):
        self.main_editor.pg_previewer.start_renderer(PlacePreview(self.place))

    def save_click(self):
        self.main_editor.pg_previewer.start_renderer(PlacePreview(self.place))
        self.place.save()
