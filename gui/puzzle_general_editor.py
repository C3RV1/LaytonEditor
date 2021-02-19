import wx

import formats.gds
import formats.puzzles.puzzle_data as pzd
import formats.puzzles.puzzle_gds_parser as pgp
import gui.generated


class PuzzleGeneralEditor(gui.generated.PuzzleGeneralEditor):
    def __init__(self, parent):
        super(PuzzleGeneralEditor, self).__init__(parent)

        self.puzzle_data = pzd.PuzzleData(rom=parent.rom)

        self.puzzle_gds_parser = None

        self.current_selected = -1
        self.current_params = []
        self.current_param_labels = []
        self.current_param_inputs = []
        self.current_param_types = []

    def update_puzzle_preview(self):
        self.puzzle_preview.SetBitmap(self.puzzle_data.bg.extract_image_wx_bitmap())

    def OnButtonGDSLoad(self, event):
        puzzle_id = int(self.gds_load_input.Value, 0)
        self.puzzle_data.set_internal_id(puzzle_id)
        if not self.puzzle_data.load_from_rom():
            gds_error = wx.MessageDialog(self, "Can't load puzzle (not found)", style=wx.ICON_ERROR | wx.OK)
            gds_error.ShowModal()
            return
        if not self.puzzle_data.load_gds():
            gds_error = wx.MessageDialog(self, "Can't load gds (not found)", style=wx.ICON_ERROR | wx.OK)
            gds_error.ShowModal()
            return

        self.current_selected = -1
        self.destroy_current()
        self.load_gds_parser()
        self.update_gds_list()
        self.update_puzzle_preview()

    def OnButtonGDSSave(self, event):
        self.save_current()
        self.puzzle_data.set_internal_id(int(self.gds_save_input.Value, 0))
        if not self.puzzle_data.save_gds():
            gds_error = wx.MessageDialog(self, "Can't save gds (not found)", style=wx.ICON_ERROR | wx.OK)
            gds_error.ShowModal()
            return

        successful = wx.MessageDialog(self, "Saved successfully")
        successful.ShowModal()

    def OnButtonUpdatePuzzlePreview(self, event):
        self.update_puzzle_preview()

    def OnCommandListSelected(self, event: wx.ListEvent):
        self.save_current()
        self.current_selected = event.GetIndex()
        self.generate_params()
        self.update_gds_list()

    def load_gds_parser(self):
        if self.puzzle_data.type in pzd.PuzzleData.INPUTS:
            self.puzzle_gds_parser = pgp.InputGDSParser()
        elif self.puzzle_data.type == pzd.PuzzleData.MULTIPLE_CHOICE:
            self.puzzle_gds_parser = pgp.MultipleChoiceGDSParser()
        else:
            self.puzzle_gds_parser = pgp.PuzzleGDSParser()

    def destroy_current(self):
        master_sizer: wx.Sizer = self.parameter_lbl.GetContainingSizer()

        for param in self.current_params:  # type: wx.Sizer
            count = param.GetItemCount()
            for _ in range(count):
                param.GetChildren()[0].GetWindow().Destroy()
            master_sizer.Remove(param)
        self.current_params = []
        self.current_param_labels = []
        self.current_param_inputs = []
        self.current_param_types = []

    def generate_params(self):
        self.destroy_current()
        master_sizer: wx.Sizer = self.parameter_lbl.GetContainingSizer()
        command: formats.gds.GDSCommand = self.puzzle_data.gds.commands[self.current_selected]

        def helper_add_param(param_lbl, param_value):
            param_sizer = wx.BoxSizer()
            param_lbl = wx.StaticText(self.m_panel36, label=param_lbl)
            param_sizer.Add(param_lbl, 1, wx.ALL, 5)
            param_inp = wx.TextCtrl(self.m_panel36, value=str(param_value))
            param_sizer.Add(param_inp, 1, wx.ALL, 5)
            param_type = wx.TextCtrl(self.m_panel36, value=self.puzzle_gds_parser.parse_type(param_value))
            param_sizer.Add(param_type, 1, wx.ALL, 5)
            master_sizer.Add(param_sizer, 0, wx.EXPAND, 5)

            self.current_params.append(param_sizer)
            self.current_param_labels.append(param_lbl)
            self.current_param_inputs.append(param_inp)
            self.current_param_types.append(param_type)

        helper_add_param("Command", command.command)

        params_parsed = self.puzzle_gds_parser.parse_command_params(command)
        for param in range(len(command.params)):
            helper_add_param(params_parsed[param], command.params[param])

        self.Layout()

    def save_current(self):
        if self.current_selected == -1:
            return
        self.puzzle_data.gds.commands[self.current_selected] = formats.gds.GDSCommand(
            int(self.current_param_inputs[0].Value)
        )
        params = self.current_param_inputs[1:]
        types = self.current_param_types[1:]
        for i in range(len(params)):
            value = self.puzzle_gds_parser.from_parsed_type(types[i].Value, params[i].Value)
            self.puzzle_data.gds.commands[self.current_selected].params.append(value)

    def update_gds_list(self):
        self.command_list.DeleteAllItems()

        for command in self.puzzle_data.gds.commands:
            command_name = self.puzzle_gds_parser.parse_command_name(command)
            self.command_list.Append((command_name,))

    def OnCmdNew(self, event):
        if self.current_selected == -1:
            self.current_selected = len(self.puzzle_data.gds.commands) - 1
        self.current_selected += 1
        self.puzzle_data.gds.commands.insert(self.current_selected, formats.gds.GDSCommand(0))
        self.update_gds_list()
        self.generate_params()

    def OnCmdDel(self, event):
        if self.current_selected == -1:
            return
        self.puzzle_data.gds.commands.pop(self.current_selected)
        self.current_selected -= 1
        if self.current_selected < 0:
            self.current_selected = -1
        self.update_gds_list()
        self.generate_params()

    def OnCmdUp(self, event):
        if self.current_selected <= 0:
            return
        previous_element = self.puzzle_data.gds.commands[self.current_selected - 1]
        current_element = self.puzzle_data.gds.commands[self.current_selected]
        self.puzzle_data.gds.commands[self.current_selected] = previous_element
        self.puzzle_data.gds.commands[self.current_selected - 1] = current_element
        self.current_selected -= 1
        self.update_gds_list()
        self.generate_params()

    def OnCmdDown(self, event):
        if self.current_selected == -1 or self.current_selected >= len(self.puzzle_data.gds.commands) - 1:
            return
        next_element = self.puzzle_data.gds.commands[self.current_selected + 1]
        current_element = self.puzzle_data.gds.commands[self.current_selected]
        self.puzzle_data.gds.commands[self.current_selected] = next_element
        self.puzzle_data.gds.commands[self.current_selected + 1] = current_element
        self.current_selected += 1
        self.update_gds_list()
        self.generate_params()

    def OnParamSetNum(self, event):
        if self.current_selected == -1:
            return
        number_of_params = int(str(self.param_num_inp.Value), 0)

        current_command: formats.gds.GDSCommand = self.puzzle_data.gds.commands[self.current_selected]
        current_command.params = [0] * number_of_params
        self.generate_params()
