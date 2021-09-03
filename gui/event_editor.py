from dataclasses import dataclass
from typing import Dict, List, Any

from gui import generated
from formats.event import Event
from formats.gds import GDSCommand
import wx
import wx.propgrid


@dataclass
class CommandRepr:
    command_name: str
    params: List[List]

    @staticmethod
    def from_gds(gds_command: GDSCommand, event: Event):
        name, params, param_names = event.convert_command(gds_command, for_code=False)
        param_dict = []
        for i in range(len(params)):
            param_dict.append([param_names[i] , type(params[i]).__name__, params[i]])
        if name == "Dialogue":
            param_dict[-1][1] = "long_str"
        command_repr = CommandRepr(name, param_dict)
        return command_repr

    def to_gds(self, event: Event):
        command = event.revert_command(self.command_name, [param[2] for param in self.params])
        return command


class CommandPanel(wx.Panel):
    def __init__(self, command_repr: CommandRepr, *args, **kwargs):
        super(CommandPanel, self).__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.command_repr = command_repr

        self.command_name_label = wx.StaticText(self, wx.ID_ANY, command_repr.command_name, wx.DefaultPosition,
                                                wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.command_name_label.SetSize((112, -1))
        self.command_name_label.Wrap(-1)

        self.move_up_btn = wx.Button(self, wx.ID_ANY, "Move Up", wx.DefaultPosition, wx.DefaultSize, 0)
        self.move_up_btn.SetSize((112, -1))
        self.move_down_btn = wx.Button(self, wx.ID_ANY, "Move Down", wx.DefaultPosition, wx.DefaultSize, 0)
        self.move_down_btn.SetSize((112, -1))
        self.delete_btn = wx.Button(self, wx.ID_ANY, "Delete", wx.DefaultPosition, wx.DefaultSize, 0)
        self.delete_btn.SetSize((112, -1))

        self.propertygrid = wx.propgrid.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                     wx.propgrid.PG_DEFAULT_STYLE | wx.propgrid.PG_HIDE_MARGIN |
                                                     wx.propgrid.PG_SPLITTER_AUTO_CENTER |
                                                     wx.propgrid.PG_STATIC_LAYOUT | wx.propgrid.PG_STATIC_SPLITTER)
        self.propertygrid.SetMaxSize((470, self.propertygrid.GetRowHeight() * len(command_repr.params) + 4))
        self.properties: List[wx.propgrid.PGProperty] = []
        for param in command_repr.params:
            p_label, p_type, p_value = param
            if p_type == "int":
                property_ = self.propertygrid.Append(wx.propgrid.IntProperty(p_label, p_label, p_value))
            elif p_type == "float":
                property_ = self.propertygrid.Append(wx.propgrid.FloatProperty(p_label, p_label, p_value))
            elif p_type == "str":
                property_ = self.propertygrid.Append(wx.propgrid.StringProperty(p_label, p_label, p_value))
            elif p_type == "long_str":
                property_ = self.propertygrid.Append(wx.propgrid.LongStringProperty(p_label, p_label, p_value))
            elif p_type == "bool":
                property_ = self.propertygrid.Append(wx.propgrid.BoolProperty(p_label, p_label, p_value))
            elif p_value is None:
                param[1] = "int"
                property_ = self.propertygrid.Append(wx.propgrid.IntProperty(p_label, p_label, -1))
            else:
                continue
            property_: wx.propgrid.PGProperty
            self.properties.append(property_)

        sizer2.Add(self.command_name_label, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.command_name_label.Layout()
        sizer2.Add(self.move_up_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.move_up_btn.Layout()
        sizer2.Add(self.move_down_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.move_down_btn.Layout()
        sizer2.Add(self.delete_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.delete_btn.Layout()
        sizer.Add(sizer2, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.propertygrid, 0, wx.ALL | wx.EXPAND, 5)
        self.propertygrid.Layout()
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.move_up_btn.Bind(wx.EVT_BUTTON, self.move_up)
        self.move_down_btn.Bind(wx.EVT_BUTTON, self.move_down)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.delete)

    def get_command_repr(self) -> CommandRepr:
        for i, property in enumerate(self.properties):
            self.command_repr.params[i][2] = property.GetValue()
        return self.command_repr

    def move_up(self, _):
        self.GetGrandParent().move_up(self)

    def move_down(self, _):
        self.GetGrandParent().move_down(self)

    def delete(self, _):
        self.GetGrandParent().delete(self)

class EventEditor(generated.EventEditor):
    def __init__(self, *args, **kwargs):
        super(EventEditor, self).__init__(*args, **kwargs)
        self.menu = wx.Menu()
        self.event: Event = None
        self.command_panels: List[CommandPanel] = []
        maineditor = self.GetGrandParent()

        def add_menu_item(menu, title, handler):
            ase_menu_item = wx.MenuItem(menu, wx.ID_ANY, title)
            menu.Append(ase_menu_item)
            maineditor.Bind(wx.EVT_MENU, handler, id=ase_menu_item.GetId())

        add_menu_item(self.menu, "Apply", self.apply_changes)
        add_menu_item(self.menu, "Save", self.save_changes)

    def add_command_panel(self, command_repr: CommandRepr):
        sizer: wx.Sizer = self.event_commands.GetSizer()
        command_panel = CommandPanel(command_repr, self.event_commands, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        sizer.Add(command_panel, 0, wx.ALL | wx.EXPAND, 5)
        command_panel.Layout()
        sizer.Layout()

    def set_event_info(self):
        self.m_mapTopID.SetValue(self.event.map_top_id)
        self.m_mapBtmID.SetValue(self.event.map_bottom_id)

        self.char_id0.SetValue(self.event.characters[0])
        self.char_id1.SetValue(self.event.characters[1])
        self.char_id2.SetValue(self.event.characters[2])
        self.char_id3.SetValue(self.event.characters[3])
        self.char_id4.SetValue(self.event.characters[4])
        self.char_id5.SetValue(self.event.characters[5])
        self.char_id6.SetValue(self.event.characters[6])
        self.char_id7.SetValue(self.event.characters[7])

        self.char_slot0.SetValue(self.event.characters_pos[0])
        self.char_slot1.SetValue(self.event.characters_pos[1])
        self.char_slot2.SetValue(self.event.characters_pos[2])
        self.char_slot3.SetValue(self.event.characters_pos[3])
        self.char_slot4.SetValue(self.event.characters_pos[4])
        self.char_slot5.SetValue(self.event.characters_pos[5])
        self.char_slot6.SetValue(self.event.characters_pos[6])
        self.char_slot7.SetValue(self.event.characters_pos[7])

        self.char_visible0.SetValue(self.event.characters_shown[0])
        self.char_visible1.SetValue(self.event.characters_shown[1])
        self.char_visible2.SetValue(self.event.characters_shown[2])
        self.char_visible3.SetValue(self.event.characters_shown[3])
        self.char_visible4.SetValue(self.event.characters_shown[4])
        self.char_visible5.SetValue(self.event.characters_shown[5])
        self.char_visible6.SetValue(self.event.characters_shown[6])
        self.char_visible7.SetValue(self.event.characters_shown[7])

        self.char_anim0.SetValue(self.event.characters_anim_index[0])
        self.char_anim1.SetValue(self.event.characters_anim_index[1])
        self.char_anim2.SetValue(self.event.characters_anim_index[2])
        self.char_anim3.SetValue(self.event.characters_anim_index[3])
        self.char_anim4.SetValue(self.event.characters_anim_index[4])
        self.char_anim5.SetValue(self.event.characters_anim_index[5])
        self.char_anim6.SetValue(self.event.characters_anim_index[6])
        self.char_anim7.SetValue(self.event.characters_anim_index[7])

    def load_event(self, event: Event):
        self.event = event
        self.set_event_info()
        self.command_panels.clear()

        sizer: wx.Sizer = self.event_commands.GetSizer()
        sizer.Clear(True)
        for i, command in enumerate(self.event.event_gds.commands):
            self.add_command_panel(CommandRepr.from_gds(command, self.event))
        self.event_commands.Layout()
        self.Layout()

    def apply_changes(self, _event):
        pass

    def save_changes(self, _event):
        pass

    def move_up(self, command_panel: CommandPanel):
        sizer: wx.Sizer = self.event_commands.GetSizer()
        for j, child in enumerate(sizer.GetChildren()):
            child: wx.SizerItem
            if child.GetWindow() == command_panel:
                sizer.Detach(command_panel)
                sizer.Insert(max(0, j - 1), command_panel, 0, wx.ALL | wx.EXPAND, 5)
                break
        command_panel.Layout()
        for child in sizer.GetChildren():
            child.GetWindow().Layout()
        self.event_commands.Layout()
        sizer.Layout()

    def move_down(self, command_panel):
        sizer: wx.Sizer = self.event_commands.GetSizer()
        for j, child in enumerate(sizer.GetChildren()):
            child: wx.SizerItem
            if child.GetWindow() == command_panel:
                sizer.Detach(command_panel)
                sizer.Insert(min(len(sizer.GetChildren()), j + 1), command_panel, 0, wx.ALL | wx.EXPAND, 5)
                break
        command_panel.Layout()
        for child in sizer.GetChildren():
            child.GetWindow().Layout()
        self.event_commands.Layout()
        sizer.Layout()

    def delete(self, command_panel):
        sizer: wx.Sizer = self.event_commands.GetSizer()
        for j, child in enumerate(sizer.GetChildren()):
            child: wx.SizerItem
            if child.GetWindow() == command_panel:
                sizer.Remove(j)
                command_panel.Destroy()
                break
        try:
            command_panel.Layout()
        except RuntimeError:
            # wrapped C/C++ object of type CommandPanel has been deleted
            pass
        self.event_commands.Layout()
        sizer.Layout()

    def enter(self):
        self.GetGrandParent().add_menu(self.menu, "Event")

    def exit(self):
        self.GetGrandParent().remove_menu("Event")
