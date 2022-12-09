from .ui.EventWidget import EventWidgetUI
from formats.event import Event
from formats_parsed.EventDCC import EventDCC


class EventWidget(EventWidgetUI):
    def __init__(self, main_editor):
        super(EventWidget, self).__init__()
        self.event = None
        self.main_editor = main_editor

    def set_event(self, ev: Event):
        self.event = ev
        dcc_text = EventDCC(ev)
        serialized = dcc_text.serialize()
        self.text_editor.setPlainText(serialized)
