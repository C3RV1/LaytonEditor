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
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Layton Editor", pos = wx.DefaultPosition, size = wx.Size( 624,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 600,600 ), wx.DefaultSize )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel9 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer141 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter1 = wx.SplitterWindow( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.m_panel_leftside = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_leftside.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )

		bSizer_leftside = wx.BoxSizer( wx.VERTICAL )

		self.tree_imagefiles = wx.TreeCtrl( self.m_panel_leftside, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		bSizer_leftside.Add( self.tree_imagefiles, 1, wx.EXPAND|wx.ALL, 5 )

		gSizer_buttonsleft = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button_extract = wx.Button( self.m_panel_leftside, wx.ID_ANY, u"Extract", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft.Add( self.m_button_extract, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_replacefile = wx.Button( self.m_panel_leftside, wx.ID_ANY, u"Replace", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft.Add( self.m_button_replacefile, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_extractdecom = wx.Button( self.m_panel_leftside, wx.ID_ANY, u"Extract Decompressed", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft.Add( self.m_button_extractdecom, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button23 = wx.Button( self.m_panel_leftside, wx.ID_ANY, u"Replace Decompressed", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft.Add( self.m_button23, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer_leftside.Add( gSizer_buttonsleft, 0, wx.EXPAND, 5 )


		self.m_panel_leftside.SetSizer( bSizer_leftside )
		self.m_panel_leftside.Layout()
		bSizer_leftside.Fit( self.m_panel_leftside )
		self.m_panel_imageinfo = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_imageinfo.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )

		bSizer_imageinfo = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_previewimage = wx.Panel( self.m_panel_imageinfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_previewimage.SetMinSize( wx.Size( 276,202 ) )

		bSizer_previewimage = wx.BoxSizer( wx.VERTICAL )

		self.previewImage = wx.StaticBitmap( self.m_panel_previewimage, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.previewImage.SetMinSize( wx.Size( 256,192 ) )

		bSizer_previewimage.Add( self.previewImage, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.m_panel_previewimage.SetSizer( bSizer_previewimage )
		self.m_panel_previewimage.Layout()
		bSizer_previewimage.Fit( self.m_panel_previewimage )
		bSizer_imageinfo.Add( self.m_panel_previewimage, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer_selectimage = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_previousimage = wx.Button( self.m_panel_imageinfo, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer_selectimage.Add( self.m_button_previousimage, 1, wx.ALL, 5 )

		self.m_staticText_currentimage = wx.StaticText( self.m_panel_imageinfo, wx.ID_ANY, u"0/0", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_currentimage.Wrap( -1 )

		bSizer_selectimage.Add( self.m_staticText_currentimage, 1, wx.ALL|wx.EXPAND, 10 )

		self.m_button_nextimage = wx.Button( self.m_panel_imageinfo, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer_selectimage.Add( self.m_button_nextimage, 1, wx.ALL, 5 )


		bSizer_imageinfo.Add( bSizer_selectimage, 0, wx.EXPAND, 5 )

		self.m_staticText_Colordepth = wx.StaticText( self.m_panel_imageinfo, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_Colordepth.Wrap( -1 )

		bSizer_imageinfo.Add( self.m_staticText_Colordepth, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText_imagename = wx.StaticText( self.m_panel_imageinfo, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_imagename.Wrap( -1 )

		bSizer_imageinfo.Add( self.m_staticText_imagename, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText_imageID = wx.StaticText( self.m_panel_imageinfo, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_imageID.Wrap( -1 )

		bSizer_imageinfo.Add( self.m_staticText_imageID, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panel_filler = wx.Panel( self.m_panel_imageinfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_imageinfo.Add( self.m_panel_filler, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_saveimage = wx.Button( self.m_panel_imageinfo, wx.ID_ANY, u"Save Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_imageinfo.Add( self.m_button_saveimage, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_replaceimage = wx.Button( self.m_panel_imageinfo, wx.ID_ANY, u"Replace Image (no palette change)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_imageinfo.Add( self.m_button_replaceimage, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_replaceimageandpalette = wx.Button( self.m_panel_imageinfo, wx.ID_ANY, u"Replace Image (add to palette)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_imageinfo.Add( self.m_button_replaceimageandpalette, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_editfile = wx.Button( self.m_panel_imageinfo, wx.ID_ANY, u"Edit File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_imageinfo.Add( self.m_button_editfile, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel_imageinfo.SetSizer( bSizer_imageinfo )
		self.m_panel_imageinfo.Layout()
		bSizer_imageinfo.Fit( self.m_panel_imageinfo )
		self.m_splitter1.SplitVertically( self.m_panel_leftside, self.m_panel_imageinfo, 0 )
		bSizer141.Add( self.m_splitter1, 1, wx.EXPAND, 5 )


		self.m_panel9.SetSizer( bSizer141 )
		self.m_panel9.Layout()
		bSizer141.Fit( self.m_panel9 )
		self.m_notebook1.AddPage( self.m_panel9, u"Images", True )
		self.m_panel10 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter3 = wx.SplitterWindow( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )

		self.m_panel11 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer28 = wx.BoxSizer( wx.VERTICAL )

		bSizer_leftside1 = wx.BoxSizer( wx.VERTICAL )

		self.tree_imagefiles1 = wx.TreeCtrl( self.m_panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		bSizer_leftside1.Add( self.tree_imagefiles1, 1, wx.EXPAND|wx.ALL, 5 )

		gSizer_buttonsleft1 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button_extract1 = wx.Button( self.m_panel11, wx.ID_ANY, u"Extract", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft1.Add( self.m_button_extract1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_replacefile1 = wx.Button( self.m_panel11, wx.ID_ANY, u"Replace", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft1.Add( self.m_button_replacefile1, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer_leftside1.Add( gSizer_buttonsleft1, 0, wx.EXPAND, 5 )


		bSizer28.Add( bSizer_leftside1, 1, wx.EXPAND, 5 )


		self.m_panel11.SetSizer( bSizer28 )
		self.m_panel11.Layout()
		bSizer28.Fit( self.m_panel11 )
		self.m_panel12 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer29 = wx.BoxSizer( wx.VERTICAL )

		bSizer_imageinfo1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_previewimage1 = wx.Panel( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_previewimage1.SetMinSize( wx.Size( 276,202 ) )

		bSizer_previewimage1 = wx.BoxSizer( wx.VERTICAL )

		self.previewImage1 = wx.StaticBitmap( self.m_panel_previewimage1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.previewImage1.SetMinSize( wx.Size( 256,192 ) )

		bSizer_previewimage1.Add( self.previewImage1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.m_panel_previewimage1.SetSizer( bSizer_previewimage1 )
		self.m_panel_previewimage1.Layout()
		bSizer_previewimage1.Fit( self.m_panel_previewimage1 )
		bSizer_imageinfo1.Add( self.m_panel_previewimage1, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_Colordepth1 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_Colordepth1.Wrap( -1 )

		bSizer_imageinfo1.Add( self.m_staticText_Colordepth1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText_imagename1 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_imagename1.Wrap( -1 )

		bSizer_imageinfo1.Add( self.m_staticText_imagename1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText_imageID1 = wx.StaticText( self.m_panel12, wx.ID_ANY, u"N/A", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText_imageID1.Wrap( -1 )

		bSizer_imageinfo1.Add( self.m_staticText_imageID1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panel_filler1 = wx.Panel( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer_imageinfo1.Add( self.m_panel_filler1, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_button_saveimage1 = wx.Button( self.m_panel12, wx.ID_ANY, u"Save Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_imageinfo1.Add( self.m_button_saveimage1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_replaceimageandpalette1 = wx.Button( self.m_panel12, wx.ID_ANY, u"Replace Image (add to palette)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_imageinfo1.Add( self.m_button_replaceimageandpalette1, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer29.Add( bSizer_imageinfo1, 1, wx.EXPAND, 5 )


		self.m_panel12.SetSizer( bSizer29 )
		self.m_panel12.Layout()
		bSizer29.Fit( self.m_panel12 )
		self.m_splitter3.SplitVertically( self.m_panel11, self.m_panel12, 0 )
		bSizer27.Add( self.m_splitter3, 1, wx.EXPAND, 5 )


		self.m_panel10.SetSizer( bSizer27 )
		self.m_panel10.Layout()
		bSizer27.Fit( self.m_panel10 )
		self.m_notebook1.AddPage( self.m_panel10, u"Backgrounds", False )
		self.m_panel_text = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter4 = wx.SplitterWindow( self.m_panel_text, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter4.Bind( wx.EVT_IDLE, self.m_splitter4OnIdle )

		self.m_panel16 = wx.Panel( self.m_splitter4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer34 = wx.BoxSizer( wx.VERTICAL )

		self.m_tree_scripts_text = wx.TreeCtrl( self.m_panel16, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT )
		bSizer34.Add( self.m_tree_scripts_text, 1, wx.ALL|wx.EXPAND, 5 )

		gSizer4 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button_extr_text = wx.Button( self.m_panel16, wx.ID_ANY, u"Extract", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_button_extr_text, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button_repl_text = wx.Button( self.m_panel16, wx.ID_ANY, u"Replace", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.m_button_repl_text, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer34.Add( gSizer4, 0, wx.EXPAND, 5 )


		self.m_panel16.SetSizer( bSizer34 )
		self.m_panel16.Layout()
		bSizer34.Fit( self.m_panel16 )
		self.m_panel17 = wx.Panel( self.m_splitter4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer35 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl8 = wx.TextCtrl( self.m_panel17, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE )
		bSizer35.Add( self.m_textCtrl8, 1, wx.ALL|wx.EXPAND, 5 )

		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button_save_text = wx.Button( self.m_panel17, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_button_save_text, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_revert_text = wx.Button( self.m_panel17, wx.ID_ANY, u"Revert", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.m_button_revert_text, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer35.Add( gSizer5, 0, wx.EXPAND, 5 )


		self.m_panel17.SetSizer( bSizer35 )
		self.m_panel17.Layout()
		bSizer35.Fit( self.m_panel17 )
		self.m_splitter4.SplitVertically( self.m_panel16, self.m_panel17, 0 )
		bSizer33.Add( self.m_splitter4, 1, wx.EXPAND, 5 )


		self.m_panel_text.SetSizer( bSizer33 )
		self.m_panel_text.Layout()
		bSizer33.Fit( self.m_panel_text )
		self.m_notebook1.AddPage( self.m_panel_text, u"(Script) Text", False )
		self.m_panel_asmhacks = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText10 = wx.StaticText( self.m_panel_asmhacks, wx.ID_ANY, u"Warning: Only don't use on an already patched rom. It will break the setupcode.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer15.Add( self.m_staticText10, 0, wx.ALL, 5 )

		bSizer191 = wx.BoxSizer( wx.VERTICAL )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText12 = wx.StaticText( self.m_panel_asmhacks, wx.ID_ANY, u"Setup Code Folder: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		bSizer20.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self.m_panel_asmhacks, wx.ID_ANY, u"setupcode/", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer20.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer191.Add( bSizer20, 0, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText13 = wx.StaticText( self.m_panel_asmhacks, wx.ID_ANY, u"Patch Code Folder: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		bSizer21.Add( self.m_staticText13, 0, wx.ALL, 5 )

		self.m_textCtrl3 = wx.TextCtrl( self.m_panel_asmhacks, wx.ID_ANY, u"gamecode/", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_textCtrl3, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer191.Add( bSizer21, 1, wx.EXPAND, 5 )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText131 = wx.StaticText( self.m_panel_asmhacks, wx.ID_ANY, u"ArenaLoOffsetPtr: (hex)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )

		bSizer22.Add( self.m_staticText131, 1, wx.ALL, 5 )

		self.m_textCtrl31 = wx.TextCtrl( self.m_panel_asmhacks, wx.ID_ANY, u"0x0201efb8", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer22.Add( self.m_textCtrl31, 0, wx.ALL, 5 )


		bSizer191.Add( bSizer22, 1, wx.EXPAND, 5 )


		bSizer15.Add( bSizer191, 0, wx.EXPAND, 5 )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button26 = wx.Button( self.m_panel_asmhacks, wx.ID_ANY, u"Patch", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.m_button26, 1, wx.ALIGN_BOTTOM|wx.ALL, 5 )


		bSizer15.Add( bSizer19, 1, wx.EXPAND, 5 )


		self.m_panel_asmhacks.SetSizer( bSizer15 )
		self.m_panel_asmhacks.Layout()
		bSizer15.Fit( self.m_panel_asmhacks )
		self.m_notebook1.AddPage( self.m_panel_asmhacks, u"ASM Patcher", False )

		bSizer14.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer13.Add( bSizer14, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizer13 )
		self.Layout()
		self.m_menubar_windowmenu = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menuItem_openfile = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_openfile )

		self.m_menuItem_savefile = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_savefile )

		self.m_menuItem_savefileas = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Save As", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_savefileas )

		self.m_menubar_windowmenu.Append( self.m_menu_file, u"File" )

		self.m_menu2 = wx.Menu()
		self.m_menuItem4 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Edit Base Data", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem4 )

		self.m_menuItem5 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Create Puzzle Multiple Choice", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem5 )

		self.m_menubar_windowmenu.Append( self.m_menu2, u"Puzzles" )

		self.SetMenuBar( self.m_menubar_windowmenu )


		self.Centre( wx.HORIZONTAL )

		# Connect Events
		self.tree_imagefiles.Bind( wx.EVT_TREE_SEL_CHANGED, self.tree_imagefilesOnTreeSelChanged )
		self.m_button_extract.Bind( wx.EVT_BUTTON, self.OnButtonClickExtract )
		self.m_button_replacefile.Bind( wx.EVT_BUTTON, self.OnButtonClickReplace )
		self.m_button_extractdecom.Bind( wx.EVT_BUTTON, self.OnButtonClickExtractDecom )
		self.m_button23.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceDecom )
		self.m_button_previousimage.Bind( wx.EVT_BUTTON, self.OnButtonClickPreviousImage )
		self.m_button_nextimage.Bind( wx.EVT_BUTTON, self.OnButtonClickNextImage )
		self.m_button_saveimage.Bind( wx.EVT_BUTTON, self.OnButtonClickSaveImage )
		self.m_button_replaceimage.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceImage )
		self.m_button_replaceimageandpalette.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceImageAddPall )
		self.m_button_editfile.Bind( wx.EVT_BUTTON, self.OnButtonClickEditFile )
		self.tree_imagefiles1.Bind( wx.EVT_TREE_SEL_CHANGED, self.tree_imagefilesbgOnTreeSelChanged )
		self.m_button_extract1.Bind( wx.EVT_BUTTON, self.OnButtonClickExtractBG )
		self.m_button_replacefile1.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceBG )
		self.m_button_saveimage1.Bind( wx.EVT_BUTTON, self.OnButtonClickSaveImageBG )
		self.m_button_replaceimageandpalette1.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceImageBG )
		self.m_tree_scripts_text.Bind( wx.EVT_TREE_SEL_CHANGED, self.m_tree_scripts_textOnTreeSelChanged )
		self.m_button_extr_text.Bind( wx.EVT_BUTTON, self.m_button_extr_textOnButtonClick )
		self.m_button_repl_text.Bind( wx.EVT_BUTTON, self.m_button_repl_textOnButtonClick )
		self.m_button_save_text.Bind( wx.EVT_BUTTON, self.m_button_save_textOnButtonClick )
		self.m_button_revert_text.Bind( wx.EVT_BUTTON, self.m_button_revert_textOnButtonClick )
		self.m_button26.Bind( wx.EVT_BUTTON, self.OnButtonClickPatchRom )
		self.Bind( wx.EVT_MENU, self.OnMenuSelectionOpen, id = self.m_menuItem_openfile.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelectionSave, id = self.m_menuItem_savefile.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelectionSaveAs, id = self.m_menuItem_savefileas.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuBaseDataEdit, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuPuzzleMultipleChoice, id = self.m_menuItem5.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def tree_imagefilesOnTreeSelChanged( self, event ):
		event.Skip()

	def OnButtonClickExtract( self, event ):
		event.Skip()

	def OnButtonClickReplace( self, event ):
		event.Skip()

	def OnButtonClickExtractDecom( self, event ):
		event.Skip()

	def OnButtonClickReplaceDecom( self, event ):
		event.Skip()

	def OnButtonClickPreviousImage( self, event ):
		event.Skip()

	def OnButtonClickNextImage( self, event ):
		event.Skip()

	def OnButtonClickSaveImage( self, event ):
		event.Skip()

	def OnButtonClickReplaceImage( self, event ):
		event.Skip()

	def OnButtonClickReplaceImageAddPall( self, event ):
		event.Skip()

	def OnButtonClickEditFile( self, event ):
		event.Skip()

	def tree_imagefilesbgOnTreeSelChanged( self, event ):
		event.Skip()

	def OnButtonClickExtractBG( self, event ):
		event.Skip()

	def OnButtonClickReplaceBG( self, event ):
		event.Skip()

	def OnButtonClickSaveImageBG( self, event ):
		event.Skip()

	def OnButtonClickReplaceImageBG( self, event ):
		event.Skip()

	def m_tree_scripts_textOnTreeSelChanged( self, event ):
		event.Skip()

	def m_button_extr_textOnButtonClick( self, event ):
		event.Skip()

	def m_button_repl_textOnButtonClick( self, event ):
		event.Skip()

	def m_button_save_textOnButtonClick( self, event ):
		event.Skip()

	def m_button_revert_textOnButtonClick( self, event ):
		event.Skip()

	def OnButtonClickPatchRom( self, event ):
		event.Skip()

	def OnMenuSelectionOpen( self, event ):
		event.Skip()

	def OnMenuSelectionSave( self, event ):
		event.Skip()

	def OnMenuSelectionSaveAs( self, event ):
		event.Skip()

	def OnMenuBaseDataEdit( self, event ):
		event.Skip()

	def OnMenuPuzzleMultipleChoice( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )

	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )

	def m_splitter4OnIdle( self, event ):
		self.m_splitter4.SetSashPosition( 0 )
		self.m_splitter4.Unbind( wx.EVT_IDLE )


