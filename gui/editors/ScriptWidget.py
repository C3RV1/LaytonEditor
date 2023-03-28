from ..ui.ScriptWidget import ScriptWidgetUI

from formats.gds import GDS

from gui.editors.command_editor.CommandListEditor import CommandListEditor
from gui.editors.command_editor.commands import get_event_command_widget
from gui.editors.command_editor.command_parsers import script_cmd_parsers, script_cmd_context_menu

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..MainEditor import MainEditor


class ScriptEditor(ScriptWidgetUI):
    script_editor: CommandListEditor

    def __init__(self, main_editor):
        super(ScriptEditor, self).__init__()
        self.main_editor: MainEditor = main_editor
        self.gds: GDS = None

    def get_command_editor_widget(self):
        return CommandListEditor(get_event_command_widget, script_cmd_parsers, script_cmd_context_menu)

    def set_script(self, gds: GDS):
        self.gds = gds
        self.script_editor.set_gds_and_data(gds, rom=self.main_editor.rom)
        self.script_editor.clear_selection()

    def save_btn_click(self):
        self.script_editor.save()
        self.gds.save()
