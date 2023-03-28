import logging

from gui.ui.event.EventWidget import EventWidgetUI
from formats.event import Event
from gui.editors.command_editor.command_parsers import event_cmd_parsers, event_cmd_context_menu

from previewers.event.EventPlayer import EventPlayer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.MainEditor import MainEditor


from .EventPropertiesWidget import EventPropertiesWidget
from PySide6 import QtCore, QtWidgets
from gui.editor_categories.Events import EventCategory, EventNode
from gui.editors.command_editor.commands import get_event_command_widget
from gui.editors.command_editor.CommandListEditor import CommandListEditor


class EventEditor(EventWidgetUI):
    script_editor: CommandListEditor

    def __init__(self, main_editor):
        super(EventEditor, self).__init__()
        self.event = None
        self.event_node: QtCore.QModelIndex = None
        self.main_editor: MainEditor = main_editor

    def get_command_editor_widget(self):
        return CommandListEditor(get_event_command_widget, event_cmd_parsers, event_cmd_context_menu)

    def tab_changed(self, current: int):
        if current != 1:
            self.script_editor.clear_selection()

    def get_event_properties_widget(self):
        return EventPropertiesWidget(self)

    def set_event(self, ev: Event, ev_index: QtCore.QModelIndex):
        self.event = ev
        self.event_node = ev_index
        self.character_widget.set_event(ev)

        self.script_editor.set_gds_and_data(self.event.gds, event=self.event, rom=self.event.rom)
        self.script_editor.clear_selection()

    def preview_click(self):
        self.script_editor.save()
        self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))

    def save_click(self):
        self.script_editor.save()
        self.event.save_to_rom()
        self.reload_category_preview()
        self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))

    def reload_category_preview(self):
        event_node: EventNode = self.event_node.internalPointer()
        category: EventCategory = event_node.category
        category.load_event_names()
        self.main_editor.tree_model.dataChanged.emit(self.event_node, self.event_node)
