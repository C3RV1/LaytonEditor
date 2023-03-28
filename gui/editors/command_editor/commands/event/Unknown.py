from gui.ui.command_editor.commands.event.Unknown import UnknownUI
from ..CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from formats_parsed.dcc import DCCParser


class Unknown(CommandEditor, UnknownUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(Unknown, self).set_command(command, event)
        dcc_parser = DCCParser()
        dcc_parser.reset()
        dcc_parser["::calls"].append({
            "func": f"gds_{hex(command.command)[2:]}",
            "parameters": command.params.copy()
        })
        self.command_input.setText(dcc_parser.serialize())

    def save(self):
        dcc_parser = DCCParser()
        dcc_parser.parse(self.command_input.text())
        func = dcc_parser["::calls::0::func"]
        self.command.params = dcc_parser["::calls::0::parameters"]
        self.command.command = int(func[4:], 16)

