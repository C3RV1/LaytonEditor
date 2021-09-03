# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Mar 23 2021)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from gui.previews.gds_stc import GdsSTC
from gui.previews.scaledimage import ScaledImage
from gui.previews.placeviewer import PlaceViewer
import wx
import wx.xrc
import wx.aui
import wx.stc
import wx.dataview
import wx.propgrid as pg

###########################################################################
## Class MainEditor
###########################################################################

class MainEditor ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Layton Editor", pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.le_menu = wx.MenuBar( 0 )
		self.le_menu_file = wx.Menu()
		self.le_menu_file_open = wx.MenuItem( self.le_menu_file, wx.ID_ANY, u"Open Rom", wx.EmptyString, wx.ITEM_NORMAL )
		self.le_menu_file.Append( self.le_menu_file_open )

		self.le_menu_file_save = wx.MenuItem( self.le_menu_file, wx.ID_ANY, u"Save Rom", wx.EmptyString, wx.ITEM_NORMAL )
		self.le_menu_file.Append( self.le_menu_file_save )

		self.le_menu_file_saveas = wx.MenuItem( self.le_menu_file, wx.ID_ANY, u"Save Rom As", wx.EmptyString, wx.ITEM_NORMAL )
		self.le_menu_file.Append( self.le_menu_file_saveas )

		self.le_menu.Append( self.le_menu_file, u"File" )

		self.SetMenuBar( self.le_menu )

		le_layout = wx.BoxSizer( wx.VERTICAL )

		self.le_editor_pages = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.le_no_file_opened = wx.Panel( self.le_editor_pages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		nfo_layout = wx.BoxSizer( wx.HORIZONTAL )

		self.nfo_text = wx.StaticText( self.le_no_file_opened, wx.ID_ANY, u"No rom is currently opened.\nGo to File > Open Rom to open a rom.\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.nfo_text.Wrap( -1 )

		nfo_layout.Add( self.nfo_text, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		self.le_no_file_opened.SetSizer( nfo_layout )
		self.le_no_file_opened.Layout()
		nfo_layout.Fit( self.le_no_file_opened )
		self.le_editor_pages.AddPage( self.le_no_file_opened, u"No open rom", False, wx.NullBitmap )

		le_layout.Add( self.le_editor_pages, 1, wx.EXPAND, 5 )


		self.SetSizer( le_layout )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.close_window )
		self.Bind( wx.EVT_MENU, self.le_menu_file_open_OnMenuSelection, id = self.le_menu_file_open.GetId() )
		self.Bind( wx.EVT_MENU, self.le_menu_file_save_OnMenuSelection, id = self.le_menu_file_save.GetId() )
		self.Bind( wx.EVT_MENU, self.le_menu_file_saveas_OnMenuSelection, id = self.le_menu_file_saveas.GetId() )
		self.le_editor_pages.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.le_page_changed )
		self.le_editor_pages.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.le_page_changing )
		self.le_editor_pages.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.le_page_close )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def close_window( self, event ):
		event.Skip()

	def le_menu_file_open_OnMenuSelection( self, event ):
		event.Skip()

	def le_menu_file_save_OnMenuSelection( self, event ):
		event.Skip()

	def le_menu_file_saveas_OnMenuSelection( self, event ):
		event.Skip()

	def le_page_changed( self, event ):
		event.Skip()

	def le_page_changing( self, event ):
		event.Skip()

	def le_page_close( self, event ):
		event.Skip()


###########################################################################
## Class FilesystemEditor
###########################################################################

