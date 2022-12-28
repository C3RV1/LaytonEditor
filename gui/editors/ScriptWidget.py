from ..ui.TextWidget import TextWidgetUI

from formats.gds import GDS
from formats_parsed.gds_parsers import EventGDSParser
from formats_parsed.dcc import DCCParser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..MainEditor import MainEditor


class ScriptEditor(TextWidgetUI):
    def __init__(self, main_editor):
        super(ScriptEditor, self).__init__()
        self.main_editor: MainEditor = main_editor
        self.gds: GDS = None
        self.dcc_parser = DCCParser()

    def set_script(self, gds: GDS):
        self.gds = gds
        self.dcc_parser.reset()
        EventGDSParser().serialize_into_dcc(gds, self.dcc_parser)
        self.text_editor.setPlainText(self.dcc_parser.serialize())

    def save_btn_click(self):
        self.dcc_parser.reset()
        self.dcc_parser.parse(self.text_editor.toPlainText())
        EventGDSParser().parse_from_dcc(self.gds, self.dcc_parser)
        self.gds.save()
