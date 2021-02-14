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
## Class PuzzleInputEditor
###########################################################################

class PuzzleInputEditor ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 793,467 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )

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
		bSizer71.Add( self.m_panel28, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel36 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel36.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.m_panel36.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer80 = wx.BoxSizer( wx.VERTICAL )

		self.input_bg_preview = wx.StaticBitmap( self.m_panel36, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 256,256 ), 0 )
		bSizer80.Add( self.input_bg_preview, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		self.input_bg_lbl = wx.StaticText( self.m_panel36, wx.ID_ANY, u"Input BG: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.input_bg_lbl.Wrap( -1 )

		bSizer81.Add( self.input_bg_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.input_bg_inp = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.input_bg_inp, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer80.Add( bSizer81, 0, wx.ALIGN_CENTER, 5 )

		bSizer82 = wx.BoxSizer( wx.HORIZONTAL )

		self.type_of_input_lbl = wx.StaticText( self.m_panel36, wx.ID_ANY, u"Type of input: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.type_of_input_lbl.Wrap( -1 )

		bSizer82.Add( self.type_of_input_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.type_of_input_inp = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.type_of_input_inp, 1, wx.ALL, 5 )


		bSizer80.Add( bSizer82, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer83 = wx.BoxSizer( wx.HORIZONTAL )

		self.answer_lbl = wx.StaticText( self.m_panel36, wx.ID_ANY, u"Answer: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.answer_lbl.Wrap( -1 )

		bSizer83.Add( self.answer_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.answer_inp = wx.TextCtrl( self.m_panel36, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer83.Add( self.answer_inp, 1, wx.ALL, 5 )


		bSizer80.Add( bSizer83, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.m_panel36.SetSizer( bSizer80 )
		self.m_panel36.Layout()
		bSizer80.Fit( self.m_panel36 )
		bSizer71.Add( self.m_panel36, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer71 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.gds_load_button.Bind( wx.EVT_BUTTON, self.OnButtonGDSLoad )
		self.gds_save_button.Bind( wx.EVT_BUTTON, self.OnButtonGDSSave )
		self.m_button43.Bind( wx.EVT_BUTTON, self.OnButtonUpdatePuzzlePreview )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnButtonGDSLoad( self, event ):
		event.Skip()

	def OnButtonGDSSave( self, event ):
		event.Skip()

	def OnButtonUpdatePuzzlePreview( self, event ):
		event.Skip()


