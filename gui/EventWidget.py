import logging

from .ui.EventWidget import EventWidgetUI
from formats.event import Event
from formats_parsed.EventDCC import EventDCC
from formats_parsed.EventScript import EventScript

from previewers.event.EventPlayer import EventPlayer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MainEditor import MainEditor


class EventWidget(EventWidgetUI):
    def __init__(self, main_editor):
        super(EventWidget, self).__init__()
        self.event = None
        self.main_editor: MainEditor = main_editor

    def set_event(self, ev: Event):
        self.event = ev
        dcc_text = EventDCC(ev)
        serialized = dcc_text.serialize()
        self.text_editor.setPlainText(serialized)

    def preview_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = EventDCC(self.event).parse(text)
        if is_ok:
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def save_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = EventDCC(self.event).parse(text)
        if is_ok:
            self.event.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def preview_ev_script_btn_click(self):
        text = self.text_editor.toPlainText()
        try:
            ev_script = EventScript(text, self.event)
            ev_script.parse()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        except Exception as e:
            logging.error(f"Error compiling EventScript: {e}")

    def save_ev_script_btn_click(self):
        text = self.text_editor.toPlainText()
        try:
            ev_script = EventScript(text, self.event)
            ev_script.parse()
            self.event.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        except Exception as e:
            logging.error(f"Error compiling EventScript: {e}")