class FilesystemEditor ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		fs_layout = wx.BoxSizer( wx.VERTICAL )

		self.fs_split_ft_fp = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_LIVE_UPDATE )
		self.fs_split_ft_fp.Bind( wx.EVT_IDLE, self.fs_split_ft_fpOnIdle )

		self.fs_filetree = wx.Panel( self.fs_split_ft_fp, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ft_layout = wx.BoxSizer( wx.VERTICAL )

		self.ft_filetree = wx.TreeCtrl( self.fs_filetree, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_EDIT_LABELS|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_TWIST_BUTTONS )
		self.ft_filetree.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		ft_layout.Add( self.ft_filetree, 1, wx.EXPAND, 5 )


		self.fs_filetree.SetSizer( ft_layout )
		self.fs_filetree.Layout()
		ft_layout.Fit( self.fs_filetree )
		self.fs_filepreview = wx.Panel( self.fs_split_ft_fp, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_formats_book = wx.Simplebook( self.fs_filepreview, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fp_empty = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.fp_formats_book.AddPage( self.fp_empty, u"a page", True )
		self.fp_text = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_text_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_text_edit = wx.TextCtrl( self.fp_text, wx.ID_ANY, u"Hello World!", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		fp_text_layout.Add( self.fp_text_edit, 1, wx.EXPAND, 5 )


		self.fp_text.SetSizer( fp_text_layout )
		self.fp_text.Layout()
		fp_text_layout.Fit( self.fp_text )
		self.fp_formats_book.AddPage( self.fp_text, u"a page", False )
		self.fp_gds = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_gds_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_gds_stc = GdsSTC( self.fp_gds, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
		self.fp_gds_stc.SetUseTabs ( True )
		self.fp_gds_stc.SetTabWidth ( 4 )
		self.fp_gds_stc.SetIndent ( 4 )
		self.fp_gds_stc.SetTabIndents( True )
		self.fp_gds_stc.SetBackSpaceUnIndents( True )
		self.fp_gds_stc.SetViewEOL( False )
		self.fp_gds_stc.SetViewWhiteSpace( False )
		self.fp_gds_stc.SetMarginWidth( 2, 0 )
		self.fp_gds_stc.SetIndentationGuides( True )
		self.fp_gds_stc.SetReadOnly( False )
		self.fp_gds_stc.SetMarginType ( 1, wx.stc.STC_MARGIN_SYMBOL )
		self.fp_gds_stc.SetMarginMask ( 1, wx.stc.STC_MASK_FOLDERS )
		self.fp_gds_stc.SetMarginWidth ( 1, 16)
		self.fp_gds_stc.SetMarginSensitive( 1, True )
		self.fp_gds_stc.SetProperty ( "fold", "1" )
		self.fp_gds_stc.SetFoldFlags ( wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED )
		self.fp_gds_stc.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER )
		self.fp_gds_stc.SetMarginWidth( 0, self.fp_gds_stc.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.fp_gds_stc.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.fp_gds_stc.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.fp_gds_stc.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.fp_gds_stc.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.fp_gds_stc.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.fp_gds_stc.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.fp_gds_stc.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.fp_gds_stc.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.fp_gds_stc.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.fp_gds_stc.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.fp_gds_stc.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		fp_gds_layout.Add( self.fp_gds_stc, 1, wx.EXPAND, 5 )

		fp_gds_cmd_layout = wx.BoxSizer( wx.HORIZONTAL )

		self.fp_gds_cmd_name = wx.StaticText( self.fp_gds, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fp_gds_cmd_name.Wrap( -1 )

		self.fp_gds_cmd_name.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		fp_gds_cmd_layout.Add( self.fp_gds_cmd_name, 0, wx.TOP|wx.BOTTOM|wx.LEFT, 5 )

		self.fp_gds_cmd_help = wx.StaticText( self.fp_gds, wx.ID_ANY, u"g", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fp_gds_cmd_help.Wrap( -1 )

		fp_gds_cmd_layout.Add( self.fp_gds_cmd_help, 0, wx.ALL, 5 )


		fp_gds_layout.Add( fp_gds_cmd_layout, 0, wx.EXPAND, 5 )


		self.fp_gds.SetSizer( fp_gds_layout )
		self.fp_gds.Layout()
		fp_gds_layout.Fit( self.fp_gds )
		self.fp_formats_book.AddPage( self.fp_gds, u"a page", False )
		self.fp_bg = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_bg_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_bg_viewimage_scaled = ScaledImage( self.fp_bg, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.fp_bg_viewimage_scaled.SetBackgroundColour( wx.Colour( 248, 248, 248 ) )

		fp_bg_layout.Add( self.fp_bg_viewimage_scaled, 1, wx.EXPAND, 5 )


		self.fp_bg.SetSizer( fp_bg_layout )
		self.fp_bg.Layout()
		fp_bg_layout.Fit( self.fp_bg )
		self.fp_formats_book.AddPage( self.fp_bg, u"a page", False )
		self.fp_ani = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_ani_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_ani_imageindex = wx.Slider( self.fp_ani, wx.ID_ANY, 0, 0, 4, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_LABELS )
		fp_ani_layout.Add( self.fp_ani_imageindex, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )

		self.fp_ani_viewimage_scaled = ScaledImage( self.fp_ani, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.fp_ani_viewimage_scaled.SetBackgroundColour( wx.Colour( 248, 248, 248 ) )

		fp_ani_layout.Add( self.fp_ani_viewimage_scaled, 1, wx.ALL|wx.EXPAND, 5 )


		self.fp_ani.SetSizer( fp_ani_layout )
		self.fp_ani.Layout()
		fp_ani_layout.Fit( self.fp_ani )
		self.fp_formats_book.AddPage( self.fp_ani, u"a page", False )
		self.fp_place = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_place_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_place_viewer = PlaceViewer( self.fp_place, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_place_layout.Add( self.fp_place_viewer, 1, wx.EXPAND |wx.ALL, 5 )


		self.fp_place.SetSizer( fp_place_layout )
		self.fp_place.Layout()
		fp_place_layout.Fit( self.fp_place )
		self.fp_formats_book.AddPage( self.fp_place, u"a page", False )
		self.fp_samplebank = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_samplebank_layout = wx.BoxSizer( wx.VERTICAL )

		fp_samplebank_listChoices = []
		self.fp_samplebank_list = wx.ListBox( self.fp_samplebank, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, fp_samplebank_listChoices, 0 )
		fp_samplebank_layout.Add( self.fp_samplebank_list, 1, wx.ALL|wx.EXPAND, 5 )


		self.fp_samplebank.SetSizer( fp_samplebank_layout )
		self.fp_samplebank.Layout()
		fp_samplebank_layout.Fit( self.fp_samplebank )
		self.fp_formats_book.AddPage( self.fp_samplebank, u"a page", False )
		self.fp_info = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_info_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_info_text = wx.TextCtrl( self.fp_info, wx.ID_ANY, u"Hello World!", wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.fp_info_text.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )

		fp_info_layout.Add( self.fp_info_text, 1, wx.EXPAND, 5 )


		self.fp_info.SetSizer( fp_info_layout )
		self.fp_info.Layout()
		fp_info_layout.Fit( self.fp_info )
		self.fp_formats_book.AddPage( self.fp_info, u"a page", False )
		self.fp_puzzle = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fp_puzzle_layout = wx.BoxSizer( wx.VERTICAL )

		self.puzzle_scintilla = wx.stc.StyledTextCtrl( self.fp_puzzle, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
		self.puzzle_scintilla.SetUseTabs ( False )
		self.puzzle_scintilla.SetTabWidth ( 4 )
		self.puzzle_scintilla.SetIndent ( 4 )
		self.puzzle_scintilla.SetTabIndents( True )
		self.puzzle_scintilla.SetBackSpaceUnIndents( True )
		self.puzzle_scintilla.SetViewEOL( False )
		self.puzzle_scintilla.SetViewWhiteSpace( False )
		self.puzzle_scintilla.SetMarginWidth( 2, 0 )
		self.puzzle_scintilla.SetIndentationGuides( True )
		self.puzzle_scintilla.SetReadOnly( False )
		self.puzzle_scintilla.SetMarginType ( 1, wx.stc.STC_MARGIN_SYMBOL )
		self.puzzle_scintilla.SetMarginMask ( 1, wx.stc.STC_MASK_FOLDERS )
		self.puzzle_scintilla.SetMarginWidth ( 1, 16)
		self.puzzle_scintilla.SetMarginSensitive( 1, True )
		self.puzzle_scintilla.SetProperty ( "fold", "1" )
		self.puzzle_scintilla.SetFoldFlags ( wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED )
		self.puzzle_scintilla.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER )
		self.puzzle_scintilla.SetMarginWidth( 0, self.puzzle_scintilla.TextWidth( wx.stc.STC_STYLE_LINENUMBER, "_99999" ) )
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDER, wx.stc.STC_MARK_BOXPLUS )
		self.puzzle_scintilla.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDER, wx.BLACK)
		self.puzzle_scintilla.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDER, wx.WHITE)
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.stc.STC_MARK_BOXMINUS )
		self.puzzle_scintilla.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.BLACK )
		self.puzzle_scintilla.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPEN, wx.WHITE )
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERSUB, wx.stc.STC_MARK_EMPTY )
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEREND, wx.stc.STC_MARK_BOXPLUS )
		self.puzzle_scintilla.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEREND, wx.BLACK )
		self.puzzle_scintilla.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEREND, wx.WHITE )
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUS )
		self.puzzle_scintilla.MarkerSetBackground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.BLACK)
		self.puzzle_scintilla.MarkerSetForeground( wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.WHITE)
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_EMPTY )
		self.puzzle_scintilla.MarkerDefine( wx.stc.STC_MARKNUM_FOLDERTAIL, wx.stc.STC_MARK_EMPTY )
		self.puzzle_scintilla.SetSelBackground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT ) )
		self.puzzle_scintilla.SetSelForeground( True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		fp_puzzle_layout.Add( self.puzzle_scintilla, 1, wx.EXPAND |wx.ALL, 0 )


		self.fp_puzzle.SetSizer( fp_puzzle_layout )
		self.fp_puzzle.Layout()
		fp_puzzle_layout.Fit( self.fp_puzzle )
		self.fp_formats_book.AddPage( self.fp_puzzle, u"a page", False )

		fp_layout.Add( self.fp_formats_book, 1, wx.EXPAND, 5 )


		self.fs_filepreview.SetSizer( fp_layout )
		self.fs_filepreview.Layout()
		fp_layout.Fit( self.fs_filepreview )
		self.fs_split_ft_fp.SplitVertically( self.fs_filetree, self.fs_filepreview, 0 )
		fs_layout.Add( self.fs_split_ft_fp, 1, wx.EXPAND, 5 )


		self.SetSizer( fs_layout )
		self.Layout()

		# Connect Events
		self.ft_filetree.Bind( wx.EVT_TREE_END_LABEL_EDIT, self.ft_filetree_end_label_edit )
		self.ft_filetree.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.ft_filetree_activated )
		self.ft_filetree.Bind( wx.EVT_TREE_KEY_DOWN, self.ft_filetree_keydown )
		self.ft_filetree.Bind( wx.EVT_TREE_SEL_CHANGED, self.ft_filetree_selchanged )
		self.fp_text_edit.Bind( wx.EVT_TEXT, self.fp_text_edit_changed )
		self.fp_gds_stc.Bind( wx.EVT_UPDATE_UI, self.fp_gds_stc_updateui )
		self.fp_ani_imageindex.Bind( wx.EVT_SLIDER, self.fp_ani_imageindex_on_slider )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def ft_filetree_end_label_edit( self, event ):
		event.Skip()

	def ft_filetree_activated( self, event ):
		event.Skip()

	def ft_filetree_keydown( self, event ):
		event.Skip()

	def ft_filetree_selchanged( self, event ):
		event.Skip()

	def fp_text_edit_changed( self, event ):
		event.Skip()

	def fp_gds_stc_updateui( self, event ):
		event.Skip()

	def fp_ani_imageindex_on_slider( self, event ):
		event.Skip()

	def fs_split_ft_fpOnIdle( self, event ):
		self.fs_split_ft_fp.SetSashPosition( 0 )
		self.fs_split_ft_fp.Unbind( wx.EVT_IDLE )


