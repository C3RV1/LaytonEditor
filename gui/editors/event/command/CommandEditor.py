from formats.gds import GDSCommand
from formats.event import Event


class CommandEditor:
    def __init__(self):
        super(CommandEditor, self).__init__()
        self.command: GDSCommand = None
        self.event: Event = None

    def set_command(self, command: GDSCommand, event: Event):
        self.command = command
        self.event = event

    def save(self):
        pass
