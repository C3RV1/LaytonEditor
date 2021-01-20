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
## Class PuzzleBaseDataEditor
###########################################################################

class PuzzleBaseDataEditor ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit Puzzle Base Data", pos = wx.DefaultPosition, size = wx.Size( 794,509 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel25 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel25.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer42 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel29 = wx.Panel( self.m_panel25, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer46 = wx.BoxSizer( wx.VERTICAL )

		self.puzz_display = wx.StaticBitmap( self.m_panel29, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 256,256 ), 0 )
		bSizer46.Add( self.puzz_display, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel29.SetSizer( bSizer46 )
		self.m_panel29.Layout()
		bSizer46.Fit( self.m_panel29 )
		bSizer42.Add( self.m_panel29, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer45 = wx.BoxSizer( wx.HORIZONTAL )

		self.puzz_id_label = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Puzzle Internal ID:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.puzz_id_label.Wrap( -1 )

		bSizer45.Add( self.puzz_id_label, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.puzz_id_text = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer45.Add( self.puzz_id_text, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.load_puzz = wx.Button( self.m_panel25, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer45.Add( self.load_puzz, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer42.Add( bSizer45, 0, wx.EXPAND, 5 )

		bSizer54 = wx.BoxSizer( wx.HORIZONTAL )

		self.puzzle_number_label = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Puzzle Number:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.puzzle_number_label.Wrap( -1 )

		bSizer54.Add( self.puzzle_number_label, 1, wx.ALL, 5 )

		self.puzzle_num_display = wx.StaticText( self.m_panel25, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.puzzle_num_display.Wrap( -1 )

		bSizer54.Add( self.puzzle_num_display, 1, wx.ALL, 5 )

		self.padding_label = wx.StaticText( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.padding_label.Wrap( -1 )

		bSizer54.Add( self.padding_label, 1, wx.ALL, 5 )


		bSizer42.Add( bSizer54, 0, wx.EXPAND, 5 )

		bSizer50 = wx.BoxSizer( wx.HORIZONTAL )

		self.puzz_title_label = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Puzzle Title:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.puzz_title_label.Wrap( -1 )

		bSizer50.Add( self.puzz_title_label, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.puzz_title_input = wx.TextCtrl( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.puzz_title_input.SetMaxLength( 48 )
		bSizer50.Add( self.puzz_title_input, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.padding_style = wx.StaticText( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.padding_style.Wrap( -1 )

		bSizer50.Add( self.padding_style, 1, wx.ALL, 5 )


		bSizer42.Add( bSizer50, 0, wx.EXPAND, 5 )

		bSizer53 = wx.BoxSizer( wx.HORIZONTAL )

		self.puzzle_type_label = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Puzzle Type: ", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.puzzle_type_label.Wrap( -1 )

		bSizer53.Add( self.puzzle_type_label, 1, wx.ALL, 5 )

		puzzle_type_choiceChoices = [ u"unknown0", u"unknown1", u"Multiple Choice", u"Mark Answer", u"unknown4", u"Circle Answer", u"unknown6", u"unknown7", u"unknown8", u"Line Separe", u"Sort", u"unknownB", u"unknownC", u"unknownD", u"unknownE", u"unknownF", u"unknown10", u"unknown11", u"Tile Rotate", u"unknown13", u"unknown14", u"unknown15", u"Input", u"Area", u"unknown18", u"Slide", u"Tile Rotate 2", u"unknown1B", u"unknown1C", u"unknown1D", u"unknown1E", u"unknown1F", u"unknown20", u"unknown21", u"unknown22", u"unknown23", wx.EmptyString ]
		self.puzzle_type_choice = wx.Choice( self.m_panel25, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, puzzle_type_choiceChoices, 0 )
		self.puzzle_type_choice.SetSelection( 0 )
		bSizer53.Add( self.puzzle_type_choice, 1, wx.ALL, 5 )

		self.padding_label2 = wx.StaticText( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.padding_label2.Wrap( -1 )

		bSizer53.Add( self.padding_label2, 1, wx.ALL, 5 )


		bSizer42.Add( bSizer53, 0, wx.EXPAND, 5 )

		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )

		self.save_puzzle_button = wx.Button( self.m_panel25, wx.ID_ANY, u"Save Puzzle", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.save_puzzle_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.saved_successfully = wx.CheckBox( self.m_panel25, wx.ID_ANY, u"Saved successfully", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.saved_successfully.Enable( False )

		bSizer51.Add( self.saved_successfully, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer42.Add( bSizer51, 0, wx.ALIGN_CENTER, 5 )


		self.m_panel25.SetSizer( bSizer42 )
		self.m_panel25.Layout()
		bSizer42.Fit( self.m_panel25 )
		bSizer41.Add( self.m_panel25, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel26 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel26.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer47 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel30 = wx.Panel( self.m_panel26, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer48 = wx.BoxSizer( wx.VERTICAL )

		self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_panel30, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		bSizer49 = wx.BoxSizer( wx.VERTICAL )

		self.puzz_txt_label = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Puzzle Introduction", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.puzz_txt_label.Wrap( -1 )

		bSizer49.Add( self.puzz_txt_label, 1, wx.ALL|wx.EXPAND, 5 )

		self.puzz_txt_input = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer49.Add( self.puzz_txt_input, 3, wx.ALL|wx.EXPAND, 5 )

		self.correct_label = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Correct Answer", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.correct_label.Wrap( -1 )

		bSizer49.Add( self.correct_label, 1, wx.ALL|wx.EXPAND, 5 )

		self.correct_input = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer49.Add( self.correct_input, 3, wx.ALL|wx.EXPAND, 5 )

		self.incorrect_label = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Incorrect Answer", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.incorrect_label.Wrap( -1 )

		bSizer49.Add( self.incorrect_label, 1, wx.ALL|wx.EXPAND, 5 )

		self.incorrect_input = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer49.Add( self.incorrect_input, 3, wx.ALL|wx.EXPAND, 5 )

		self.hint1_label = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Hint 1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.hint1_label.Wrap( -1 )

		bSizer49.Add( self.hint1_label, 1, wx.ALL|wx.EXPAND, 5 )

		self.hint1_input = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer49.Add( self.hint1_input, 3, wx.ALL|wx.EXPAND, 5 )

		self.hint2_label = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Hint 2", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.hint2_label.Wrap( -1 )

		bSizer49.Add( self.hint2_label, 1, wx.ALL|wx.EXPAND, 5 )

		self.hint2_input = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer49.Add( self.hint2_input, 3, wx.ALL|wx.EXPAND, 5 )

		self.hint3_label = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Hint 3", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.hint3_label.Wrap( -1 )

		bSizer49.Add( self.hint3_label, 1, wx.ALL|wx.EXPAND, 5 )

		self.hint3_input = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer49.Add( self.hint3_input, 3, wx.ALL|wx.EXPAND, 5 )


		self.m_scrolledWindow1.SetSizer( bSizer49 )
		self.m_scrolledWindow1.Layout()
		bSizer49.Fit( self.m_scrolledWindow1 )
		bSizer48.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel30.SetSizer( bSizer48 )
		self.m_panel30.Layout()
		bSizer48.Fit( self.m_panel30 )
		bSizer47.Add( self.m_panel30, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel26.SetSizer( bSizer47 )
		self.m_panel26.Layout()
		bSizer47.Fit( self.m_panel26 )
		bSizer41.Add( self.m_panel26, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer41 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.load_puzz.Bind( wx.EVT_BUTTON, self.OnButtonLoadPuzzle )
		self.save_puzzle_button.Bind( wx.EVT_BUTTON, self.OnButtonSavePuzzle )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnButtonLoadPuzzle( self, event ):
		event.Skip()

	def OnButtonSavePuzzle( self, event ):
		event.Skip()