###########################################################################
## Class SpriteEditor
###########################################################################

class SpriteEditor ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		ase_layout = wx.BoxSizer( wx.VERTICAL )

		self.ase_split = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.ase_split.Bind( wx.EVT_IDLE, self.ase_splitOnIdle )

		self.ase_page_animations = wx.Panel( self.ase_split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ase_animations_layout = wx.BoxSizer( wx.VERTICAL )

		self.ase_animations_list = wx.ListCtrl( self.ase_page_animations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_EDIT_LABELS|wx.LC_HRULES|wx.LC_LIST|wx.LC_SINGLE_SEL )
		ase_animations_layout.Add( self.ase_animations_list, 1, wx.ALL|wx.EXPAND, 5 )

		self.ase_frame_slider = wx.Slider( self.ase_page_animations, wx.ID_ANY, 50, 0, 5, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_MIN_MAX_LABELS )
		ase_animations_layout.Add( self.ase_frame_slider, 0, wx.ALL|wx.EXPAND, 5 )

		self.ase_frame_view = ScaledImage( self.ase_page_animations, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ase_animations_layout.Add( self.ase_frame_view, 2, wx.EXPAND |wx.ALL, 5 )

		ase_frame_properties = wx.GridSizer( 0, 3, 0, 0 )

		ase_prop_frame_index = wx.BoxSizer( wx.VERTICAL )

		self.ase_prop_frame_index_label = wx.StaticText( self.ase_page_animations, wx.ID_ANY, u"Frame Index:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.ase_prop_frame_index_label.Wrap( -1 )

		ase_prop_frame_index.Add( self.ase_prop_frame_index_label, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.ase_prop_frame_index_spin = wx.SpinCtrl( self.ase_page_animations, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		ase_prop_frame_index.Add( self.ase_prop_frame_index_spin, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		ase_frame_properties.Add( ase_prop_frame_index, 1, wx.EXPAND, 5 )

		ase_prop_frame_duration = wx.BoxSizer( wx.VERTICAL )

		self.ase_prop_frame_duration_label = wx.StaticText( self.ase_page_animations, wx.ID_ANY, u"Frame Duration:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.ase_prop_frame_duration_label.Wrap( -1 )

		ase_prop_frame_duration.Add( self.ase_prop_frame_duration_label, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.ase_prop_frame_duration_spin = wx.SpinCtrl( self.ase_page_animations, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		ase_prop_frame_duration.Add( self.ase_prop_frame_duration_spin, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )


		ase_frame_properties.Add( ase_prop_frame_duration, 1, wx.EXPAND, 5 )

		ase_prop_image_index1 = wx.BoxSizer( wx.VERTICAL )

		self.ase_prop_image_index = wx.StaticText( self.ase_page_animations, wx.ID_ANY, u"Image Index:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.ase_prop_image_index.Wrap( -1 )

		ase_prop_image_index1.Add( self.ase_prop_image_index, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.ase_prop_image_index_spin = wx.SpinCtrl( self.ase_page_animations, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		ase_prop_image_index1.Add( self.ase_prop_image_index_spin, 0, wx.BOTTOM|wx.RIGHT|wx.LEFT|wx.EXPAND, 5 )


		ase_frame_properties.Add( ase_prop_image_index1, 1, wx.EXPAND, 5 )


		ase_animations_layout.Add( ase_frame_properties, 0, wx.EXPAND, 5 )


		self.ase_page_animations.SetSizer( ase_animations_layout )
		self.ase_page_animations.Layout()
		ase_animations_layout.Fit( self.ase_page_animations )
		self.ase_other_panel = wx.Panel( self.ase_split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ase_other_layout = wx.BoxSizer( wx.VERTICAL )

		self.ase_other_pages = wx.Notebook( self.ase_other_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ase_images_panel = wx.Panel( self.ase_other_pages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ase_images_layout = wx.BoxSizer( wx.VERTICAL )

		self.ase_images_slider = wx.Slider( self.ase_images_panel, wx.ID_ANY, 5, 0, 5, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_MIN_MAX_LABELS )
		ase_images_layout.Add( self.ase_images_slider, 0, wx.ALL|wx.EXPAND, 5 )

		self.ase_images_view = ScaledImage( self.ase_images_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ase_images_layout.Add( self.ase_images_view, 1, wx.EXPAND |wx.ALL, 5 )


		self.ase_images_panel.SetSizer( ase_images_layout )
		self.ase_images_panel.Layout()
		ase_images_layout.Fit( self.ase_images_panel )
		self.ase_other_pages.AddPage( self.ase_images_panel, u"Images", False )
		self.ase_page_variables = wx.Panel( self.ase_other_pages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		ase_variables_layout = wx.BoxSizer( wx.VERTICAL )

		self.ase_variables_dataview = wx.dataview.DataViewListCtrl( self.ase_page_variables, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ase_variables_names = self.ase_variables_dataview.AppendTextColumn( u"Name", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_1 = self.ase_variables_dataview.AppendTextColumn( u"Value 1", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_2 = self.ase_variables_dataview.AppendTextColumn( u"Value 2", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_3 = self.ase_variables_dataview.AppendTextColumn( u"Value 3", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_4 = self.ase_variables_dataview.AppendTextColumn( u"Value 4", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_5 = self.ase_variables_dataview.AppendTextColumn( u"Value 5", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_6 = self.ase_variables_dataview.AppendTextColumn( u"Value 6", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_7 = self.ase_variables_dataview.AppendTextColumn( u"Value 7", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_8 = self.ase_variables_dataview.AppendTextColumn( u"Value 8", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		ase_variables_layout.Add( self.ase_variables_dataview, 1, wx.ALL|wx.EXPAND, 5 )


		self.ase_page_variables.SetSizer( ase_variables_layout )
		self.ase_page_variables.Layout()
		ase_variables_layout.Fit( self.ase_page_variables )
		self.ase_other_pages.AddPage( self.ase_page_variables, u"Variables", True )

		ase_other_layout.Add( self.ase_other_pages, 1, wx.EXPAND |wx.ALL, 5 )


		self.ase_other_panel.SetSizer( ase_other_layout )
		self.ase_other_panel.Layout()
		ase_other_layout.Fit( self.ase_other_panel )
		self.ase_split.SplitVertically( self.ase_page_animations, self.ase_other_panel, 0 )
		ase_layout.Add( self.ase_split, 1, wx.EXPAND, 5 )


		self.SetSizer( ase_layout )
		self.Layout()

		# Connect Events
		self.ase_animations_list.Bind( wx.EVT_LIST_END_LABEL_EDIT, self.ase_animations_list_label_edit )
		self.ase_animations_list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.ase_animations_list_selected )
		self.ase_frame_slider.Bind( wx.EVT_SLIDER, self.ase_frame_slider_changed )
		self.ase_prop_frame_index_spin.Bind( wx.EVT_SPINCTRL, self.ase_prop_frame_index_spin_changed )
		self.ase_prop_frame_duration_spin.Bind( wx.EVT_SPINCTRL, self.ase_prop_frame_duration_spin_changed )
		self.ase_prop_image_index_spin.Bind( wx.EVT_SPINCTRL, self.ase_prop_image_index_spin_changed )
		self.ase_other_panel.Bind( wx.EVT_LEFT_DCLICK, self.ase_other_mouse_event )
		self.ase_other_panel.Bind( wx.EVT_LEFT_DOWN, self.ase_other_mouse_event )
		self.ase_other_panel.Bind( wx.EVT_MIDDLE_DCLICK, self.ase_other_mouse_event )
		self.ase_other_panel.Bind( wx.EVT_MIDDLE_DOWN, self.ase_other_mouse_event )
		self.ase_other_panel.Bind( wx.EVT_RIGHT_DCLICK, self.ase_other_mouse_event )
		self.ase_other_panel.Bind( wx.EVT_RIGHT_DOWN, self.ase_other_mouse_event )
		self.ase_images_panel.Bind( wx.EVT_LEFT_DCLICK, self.ase_images_mouse_event )
		self.ase_images_panel.Bind( wx.EVT_LEFT_DOWN, self.ase_images_mouse_event )
		self.ase_images_panel.Bind( wx.EVT_MIDDLE_DCLICK, self.ase_images_mouse_event )
		self.ase_images_panel.Bind( wx.EVT_MIDDLE_DOWN, self.ase_images_mouse_event )
		self.ase_images_panel.Bind( wx.EVT_RIGHT_DCLICK, self.ase_images_mouse_event )
		self.ase_images_panel.Bind( wx.EVT_RIGHT_DOWN, self.ase_images_mouse_event )
		self.ase_images_slider.Bind( wx.EVT_SLIDER, self.ase_images_slider_changed )
		self.ase_variables_dataview.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EDITING_DONE, self.ase_variables_dataview_edited, id = wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def ase_animations_list_label_edit( self, event ):
		event.Skip()

	def ase_animations_list_selected( self, event ):
		event.Skip()

	def ase_frame_slider_changed( self, event ):
		event.Skip()

	def ase_prop_frame_index_spin_changed( self, event ):
		event.Skip()

	def ase_prop_frame_duration_spin_changed( self, event ):
		event.Skip()

	def ase_prop_image_index_spin_changed( self, event ):
		event.Skip()

	def ase_other_mouse_event( self, event ):
		event.Skip()






	def ase_images_mouse_event( self, event ):
		event.Skip()






	def ase_images_slider_changed( self, event ):
		event.Skip()

	def ase_variables_dataview_edited( self, event ):
		event.Skip()

	def ase_splitOnIdle( self, event ):
		self.ase_split.SetSashPosition( 0 )
		self.ase_split.Unbind( wx.EVT_IDLE )


###########################################################################
## Class Arm9PatchPage
###########################################################################

class Arm9PatchPage ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		ap_layout = wx.BoxSizer( wx.VERTICAL )

		fp_code_layout = wx.BoxSizer( wx.VERTICAL )

		self.fp_code_message = wx.StaticText( self, wx.ID_ANY, u"Patch Arm9", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
		self.fp_code_message.Wrap( -1 )

		self.fp_code_message.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		fp_code_layout.Add( self.fp_code_message, 0, wx.ALL|wx.EXPAND, 5 )

		self.fp_code_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fp_code_layout.Add( self.fp_code_staticline, 0, wx.EXPAND |wx.ALL, 5 )

		self.fp_code_patches_text = wx.StaticText( self, wx.ID_ANY, u"Patch Directory:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fp_code_patches_text.Wrap( -1 )

		fp_code_layout.Add( self.fp_code_patches_text, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.fp_code_patches = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select patches folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL )
		fp_code_layout.Add( self.fp_code_patches, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.fp_code_arenaptraddr = wx.StaticText( self, wx.ID_ANY, u"Arena Pointer Address:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fp_code_arenaptraddr.Wrap( -1 )

		fp_code_layout.Add( self.fp_code_arenaptraddr, 0, wx.TOP|wx.RIGHT|wx.LEFT, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fp_code_layout.Add( self.m_textCtrl2, 0, wx.EXPAND|wx.BOTTOM|wx.RIGHT|wx.LEFT, 5 )

		self.fp_code_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fp_code_layout.Add( self.fp_code_staticline1, 0, wx.EXPAND |wx.ALL, 5 )


		fp_code_layout.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		fp_code_buttons = wx.BoxSizer( wx.HORIZONTAL )

		self.fp_code_btn_patch = wx.Button( self, wx.ID_ANY, u"Patch", wx.DefaultPosition, wx.DefaultSize, 0 )
		fp_code_buttons.Add( self.fp_code_btn_patch, 1, wx.ALL, 5 )

		self.fp_code_btn_restore = wx.Button( self, wx.ID_ANY, u"Restore", wx.DefaultPosition, wx.DefaultSize, 0 )
		fp_code_buttons.Add( self.fp_code_btn_restore, 1, wx.ALL, 5 )


		fp_code_layout.Add( fp_code_buttons, 0, wx.EXPAND, 5 )


		ap_layout.Add( fp_code_layout, 1, wx.EXPAND, 5 )


		self.SetSizer( ap_layout )
		self.Layout()

	def __del__( self ):
		pass


###########################################################################
## Class PlaceEditor
###########################################################################

class PlaceEditor ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		plc_layout = wx.BoxSizer( wx.VERTICAL )

		self.plc_split = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.plc_split.Bind( wx.EVT_IDLE, self.plc_splitOnIdle )

		self.plc_preview = PlaceViewer( self.plc_split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.plc_data = wx.Panel( self.plc_split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		plc_data_layout = wx.BoxSizer( wx.VERTICAL )

		self.plc_items = wx.TreeCtrl( self.plc_data, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		plc_data_layout.Add( self.plc_items, 1, wx.ALL|wx.EXPAND, 5 )

		self.plc_item_data = pg.PropertyGrid(self.plc_data, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		self.m_propertyGridItem1 = self.plc_item_data.Append( pg.StringProperty( u"Name", u"Name" ) )
		plc_data_layout.Add( self.plc_item_data, 1, wx.ALL|wx.EXPAND, 5 )


		self.plc_data.SetSizer( plc_data_layout )
		self.plc_data.Layout()
		plc_data_layout.Fit( self.plc_data )
		self.plc_split.SplitVertically( self.plc_preview, self.plc_data, 0 )
		plc_layout.Add( self.plc_split, 1, wx.EXPAND, 5 )


		self.SetSizer( plc_layout )
		self.Layout()

		# Connect Events
		self.plc_items.Bind( wx.EVT_TREE_SEL_CHANGED, self.plc_items_selchanged )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def plc_items_selchanged( self, event ):
		event.Skip()

	def plc_splitOnIdle( self, event ):
		self.plc_split.SetSashPosition( 0 )
		self.plc_split.Unbind( wx.EVT_IDLE )


###########################################################################
## Class EventEditor
###########################################################################

class EventEditor ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		self.event_commands_add = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.ALWAYS_SHOW_SB|wx.HSCROLL|wx.VSCROLL )
		self.event_commands_add.SetScrollRate( 5, 5 )
		self.event_commands_add.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.event_commands_add.SetMaxSize( wx.Size( -1,300 ) )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_dialogueBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Dialogue", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_dialogueBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_fadeBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Fade", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_fadeBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bgLoadBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Background Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_bgLoadBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_setModeBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_setModeBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_setNextModeBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Next Mode", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_setNextModeBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_setMovieBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Movie", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_setMovieBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_setEventBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Event", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_setEventBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_setPuzzleBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Puzzle", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_setPuzzleBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chrShowBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Show Character", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_chrShowBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chrHideBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Hide Character", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_chrHideBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chrVisibilityBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Character Visibility", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_chrVisibilityBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chrSlotBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Character Slot", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_chrSlotBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_chrAnimBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Character Animation", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_chrAnimBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_showChapterBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Show Chapter", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_showChapterBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_waitBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Wait", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_waitBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bgOpacityBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Background Opacity", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_bgOpacityBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_setVoiceBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Voice", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_setVoiceBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_sfxSadBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Play SAD SFX", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_sfxSadBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bgMusicBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Play Background Music", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_bgMusicBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bgShakeBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Shake Background", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_bgShakeBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_sfxSedBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Play SED SFX", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_sfxSedBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bgmFadeOutBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Fade Out BG Music", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_bgmFadeOutBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_bgmFadeInBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Fade In BG Music", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_bgmFadeInBtn, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_dialogueSfxBtn = wx.Button( self.event_commands_add, wx.ID_ANY, u"Set Dialogue SFX", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_dialogueSfxBtn, 0, wx.ALL|wx.EXPAND, 5 )


		self.event_commands_add.SetSizer( gSizer2 )
		self.event_commands_add.Layout()
		gSizer2.Fit( self.event_commands_add )
		bSizer30.Add( self.event_commands_add, 1, wx.ALL|wx.EXPAND, 5 )

		self.character_info = pg.PropertyGridManager(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PGMAN_DEFAULT_STYLE|wx.propgrid.PG_HIDE_MARGIN|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.propgrid.PG_TOOLBAR|wx.propgrid.PG_TOOLTIPS|wx.TAB_TRAVERSAL)
		self.character_info.SetExtraStyle( wx.propgrid.PG_EX_MODE_BUTTONS )
		self.character_info.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )


		self.event_info = self.character_info.AddPage( u"Page", wx.NullBitmap )
		self.m_mapTopID = self.event_info.Append( pg.IntProperty( u"Map Top ID", u"Map Top ID" ) )
		self.m_mapBtmID = self.event_info.Append( pg.IntProperty( u"Map Bottom ID", u"Map Bottom ID" ) )

		self.character_info0 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id0 = self.character_info0.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot0 = self.character_info0.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim0 = self.character_info0.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible0 = self.character_info0.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info1 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id1 = self.character_info1.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot1 = self.character_info1.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim1 = self.character_info1.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible1 = self.character_info1.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info2 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id2 = self.character_info2.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot2 = self.character_info2.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim2 = self.character_info2.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible2 = self.character_info2.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info3 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id3 = self.character_info3.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot3 = self.character_info3.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim3 = self.character_info3.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible3 = self.character_info3.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info4 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id4 = self.character_info4.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot4 = self.character_info4.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim4 = self.character_info4.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible4 = self.character_info4.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info5 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id5 = self.character_info5.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot5 = self.character_info5.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim5 = self.character_info5.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible5 = self.character_info5.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info6 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id6 = self.character_info6.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot6 = self.character_info6.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim6 = self.character_info6.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible6 = self.character_info6.Append( pg.BoolProperty( u"Visible", u"Visible" ) )

		self.character_info7 = self.character_info.AddPage( u"Character 0", wx.NullBitmap )
		self.char_id7 = self.character_info7.Append( pg.IntProperty( u"Character ID", u"Character ID" ) )
		self.char_slot7 = self.character_info7.Append( pg.IntProperty( u"Slot", u"Slot" ) )
		self.char_anim7 = self.character_info7.Append( pg.IntProperty( u"Animation Index", u"Animation Index" ) )
		self.char_visible7 = self.character_info7.Append( pg.BoolProperty( u"Visible", u"Visible" ) )
		bSizer30.Add( self.character_info, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer28.Add( bSizer30, 2, wx.EXPAND, 5 )

		self.event_commands = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.event_commands.SetScrollRate( 5, 5 )
		self.event_commands.SetMaxSize( wx.Size( 600,600 ) )

		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel25 = wx.Panel( self.event_commands, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel25.SetBackgroundColour( wx.Colour( 192, 192, 192 ) )

		bSizer32 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText10 = wx.StaticText( self.m_panel25, wx.ID_ANY, u"Dialogue", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer32.Add( self.m_staticText10, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel25.SetSizer( bSizer32 )
		self.m_panel25.Layout()
		bSizer32.Fit( self.m_panel25 )
		bSizer31.Add( self.m_panel25, 0, wx.EXPAND |wx.ALL, 5 )


		self.event_commands.SetSizer( bSizer31 )
		self.event_commands.Layout()
		bSizer31.Fit( self.event_commands )
		bSizer28.Add( self.event_commands, 3, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer28 )
		self.Layout()

		# Connect Events
		self.m_dialogueBtn.Bind( wx.EVT_BUTTON, self.add_dialogue )
		self.m_fadeBtn.Bind( wx.EVT_BUTTON, self.add_fade )
		self.m_bgLoadBtn.Bind( wx.EVT_BUTTON, self.add_bg_load )
		self.m_setModeBtn.Bind( wx.EVT_BUTTON, self.add_set_mode )
		self.m_setNextModeBtn.Bind( wx.EVT_BUTTON, self.add_set_next_mode )
		self.m_setMovieBtn.Bind( wx.EVT_BUTTON, self.add_set_movie )
		self.m_setEventBtn.Bind( wx.EVT_BUTTON, self.add_set_event )
		self.m_setPuzzleBtn.Bind( wx.EVT_BUTTON, self.add_set_puzzle )
		self.m_chrShowBtn.Bind( wx.EVT_BUTTON, self.add_chr_show )
		self.m_chrHideBtn.Bind( wx.EVT_BUTTON, self.add_chr_hide )
		self.m_chrVisibilityBtn.Bind( wx.EVT_BUTTON, self.add_chr_visibility )
		self.m_chrSlotBtn.Bind( wx.EVT_BUTTON, self.add_chr_slot )
		self.m_chrAnimBtn.Bind( wx.EVT_BUTTON, self.add_chr_anim )
		self.m_showChapterBtn.Bind( wx.EVT_BUTTON, self.add_show_chapter )
		self.m_waitBtn.Bind( wx.EVT_BUTTON, self.add_wait )
		self.m_bgOpacityBtn.Bind( wx.EVT_BUTTON, self.add_bg_opacity )
		self.m_setVoiceBtn.Bind( wx.EVT_BUTTON, self.add_set_voice )
		self.m_sfxSadBtn.Bind( wx.EVT_BUTTON, self.add_sfx_sad )
		self.m_bgMusicBtn.Bind( wx.EVT_BUTTON, self.add_bg_music )
		self.m_bgShakeBtn.Bind( wx.EVT_BUTTON, self.add_bg_shake )
		self.m_sfxSedBtn.Bind( wx.EVT_BUTTON, self.add_sfx_sed )
		self.m_bgmFadeOutBtn.Bind( wx.EVT_BUTTON, self.add_btm_fade_out )
		self.m_bgmFadeInBtn.Bind( wx.EVT_BUTTON, self.add_btm_fade_in )
		self.m_dialogueSfxBtn.Bind( wx.EVT_BUTTON, self.add_dialogue_sfx )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def add_dialogue( self, event ):
		event.Skip()

	def add_fade( self, event ):
		event.Skip()

	def add_bg_load( self, event ):
		event.Skip()

	def add_set_mode( self, event ):
		event.Skip()

	def add_set_next_mode( self, event ):
		event.Skip()

	def add_set_movie( self, event ):
		event.Skip()

	def add_set_event( self, event ):
		event.Skip()

	def add_set_puzzle( self, event ):
		event.Skip()

	def add_chr_show( self, event ):
		event.Skip()

	def add_chr_hide( self, event ):
		event.Skip()

	def add_chr_visibility( self, event ):
		event.Skip()

	def add_chr_slot( self, event ):
		event.Skip()

	def add_chr_anim( self, event ):
		event.Skip()

	def add_show_chapter( self, event ):
		event.Skip()

	def add_wait( self, event ):
		event.Skip()

	def add_bg_opacity( self, event ):
		event.Skip()

	def add_set_voice( self, event ):
		event.Skip()

	def add_sfx_sad( self, event ):
		event.Skip()

	def add_bg_music( self, event ):
		event.Skip()

	def add_bg_shake( self, event ):
		event.Skip()

	def add_sfx_sed( self, event ):
		event.Skip()

	def add_btm_fade_out( self, event ):
		event.Skip()

	def add_btm_fade_in( self, event ):
		event.Skip()

	def add_dialogue_sfx( self, event ):
		event.Skip()


