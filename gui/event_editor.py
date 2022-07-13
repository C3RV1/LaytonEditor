from dataclasses import dataclass
from typing import List

from gui import generated
from formats.event import Event
from formats.gds import GDSCommand
from formats.parsers.gds_parsers import EventGDSParser
import wx
import wx.propgrid

from gui.PygamePreviewer import PygamePreviewer
from previewers.event.EventPlayer import EventPlayer


class ButtonNoTab(wx.Button):
    def AcceptsFocusFromKeyboard(self):
        return False


@dataclass
class CommandRepr:
    command_name: str
    params: List[List]

    @staticmethod
    def from_gds(gds_command: GDSCommand, event: Event):
        name, params, param_names = EventGDSParser(ev=event).parse_command_name(gds_command, is_code=False)
        param_dict = []
        for i in range(len(params)):
            param_dict.append([param_names[i], type(params[i]).__name__, params[i]])
            if param_dict[-1][1] == "int" and name != "Fade" and i != len(params) - 1:
                param_dict[-1][1] = "uint"
        if name == "Dialogue":
            param_dict[-1][1] = "long_str"
        command_repr = CommandRepr(name, param_dict)
        return command_repr

    def to_gds(self, event: Event):
        command = EventGDSParser(ev=event).reverse_command_name(self.command_name, [param[2] for param in self.params],
                                                                is_code=False)
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

        self.move_up_btn = ButtonNoTab(self, wx.ID_ANY, "Move Up", wx.DefaultPosition, wx.DefaultSize, 0)
        self.move_up_btn.SetSize((112, -1))
        self.move_down_btn = ButtonNoTab(self, wx.ID_ANY, "Move Down", wx.DefaultPosition, wx.DefaultSize, 0)
        self.move_down_btn.SetSize((112, -1))
        self.delete_btn = ButtonNoTab(self, wx.ID_ANY, "Delete", wx.DefaultPosition, wx.DefaultSize, 0)
        self.delete_btn.SetSize((112, -1))

        self.property_grid = wx.propgrid.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                      wx.propgrid.PG_DEFAULT_STYLE | wx.propgrid.PG_HIDE_MARGIN |
                                                      wx.propgrid.PG_SPLITTER_AUTO_CENTER |
                                                      wx.propgrid.PG_STATIC_LAYOUT | wx.propgrid.PG_STATIC_SPLITTER |
                                                      wx.TAB_TRAVERSAL)
        self.property_grid.SetMaxSize((470, self.property_grid.GetRowHeight() * len(command_repr.params) + 4))
        self.property_grid.Bind(wx.EVT_MOUSEWHEEL, self.scroll_pg)
        self.properties: List[wx.propgrid.PGProperty] = []
        for param in command_repr.params:
            p_label, p_type, p_value = param
            if p_type == "uint":
                property_ = self.property_grid.Append(wx.propgrid.UIntProperty(p_label, p_label, p_value))
            elif p_type == "int":
                property_ = self.property_grid.Append(wx.propgrid.IntProperty(p_label, p_label, p_value))
            elif p_type == "float":
                property_ = self.property_grid.Append(wx.propgrid.FloatProperty(p_label, p_label, p_value))
            elif p_type == "str":
                property_ = self.property_grid.Append(wx.propgrid.StringProperty(p_label, p_label, p_value))
            elif p_type == "long_str":
                property_ = self.property_grid.Append(wx.propgrid.LongStringProperty(p_label, p_label, p_value))
            elif p_type == "bool":
                property_ = self.property_grid.Append(wx.propgrid.BoolProperty(p_label, p_label, p_value))
            elif p_value is None:
                param[1] = "int"
                property_ = self.property_grid.Append(wx.propgrid.IntProperty(p_label, p_label, -1))
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
        sizer.Add(self.property_grid, 0, wx.ALL | wx.EXPAND, 5)
        self.property_grid.Layout()
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.move_up_btn.Bind(wx.EVT_BUTTON, self.move_up)
        self.move_down_btn.Bind(wx.EVT_BUTTON, self.move_down)
        self.delete_btn.Bind(wx.EVT_BUTTON, self.delete)
        self.property_grid.AddActionTrigger(wx.propgrid.PG_ACTION_NEXT_PROPERTY, wx.WXK_DOWN)
        self.property_grid.AddActionTrigger(wx.propgrid.PG_ACTION_PREV_PROPERTY, wx.WXK_UP)
        self.property_grid.Bind(wx.propgrid.EVT_PG_CHANGED, self.pg_changed)
        self.property_grid.DedicateKey(wx.WXK_DOWN)
        self.property_grid.DedicateKey(wx.WXK_UP)

    def get_command_repr(self) -> CommandRepr:
        for i, property_ in enumerate(self.properties):
            if self.command_repr.params[i][1] == "long_str":
                self.command_repr.params[i][2] = property_.GetValue().replace(r"\n", "\n").replace(r"\\", "\\")
                continue
            self.command_repr.params[i][2] = property_.GetValue()
        return self.command_repr

    def move_up(self, _):
        self.GetGrandParent().move_up(self)
        self.modified()

    def move_down(self, _):
        self.GetGrandParent().move_down(self)
        self.modified()

    def delete(self, _):
        self.GetGrandParent().delete(self)
        self.modified()

    def pg_changed(self, _event):
        self.modified()

    def scroll_pg(self, event):
        parent: wx.EvtHandler = self.GetParent().GetEventHandler()
        parent.ProcessEvent(event)
        event.Skip()

    def modified(self):
        pass


