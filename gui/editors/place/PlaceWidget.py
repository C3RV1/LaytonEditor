from gui.ui.PlaceWidget import PlaceWidgetUI
from formats.place import Place
from .PropertiesModel import PropertiesModel
from .HintcoinModel import HintcoinModel
from .SpritesModel import SpritesModel
from .ObjectsModel import ObjectsModel
from .CommentsModel import CommentsModel
from .ExitsModel import ExitsModel

from previewers import PlacePreview

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.MainEditor import MainEditor


# TODO: Hide all disabled items (all elements 0) and implement Add/Remove buttons


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
