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
## Class PuzzleMultipleChoice
###########################################################################

class PuzzleMultipleChoice ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Create Puzzle Multiple Choice", pos = wx.DefaultPosition, size = wx.Size( 774,488 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )

		bSizer53 = wx.BoxSizer( wx.HORIZONTAL )

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
		bSizer53.Add( self.m_panel28, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel29 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel29.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer57 = wx.BoxSizer( wx.VERTICAL )

		bSizer63 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_new_button = wx.Button( self.m_panel29, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer63.Add( self.m_new_button, 1, wx.ALL, 5 )

		self.m_button46 = wx.Button( self.m_panel29, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer63.Add( self.m_button46, 1, wx.ALL, 5 )


		bSizer57.Add( bSizer63, 0, wx.EXPAND, 5 )

		self.buttons_tree = wx.TreeCtrl( self.m_panel29, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		bSizer57.Add( self.buttons_tree, 1, wx.ALL|wx.EXPAND, 5 )

		self.edit_gds_pannel = wx.Panel( self.m_panel29, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer58 = wx.BoxSizer( wx.VERTICAL )

		bSizer59 = wx.BoxSizer( wx.HORIZONTAL )

		self.x_label = wx.StaticText( self.edit_gds_pannel, wx.ID_ANY, u"X:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.x_label.Wrap( -1 )

		bSizer59.Add( self.x_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.x_input = wx.TextCtrl( self.edit_gds_pannel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer59.Add( self.x_input, 0, wx.ALL, 5 )

		self.y_label = wx.StaticText( self.edit_gds_pannel, wx.ID_ANY, u"Y:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.y_label.Wrap( -1 )

		bSizer59.Add( self.y_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.y_input = wx.TextCtrl( self.edit_gds_pannel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer59.Add( self.y_input, 0, wx.ALL, 5 )


		bSizer58.Add( bSizer59, 0, wx.ALIGN_CENTER, 5 )

		bSizer60 = wx.BoxSizer( wx.HORIZONTAL )

		self.freebutton_label = wx.StaticText( self.edit_gds_pannel, wx.ID_ANY, u"Freebutton: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.freebutton_label.Wrap( -1 )

		bSizer60.Add( self.freebutton_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.freebutton_input = wx.TextCtrl( self.edit_gds_pannel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer60.Add( self.freebutton_input, 0, wx.ALL, 5 )


		bSizer58.Add( bSizer60, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer62 = wx.BoxSizer( wx.HORIZONTAL )

		self.is_correct_checkbox = wx.CheckBox( self.edit_gds_pannel, wx.ID_ANY, u"Is a solution: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer62.Add( self.is_correct_checkbox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.sfx_label = wx.StaticText( self.edit_gds_pannel, wx.ID_ANY, u"SFX: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sfx_label.Wrap( -1 )

		bSizer62.Add( self.sfx_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.sfx_input = wx.TextCtrl( self.edit_gds_pannel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer62.Add( self.sfx_input, 0, wx.ALL, 5 )


		bSizer58.Add( bSizer62, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.edit_gds_pannel.SetSizer( bSizer58 )
		self.edit_gds_pannel.Layout()
		bSizer58.Fit( self.edit_gds_pannel )
		bSizer57.Add( self.edit_gds_pannel, 0, wx.EXPAND |wx.ALL, 5 )


		self.m_panel29.SetSizer( bSizer57 )
		self.m_panel29.Layout()
		bSizer57.Fit( self.m_panel29 )
		bSizer53.Add( self.m_panel29, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer53 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.gds_load_button.Bind( wx.EVT_BUTTON, self.OnButtonGDSLoad )
		self.gds_save_button.Bind( wx.EVT_BUTTON, self.OnButtonGDSSave )
		self.m_button43.Bind( wx.EVT_BUTTON, self.OnButtonUpdatePuzzlePreview )
		self.m_new_button.Bind( wx.EVT_BUTTON, self.OnButtonNew )
		self.m_button46.Bind( wx.EVT_BUTTON, self.OnButtonDelete )
		self.buttons_tree.Bind( wx.EVT_TREE_SEL_CHANGED, self.ObjTreeSelChanged )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnButtonGDSLoad( self, event ):
		event.Skip()

	def OnButtonGDSSave( self, event ):
		event.Skip()

	def OnButtonUpdatePuzzlePreview( self, event ):
		event.Skip()

	def OnButtonNew( self, event ):
		event.Skip()

	def OnButtonDelete( self, event ):
		event.Skip()

	def ObjTreeSelChanged( self, event ):
		event.Skip()


