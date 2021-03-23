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
from gui.previews.puzzleviewer import PuzzleViewer
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

		self.le_menu_puzzles = wx.Menu()
		self.le_menu_puzzles_edit_base_data = wx.MenuItem( self.le_menu_puzzles, wx.ID_ANY, u"Edit Base Data", wx.EmptyString, wx.ITEM_NORMAL )
		self.le_menu_puzzles.Append( self.le_menu_puzzles_edit_base_data )

		self.le_menu_puzzles_edit_gds = wx.MenuItem( self.le_menu_puzzles, wx.ID_ANY, u"Puzzle GDS Editor", wx.EmptyString, wx.ITEM_NORMAL )
		self.le_menu_puzzles.Append( self.le_menu_puzzles_edit_gds )

		self.le_menu.Append( self.le_menu_puzzles, u"Puzzles" )

		self.event_menu = wx.Menu()
		self.event_editor = wx.MenuItem( self.event_menu, wx.ID_ANY, u"Event Editor", wx.EmptyString, wx.ITEM_NORMAL )
		self.event_menu.Append( self.event_editor )

		self.le_menu.Append( self.event_menu, u"Events" )

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
		self.Bind( wx.EVT_MENU, self.le_menu_file_open_OnMenuSelection, id = self.le_menu_file_open.GetId() )
		self.Bind( wx.EVT_MENU, self.le_menu_file_save_OnMenuSelection, id = self.le_menu_file_save.GetId() )
		self.Bind( wx.EVT_MENU, self.le_menu_file_saveas_OnMenuSelection, id = self.le_menu_file_saveas.GetId() )
		self.Bind( wx.EVT_MENU, self.le_menu_puzzles_edit_base_data_clicked, id = self.le_menu_puzzles_edit_base_data.GetId() )
		self.Bind( wx.EVT_MENU, self.le_menu_puzzles_edit_gds_clicked, id = self.le_menu_puzzles_edit_gds.GetId() )
		self.Bind( wx.EVT_MENU, self.event_editor_clicked, id = self.event_editor.GetId() )
		self.le_editor_pages.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.le_page_changed )
		self.le_editor_pages.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.le_page_changing )
		self.le_editor_pages.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.le_page_close )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def le_menu_file_open_OnMenuSelection( self, event ):
		event.Skip()

	def le_menu_file_save_OnMenuSelection( self, event ):
		event.Skip()

	def le_menu_file_saveas_OnMenuSelection( self, event ):
		event.Skip()

	def le_menu_puzzles_edit_base_data_clicked( self, event ):
		event.Skip()

	def le_menu_puzzles_edit_gds_clicked( self, event ):
		event.Skip()

	def event_editor_clicked( self, event ):
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
		self.fp_gds_stc.SetReadOnly( False );
		self.fp_gds_stc.SetMarginType ( 1, wx.stc.STC_MARGIN_SYMBOL )
		self.fp_gds_stc.SetMarginMask ( 1, wx.stc.STC_MASK_FOLDERS )
		self.fp_gds_stc.SetMarginWidth ( 1, 16)
		self.fp_gds_stc.SetMarginSensitive( 1, True )
		self.fp_gds_stc.SetProperty ( "fold", "1" )
		self.fp_gds_stc.SetFoldFlags ( wx.stc.STC_FOLDFLAG_LINEBEFORE_CONTRACTED | wx.stc.STC_FOLDFLAG_LINEAFTER_CONTRACTED );
		self.fp_gds_stc.SetMarginType( 0, wx.stc.STC_MARGIN_NUMBER );
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
		self.m_panel26 = wx.Panel( self.fp_formats_book, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.fp_formats_book.AddPage( self.m_panel26, u"a page", False )

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
		self.ase_variables_names = self.ase_variables_dataview.AppendTextColumn( u"Name", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_1 = self.ase_variables_dataview.AppendTextColumn( u"Value 1", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_2 = self.ase_variables_dataview.AppendTextColumn( u"Value 2", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_3 = self.ase_variables_dataview.AppendTextColumn( u"Value 3", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_4 = self.ase_variables_dataview.AppendTextColumn( u"Value 4", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_5 = self.ase_variables_dataview.AppendTextColumn( u"Value 5", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_6 = self.ase_variables_dataview.AppendTextColumn( u"Value 6", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_7 = self.ase_variables_dataview.AppendTextColumn( u"Value 7", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.ase_variables_dataview_value_8 = self.ase_variables_dataview.AppendTextColumn( u"Value 8", wx.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
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
## Class PuzzleEditor
###########################################################################

class PuzzleEditor ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		pz_layout = wx.BoxSizer( wx.VERTICAL )

		self.pz_split = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.pz_split.Bind( wx.EVT_IDLE, self.pz_splitOnIdle )

		self.pz_preview = PuzzleViewer( self.pz_split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.pz_data = wx.Panel( self.pz_split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		pz_data_layout = wx.BoxSizer( wx.VERTICAL )

		self.pz_data_grid = pg.PropertyGrid(self.pz_data, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		self.m_propertyGridItem2 = self.pz_data_grid.Append( pg.StringProperty( u"Name", u"Name" ) )
		pz_data_layout.Add( self.pz_data_grid, 1, wx.ALL|wx.EXPAND, 5 )


		self.pz_data.SetSizer( pz_data_layout )
		self.pz_data.Layout()
		pz_data_layout.Fit( self.pz_data )
		self.pz_split.SplitVertically( self.pz_preview, self.pz_data, 0 )
		pz_layout.Add( self.pz_split, 1, wx.EXPAND, 5 )


		self.SetSizer( pz_layout )
		self.Layout()

	def __del__( self ):
		pass

	def pz_splitOnIdle( self, event ):
		self.pz_split.SetSashPosition( 0 )
		self.pz_split.Unbind( wx.EVT_IDLE )


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

		puzzle_type_choiceChoices = [ u"unused0", u"unused1", u"Multiple Choice", u"Mark Answer", u"unused4", u"Circle Answer", u"Draw Line Plaza", u"unused7", u"unused8", u"Line Divide", u"Sort", u"Weather", u"unusedC", u"Piles Of Pancakes", u"unusedE", u"Line Divide Limited", u"Input Chars", u"Knight Tour", u"Tile Rotate", u"unused13", u"unused14", u"unaccessible_172_202_15", u"Input Numeric", u"Area", u"Roses", u"Slide", u"Tile Rotate 2", u"Slippery Crossings", u"Input Alt", u"Disappearing Act", u"Jars and Cans", u"Light The Way", u"unaccessible173_0x20", u"Rickety Bridge", u"Find Shape", u"Input Date" ]
		self.puzzle_type_choice = wx.Choice( self.m_panel25, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, puzzle_type_choiceChoices, 0 )
		self.puzzle_type_choice.SetSelection( 0 )
		bSizer53.Add( self.puzzle_type_choice, 0, wx.ALL, 5 )

		self.padding_label2 = wx.StaticText( self.m_panel25, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.padding_label2.Wrap( -1 )

		bSizer53.Add( self.padding_label2, 1, wx.ALL, 5 )


		bSizer42.Add( bSizer53, 0, wx.EXPAND, 5 )

		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )

		self.save_puzzle_button = wx.Button( self.m_panel25, wx.ID_ANY, u"Save Puzzle", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer51.Add( self.save_puzzle_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


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


###########################################################################
## Class EventEditor
###########################################################################

class EventEditor ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 405,449 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer64 = wx.BoxSizer( wx.VERTICAL )

		bSizer65 = wx.BoxSizer( wx.HORIZONTAL )

		self.event_id_lbl = wx.StaticText( self, wx.ID_ANY, u"Event ID:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.event_id_lbl.Wrap( -1 )

		bSizer65.Add( self.event_id_lbl, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.event_id_inp = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer65.Add( self.event_id_inp, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.load_event_btn = wx.Button( self, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer65.Add( self.load_event_btn, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		bSizer64.Add( bSizer65, 0, wx.EXPAND, 5 )

		bSizer66 = wx.BoxSizer( wx.HORIZONTAL )

		m_listBox2Choices = []
		self.m_listBox2 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_listBox2Choices, 0 )
		bSizer66.Add( self.m_listBox2, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer64.Add( bSizer66, 1, wx.EXPAND, 5 )

		bSizer67 = wx.BoxSizer( wx.VERTICAL )

		self.m_button22 = wx.Button( self, wx.ID_ANY, u"Play", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer67.Add( self.m_button22, 0, wx.ALL, 5 )


		bSizer64.Add( bSizer67, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer64 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.EndPreviewer )
		self.Bind( wx.EVT_SHOW, self.StartPreviewer )
		self.load_event_btn.Bind( wx.EVT_BUTTON, self.OnBtnLoadEvent )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def EndPreviewer( self, event ):
		event.Skip()

	def StartPreviewer( self, event ):
		event.Skip()

	def OnBtnLoadEvent( self, event ):
		event.Skip()