class EventEditor(generated.EventEditor):
    def __init__(self, *args, **kwargs):
        super(EventEditor, self).__init__(*args, **kwargs)
        self.menu = wx.Menu()
        self.event: [Event] = None
        self.previewer: PygamePreviewer = PygamePreviewer.INSTANCE
        self.command_panels: List[CommandPanel] = []
        self.modified = False
        main_editor = self.GetGrandParent()

        def add_menu_item(menu, title, handler):
            ase_menu_item = wx.MenuItem(menu, wx.ID_ANY, title)
            menu.Append(ase_menu_item)
            main_editor.Bind(wx.EVT_MENU, handler, id=ase_menu_item.GetId())

        add_menu_item(self.menu, "Preview", self.apply_changes)
        add_menu_item(self.menu, "Save", self.save_changes)

    def add_command_panel(self, command_repr: CommandRepr):
        sizer: wx.Sizer = self.event_commands.GetSizer()
        command_panel = CommandPanel(command_repr, self.event_commands, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.TAB_TRAVERSAL)
        sizer.Add(command_panel, 0, wx.ALL | wx.EXPAND, 5)
        command_panel.Layout()
        self.event_commands.Layout()
        sizer.Layout()
        self.Layout()

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

    def get_event_info(self):
        self.event.map_top_id = self.m_mapTopID.GetValue()
        self.event.map_bottom_id = self.m_mapBtmID.GetValue()

        self.event.characters[0] = self.char_id0.GetValue()
        self.event.characters[1] = self.char_id1.GetValue()
        self.event.characters[2] = self.char_id2.GetValue()
        self.event.characters[3] = self.char_id3.GetValue()
        self.event.characters[4] = self.char_id4.GetValue()
        self.event.characters[5] = self.char_id5.GetValue()
        self.event.characters[6] = self.char_id6.GetValue()
        self.event.characters[7] = self.char_id7.GetValue()

        self.event.characters_pos[0] = self.char_slot0.GetValue()
        self.event.characters_pos[1] = self.char_slot1.GetValue()
        self.event.characters_pos[2] = self.char_slot2.GetValue()
        self.event.characters_pos[3] = self.char_slot3.GetValue()
        self.event.characters_pos[4] = self.char_slot4.GetValue()
        self.event.characters_pos[5] = self.char_slot5.GetValue()
        self.event.characters_pos[6] = self.char_slot6.GetValue()
        self.event.characters_pos[7] = self.char_slot7.GetValue()

        self.event.characters_shown[0] = self.char_visible0.GetValue()
        self.event.characters_shown[1] = self.char_visible1.GetValue()
        self.event.characters_shown[2] = self.char_visible2.GetValue()
        self.event.characters_shown[3] = self.char_visible3.GetValue()
        self.event.characters_shown[4] = self.char_visible4.GetValue()
        self.event.characters_shown[5] = self.char_visible5.GetValue()
        self.event.characters_shown[6] = self.char_visible6.GetValue()
        self.event.characters_shown[7] = self.char_visible7.GetValue()

        self.event.characters_anim_index[0] = self.char_anim0.GetValue()
        self.event.characters_anim_index[1] = self.char_anim1.GetValue()
        self.event.characters_anim_index[2] = self.char_anim2.GetValue()
        self.event.characters_anim_index[3] = self.char_anim3.GetValue()
        self.event.characters_anim_index[4] = self.char_anim4.GetValue()
        self.event.characters_anim_index[5] = self.char_anim5.GetValue()
        self.event.characters_anim_index[6] = self.char_anim6.GetValue()
        self.event.characters_anim_index[7] = self.char_anim7.GetValue()

    def load_event(self, event: Event):
        self.event = event
        self.set_event_info()
        self.command_panels.clear()

        sizer: wx.Sizer = self.event_commands.GetSizer()
        sizer.Clear(True)
        for i, command in enumerate(self.event.gds.commands):
            self.add_command_panel(CommandRepr.from_gds(command, self.event))
        self.event_commands.Layout()
        self.Layout()
        self.modified = False

    def apply_changes(self, _):
        sizer: wx.Sizer = self.event_commands.GetSizer()
        self.get_event_info()
        self.event.texts = {}
        command_panels = [child.GetWindow() for child in sizer.GetChildren()]
        self.event.gds.commands.clear()
        for command_panel in command_panels:
            command_panel: CommandPanel
            command_repr = command_panel.get_command_repr()
            command = command_repr.to_gds(self.event)
            self.event.gds.commands.append(command)
        self.previewer.start_renderer(EventPlayer(self.event))

    def save_changes(self, _event):
        self.apply_changes(None)
        self.event.save_to_rom()
        self.modified = False

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

    def do_modify(self):
        self.modified = True

    def exit(self):
        self.GetGrandParent().remove_menu("Event")

    def close(self):
        if self.modified:
            dialog = wx.MessageDialog(self, "Save changes before exiting?", style=wx.YES_NO | wx.CANCEL)
            result = dialog.ShowModal()
            if result == wx.ID_YES:
                self.save_changes(None)
                self.exit()
                return True
            elif result == wx.ID_NO:
                self.exit()
                return True
            return False
        self.exit()
        return True

    def add_dialogue(self, _):
        self.add_command_panel(CommandRepr(
            "Dialogue",
            [["Text GDS Number", "uint", 0],
             ["Character ID", "uint", 0],
             ["Start Animation", "str", "NONE"],
             ["End Animation", "str", "NONE"],
             ["Sound Pitch?", "uint", 2],
             ["Text", "long_str", ""]]
        ))
        self.do_modify()

    def add_fade(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("fade"),
            [["Fade In", "bool", False],
             ["Fade Screen", "uint", 0],
             ["Fade Frames", "int", -1]]
        ))
        self.do_modify()

    def add_bg_load(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("bg_load"),
            [["Path", "str", ""],
             ["Screen", "uint", 0]]
        ))
        self.do_modify()

    def add_set_mode(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_mode"),
            [["Mode", "str", ""]]
        ))
        self.do_modify()

    def add_set_next_mode(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_next_mode"),
            [["Mode", "str", ""]]
        ))
        self.do_modify()

    def add_set_movie(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_movie"),
            [["Movie ID", "uint", 0]]
        ))
        self.do_modify()

    def add_set_event(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_event"),
            [["Event ID", "uint", 0]]
        ))
        self.do_modify()

    def add_set_puzzle(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_puzzle"),
            [["Puzzle ID", "uint", 0]]
        ))
        self.do_modify()

    def add_set_room(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_room"),
            [["Room ID", "uint", 0]]
        ))
        self.do_modify()

    def add_chr_show(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("chr_show"),
            [["Character Index", "uint", 0]]
        ))
        self.do_modify()

    def add_chr_hide(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("chr_hide"),
            [["Character Index", "uint", 0]]
        ))
        self.do_modify()

    def add_chr_visibility(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("chr_visibility"),
            [["Character Index", "uint", 0],
             ["Visibility", "bool", False]]
        ))
        self.do_modify()

    def add_chr_slot(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("chr_slot"),
            [["Character Index", "uint", 0],
             ["Slot", "int", 0]]
        ))
        self.do_modify()

    def add_chr_anim(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("chr_anim"),
            [["Character ID", "uint", 0],
             ["Animation", "str", "NONE"]]
        ))
        self.do_modify()

    def add_show_chapter(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("show_chapter"),
            [["Chapter Number", "uint", 0]]
        ))
        self.do_modify()

    def add_wait(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("wait"),
            [["Wait Frames", "uint", 180]]
        ))
        self.do_modify()

    def add_bg_opacity(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("bg_opacity"),
            [["unk0", "uint", 0],
             ["unk1", "uint", 0],
             ["unk2", "uint", 0],
             ["Opacity", "uint", 120]]
        ))
        self.do_modify()

    def add_set_voice(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("set_voice"),
            [["Voice ID", "uint", 0]]
        ))
        self.do_modify()

    def add_sfx_sad(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("sfx_sad"),
            [["SFX ID", "uint", 0]]
        ))
        self.do_modify()

    def add_bg_music(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("bg_music"),
            [["Music ID", "uint", 0],
             ["Volume", "float", 1.0],
             ["unk2", "uint", 0]]
        ))
        self.do_modify()

    def add_bg_shake(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("bg_shake"),
            [["unk0", "uint", 30],
             "Screen", "uint", 0]
        ))
        self.do_modify()

    def add_sfx_sed(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("sfx_sed"),
            [["SFX ID", "uint", 0]]
        ))
        self.do_modify()

    def add_btm_fade_out(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("bgm_fade_out"),
            [["unk0", "float", 0],
             ["unk1", "uint", 320]]
        ))
        self.do_modify()

    def add_btm_fade_in(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("bgm_fade_in"),
            [["unk0", "float", 1.0],
             ["unk1", "uint", 320]]
        ))
        self.do_modify()

    def add_dialogue_sfx(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("dialogue_sfx"),
            [["SAD SFX ID", "uint", 0],
             ["unk1", "float", 0.0],
             ["unk2", "uint", 0],
             ["unk2", "uint", 0]]
        ))
        self.do_modify()

    def add_wait_tap(self, _):
        self.add_command_panel(CommandRepr(
            EventGDSParser().parse_cmd("wait_tap"),
            []
        ))
        self.do_modify()
