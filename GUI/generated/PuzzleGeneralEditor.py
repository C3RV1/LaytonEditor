# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class PuzzleGeneralEditor
###########################################################################

class PuzzleGeneralEditor ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Puzzle GDS Editor", pos = wx.DefaultPosition, size = wx.Size( 1026,583 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer70 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel28 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel28.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.m_panel28.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer54 = wx.BoxSizer( wx.VERTICAL )

		self.puzzle_preview = wx.StaticBitmap( self.m_panel28, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.puzzle_preview.SetMinSize( wx.Size( 256,256 ) )

		bSizer54.Add( self.puzzle_preview, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		bSizer561 = wx.BoxSizer( wx.HORIZONTAL )

		self.gds_load_label = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Load from puzzle (id):", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.gds_load_label.Wrap( -1 )

		bSizer561.Add( self.gds_load_label, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.gds_load_input = wx.TextCtrl( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer561.Add( self.gds_load_input, 1, wx.ALL, 5 )

		self.gds_load_button = wx.Button( self.m_panel28, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer561.Add( self.gds_load_button, 1, wx.ALL, 5 )


		bSizer54.Add( bSizer561, 0, wx.EXPAND, 5 )

		bSizer56 = wx.BoxSizer( wx.HORIZONTAL )

		self.gds_save_label = wx.StaticText( self.m_panel28, wx.ID_ANY, u"Save to puzzle (id):", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.gds_save_label.Wrap( -1 )

		bSizer56.Add( self.gds_save_label, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.gds_save_input = wx.TextCtrl( self.m_panel28, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.gds_save_input, 1, wx.ALL, 5 )

		self.gds_save_button = wx.Button( self.m_panel28, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.gds_save_button, 1, wx.ALL, 5 )


		bSizer54.Add( bSizer56, 0, wx.EXPAND, 5 )

		self.m_button43 = wx.Button( self.m_panel28, wx.ID_ANY, u"Update Puzzle Preview", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer54.Add( self.m_button43, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel28.SetSizer( bSizer54 )
		self.m_panel28.Layout()
		bSizer54.Fit( self.m_panel28 )
		bSizer70.Add( self.m_panel28, 3, wx.EXPAND |wx.ALL, 5 )

		self.m_panel36 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel36.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.m_panel36.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer77 = wx.BoxSizer( wx.VERTICAL )

		bSizer78 = wx.BoxSizer( wx.HORIZONTAL )

		self.commands_lbl = wx.StaticText( self.m_panel36, wx.ID_ANY, u"Commands", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.commands_lbl.Wrap( -1 )

		bSizer78.Add( self.commands_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.button_cmd_new = wx.Button( self.m_panel36, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer78.Add( self.button_cmd_new, 1, wx.ALL, 5 )

		self.button_cmd_delete = wx.Button( self.m_panel36, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer78.Add( self.button_cmd_delete, 1, wx.ALL, 5 )

		self.button_cmd_up = wx.Button( self.m_panel36, wx.ID_ANY, u"Move up", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer78.Add( self.button_cmd_up, 1, wx.ALL, 5 )

		self.button_cmd_down = wx.Button( self.m_panel36, wx.ID_ANY, u"Move down", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer78.Add( self.button_cmd_down, 1, wx.ALL, 5 )


		bSizer77.Add( bSizer78, 0, wx.EXPAND, 5 )

		self.command_list = wx.ListCtrl( self.m_panel36, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST )
		bSizer77.Add( self.command_list, 1, wx.ALL|wx.EXPAND, 5 )

		parameter_sizer = wx.BoxSizer( wx.VERTICAL )

		self.parameter_lbl = wx.StaticText( self.m_panel36, wx.ID_ANY, u"Parameters", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.parameter_lbl.Wrap( -1 )

		parameter_sizer.Add( self.parameter_lbl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		bSizer771 = wx.BoxSizer( wx.HORIZONTAL )

		self.param_num_inp = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer771.Add( self.param_num_inp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.button_set_param_num = wx.Button( self.m_panel36, wx.ID_ANY, u"Set number of parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer771.Add( self.button_set_param_num, 1, wx.ALL, 5 )


		parameter_sizer.Add( bSizer771, 0, wx.EXPAND, 5 )


		bSizer77.Add( parameter_sizer, 1, wx.EXPAND, 5 )


		self.m_panel36.SetSizer( bSizer77 )
		self.m_panel36.Layout()
		bSizer77.Fit( self.m_panel36 )
		bSizer70.Add( self.m_panel36, 4, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer70 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.gds_load_button.Bind( wx.EVT_BUTTON, self.OnButtonGDSLoad )
		self.gds_save_button.Bind( wx.EVT_BUTTON, self.OnButtonGDSSave )
		self.m_button43.Bind( wx.EVT_BUTTON, self.OnButtonUpdatePuzzlePreview )
		self.button_cmd_new.Bind( wx.EVT_BUTTON, self.OnCmdNew )
		self.button_cmd_delete.Bind( wx.EVT_BUTTON, self.OnCmdDel )
		self.button_cmd_up.Bind( wx.EVT_BUTTON, self.OnCmdUp )
		self.button_cmd_down.Bind( wx.EVT_BUTTON, self.OnCmdDown )
		self.command_list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnCommandListSelected )
		self.button_set_param_num.Bind( wx.EVT_BUTTON, self.OnParamSetNum )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnButtonGDSLoad( self, event ):
		event.Skip()

	def OnButtonGDSSave( self, event ):
		event.Skip()

	def OnButtonUpdatePuzzlePreview( self, event ):
		event.Skip()

	def OnCmdNew( self, event ):
		event.Skip()

	def OnCmdDel( self, event ):
		event.Skip()

	def OnCmdUp( self, event ):
		event.Skip()

	def OnCmdDown( self, event ):
		event.Skip()

	def OnCommandListSelected( self, event ):
		event.Skip()

	def OnParamSetNum( self, event ):
		event.Skip()


