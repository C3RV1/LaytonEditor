# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg

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
		self.m_menuItem4 = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Create Multiple Choice", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu2.Append( self.m_menuItem4 )

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
		self.Bind( wx.EVT_MENU, self.OnMenuPuzzleMultipleChoice, id = self.m_menuItem4.GetId() )

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

###########################################################################
## Class ImageEdit
###########################################################################


class ImageEdit ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit Image", pos = wx.DefaultPosition, size = wx.Size( 800,621 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer18 = wx.BoxSizer( wx.VERTICAL )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )

		self.m_panel3 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel3.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		self.m_previewImage = wx.StaticBitmap( self.m_panel3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_previewImage.SetMinSize( wx.Size( 258,194 ) )

		bSizer21.Add( self.m_previewImage, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button8 = wx.Button( self.m_panel3, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer11.Add( self.m_button8, 1, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"1/1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText5.Wrap( -1 )

		bSizer11.Add( self.m_staticText5, 1, wx.ALIGN_CENTER|wx.ALL, 10 )

		self.m_button9 = wx.Button( self.m_panel3, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer11.Add( self.m_button9, 1, wx.ALL, 5 )


		bSizer21.Add( bSizer11, 0, wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"ID: 0", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText9.Wrap( -1 )

		bSizer21.Add( self.m_staticText9, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText11 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"i.jpg", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText11.Wrap( -1 )

		bSizer21.Add( self.m_staticText11, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Colordepth: 4bit", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText7.Wrap( -1 )

		bSizer21.Add( self.m_staticText7, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer54 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText27 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Child Image:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		bSizer54.Add( self.m_staticText27, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_text_child_image = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer54.Add( self.m_text_child_image, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer21.Add( bSizer54, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button30 = wx.Button( self.m_panel3, wx.ID_ANY, u"Import (No Palette Change)", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button30, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button31 = wx.Button( self.m_panel3, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button31, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button23 = wx.Button( self.m_panel3, wx.ID_ANY, u"Import (Add To Palette)", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button23, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button24 = wx.Button( self.m_panel3, wx.ID_ANY, u"Swap Colordepth", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button24, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button32 = wx.Button( self.m_panel3, wx.ID_ANY, u"Add Image (No Palette Change)", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button32, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button33 = wx.Button( self.m_panel3, wx.ID_ANY, u"Remove Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button33, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button25 = wx.Button( self.m_panel3, wx.ID_ANY, u"Add Image (Add to Palette)", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button25, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_button26 = wx.Button( self.m_panel3, wx.ID_ANY, u"Export All Images", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button26, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer21.Add( gSizer2, 1, wx.EXPAND, 5 )


		self.m_panel3.SetSizer( bSizer21 )
		self.m_panel3.Layout()
		bSizer21.Fit( self.m_panel3 )
		self.m_splitter2.Initialize( self.m_panel3 )
		bSizer19.Add( self.m_splitter2, 1, wx.EXPAND, 5 )

		self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel4 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button81 = wx.Button( self.m_panel4, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer111.Add( self.m_button81, 1, wx.ALL, 5 )

		self.m_staticText51 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"1/1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText51.Wrap( -1 )

		bSizer111.Add( self.m_staticText51, 1, wx.ALL, 10 )

		self.m_button91 = wx.Button( self.m_panel4, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer111.Add( self.m_button91, 1, wx.ALL, 5 )


		bSizer15.Add( bSizer111, 0, wx.EXPAND, 5 )

		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrl1 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_PROCESS_ENTER )
		self.m_textCtrl1.SetMaxLength( 24 )
		bSizer211.Add( self.m_textCtrl1, 1, wx.ALL, 5 )


		bSizer15.Add( bSizer211, 0, wx.EXPAND, 5 )

		self.m_panel10 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel10.SetBackgroundColour( wx.Colour( 230, 230, 230 ) )

		bSizer26 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel_animation_preview = wx.Panel( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_animation_preview.SetMinSize( wx.Size( 258,194 ) )

		bSizer26.Add( self.m_panel_animation_preview, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button811 = wx.Button( self.m_panel10, wx.ID_ANY, u"<", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer1111.Add( self.m_button811, 1, wx.ALL, 5 )

		self.m_staticText511 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"1/1", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText511.Wrap( -1 )

		bSizer1111.Add( self.m_staticText511, 1, wx.ALL, 10 )

		self.m_button911 = wx.Button( self.m_panel10, wx.ID_ANY, u">", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer1111.Add( self.m_button911, 1, wx.ALL, 5 )


		bSizer26.Add( bSizer1111, 0, wx.EXPAND, 5 )

		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText24 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Image ID:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText24.Wrap( -1 )

		bSizer31.Add( self.m_staticText24, 1, wx.ALL, 5 )

		self.m_staticText26 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Frame Duration:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText26.Wrap( -1 )

		bSizer31.Add( self.m_staticText26, 1, wx.ALL, 5 )

		self.m_staticText241 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Frame ID:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText241.Wrap( -1 )

		bSizer31.Add( self.m_staticText241, 1, wx.ALL, 5 )


		bSizer26.Add( bSizer31, 0, wx.EXPAND, 5 )

		bSizer33 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrl11 = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer33.Add( self.m_textCtrl11, 1, wx.ALL, 5 )

		self.m_textCtrl13 = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer33.Add( self.m_textCtrl13, 1, wx.ALL, 5 )

		self.m_textCtrl131 = wx.TextCtrl( self.m_panel10, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer33.Add( self.m_textCtrl131, 1, wx.ALL, 5 )


		bSizer26.Add( bSizer33, 0, wx.EXPAND, 5 )

		bSizer34 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button34 = wx.Button( self.m_panel10, wx.ID_ANY, u"Add frame", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer34.Add( self.m_button34, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )

		self.m_button35 = wx.Button( self.m_panel10, wx.ID_ANY, u"Remove frame", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer34.Add( self.m_button35, 1, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer26.Add( bSizer34, 1, wx.EXPAND, 5 )


		self.m_panel10.SetSizer( bSizer26 )
		self.m_panel10.Layout()
		bSizer26.Fit( self.m_panel10 )
		bSizer15.Add( self.m_panel10, 1, wx.EXPAND |wx.ALL, 5 )

		bSizer311 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText242 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Child Image X:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText242.Wrap( -1 )

		bSizer311.Add( self.m_staticText242, 1, wx.ALL, 5 )

		self.m_staticText261 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Child Image Y:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText261.Wrap( -1 )

		bSizer311.Add( self.m_staticText261, 1, wx.ALL, 5 )

		self.m_staticText2411 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Child Image ID:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText2411.Wrap( -1 )

		bSizer311.Add( self.m_staticText2411, 1, wx.ALL, 5 )


		bSizer15.Add( bSizer311, 0, wx.EXPAND, 5 )

		bSizer331 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_panel19 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer331.Add( self.m_panel19, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_spin_child_img_x = wx.SpinCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.m_spin_child_img_x.SetMaxSize( wx.Size( 80,-1 ) )

		bSizer331.Add( self.m_spin_child_img_x, 1, wx.ALL, 5 )

		self.m_panel22 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer331.Add( self.m_panel22, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_spin_child_img_y = wx.SpinCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.m_spin_child_img_y.SetMaxSize( wx.Size( 80,-1 ) )

		bSizer331.Add( self.m_spin_child_img_y, 1, wx.ALL, 5 )

		self.m_panel20 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer331.Add( self.m_panel20, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_spin_child_img_id = wx.SpinCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.m_spin_child_img_id.SetMaxSize( wx.Size( 80,-1 ) )

		bSizer331.Add( self.m_spin_child_img_id, 0, wx.ALL, 5 )

		self.m_panel21 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer331.Add( self.m_panel21, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer15.Add( bSizer331, 0, wx.EXPAND, 5 )

		bSizer40 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox_draw_child_img = wx.CheckBox( self.m_panel4, wx.ID_ANY, u"Draw Child Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_draw_child_img.SetValue(True)
		bSizer40.Add( self.m_checkBox_draw_child_img, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_save_child_img_pos = wx.Button( self.m_panel4, wx.ID_ANY, u"save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer40.Add( self.m_button_save_child_img_pos, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer15.Add( bSizer40, 1, wx.EXPAND, 5 )

		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button36 = wx.Button( self.m_panel4, wx.ID_ANY, u"Add Animation", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.m_button36, 1, wx.ALL, 5 )

		self.m_button37 = wx.Button( self.m_panel4, wx.ID_ANY, u"Remove Animation", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.m_button37, 1, wx.ALL, 5 )


		bSizer15.Add( bSizer35, 0, wx.EXPAND, 5 )


		self.m_panel4.SetSizer( bSizer15 )
		self.m_panel4.Layout()
		bSizer15.Fit( self.m_panel4 )
		self.m_notebook2.AddPage( self.m_panel4, u"Animations", True )
		self.m_panel34 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer56 = wx.BoxSizer( wx.VERTICAL )

		self.m_propertyGrid_vars = pg.PropertyGrid(self.m_panel34, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		bSizer56.Add( self.m_propertyGrid_vars, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel34.SetSizer( bSizer56 )
		self.m_panel34.Layout()
		bSizer56.Fit( self.m_panel34 )
		self.m_notebook2.AddPage( self.m_panel34, u"Variables", False )

		bSizer19.Add( self.m_notebook2, 1, wx.EXPAND, 5 )


		bSizer18.Add( bSizer19, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer18 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button8.Bind( wx.EVT_BUTTON, self.OnButtonClickPreviousImage )
		self.m_button9.Bind( wx.EVT_BUTTON, self.OnButtonClickNextImage )
		self.m_text_child_image.Bind( wx.EVT_TEXT_ENTER, self.m_text_child_imageOnTextEnter )
		self.m_button30.Bind( wx.EVT_BUTTON, self.OnButtonClickReplNoPal )
		self.m_button31.Bind( wx.EVT_BUTTON, self.OnButtonClickExport )
		self.m_button23.Bind( wx.EVT_BUTTON, self.OnButtonClickReplAddPal )
		self.m_button24.Bind( wx.EVT_BUTTON, self.OnButtonClickSwapColorDepth )
		self.m_button32.Bind( wx.EVT_BUTTON, self.OnButtonClickAddImage )
		self.m_button33.Bind( wx.EVT_BUTTON, self.OnButtonClickRemoveImage )
		self.m_button25.Bind( wx.EVT_BUTTON, self.OnButtonClickAddImageAddPal )
		self.m_button26.Bind( wx.EVT_BUTTON, self.OnButtonClickExportAll )
		self.m_button81.Bind( wx.EVT_BUTTON, self.OnButtonClickPreviousAnimation )
		self.m_button91.Bind( wx.EVT_BUTTON, self.OnButtonClickNextAnimation )
		self.m_textCtrl1.Bind( wx.EVT_TEXT_ENTER, self.m_textCtrl1OnTextEnter )
		self.m_panel_animation_preview.Bind( wx.EVT_PAINT, self.m_panel_animation_previewOnPaint )
		self.m_panel_animation_preview.Bind( wx.EVT_SIZE, self.m_panel_animation_previewOnSize )
		self.m_button811.Bind( wx.EVT_BUTTON, self.OnButtonClickPreviousAnimationFrame )
		self.m_button911.Bind( wx.EVT_BUTTON, self.OnButtonClickNextAnimationFrame )
		self.m_textCtrl11.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnterImgID )
		self.m_textCtrl13.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnterFrameDur )
		self.m_textCtrl131.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnterFrameID )
		self.m_button34.Bind( wx.EVT_BUTTON, self.OnButtonClickAddAFrame )
		self.m_button35.Bind( wx.EVT_BUTTON, self.OnButtonClickRemoveAFrame )
		self.m_spin_child_img_x.Bind( wx.EVT_SPINCTRL, self.m_spin_child_img_xOnSpinCtrl )
		self.m_spin_child_img_y.Bind( wx.EVT_SPINCTRL, self.m_spin_child_img_yOnSpinCtrl )
		self.m_spin_child_img_id.Bind( wx.EVT_SPINCTRL, self.m_spin_child_img_idOnSpinCtrl )
		self.m_checkBox_draw_child_img.Bind( wx.EVT_CHECKBOX, self.m_checkBox_draw_child_imgOnCheckBox )
		self.m_button_save_child_img_pos.Bind( wx.EVT_BUTTON, self.m_button_save_child_img_posOnButtonClick )
		self.m_button36.Bind( wx.EVT_BUTTON, self.OnButtonClickAddAnimation )
		self.m_button37.Bind( wx.EVT_BUTTON, self.OnButtonClickRemoveAnimation )
		self.m_propertyGrid_vars.Bind( pg.EVT_PG_CHANGED, self.m_propertyGrid_varsOnPropertyGridChanged )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnButtonClickPreviousImage( self, event ):
		event.Skip()

	def OnButtonClickNextImage( self, event ):
		event.Skip()

	def m_text_child_imageOnTextEnter( self, event ):
		event.Skip()

	def OnButtonClickReplNoPal( self, event ):
		event.Skip()

	def OnButtonClickExport( self, event ):
		event.Skip()

	def OnButtonClickReplAddPal( self, event ):
		event.Skip()

	def OnButtonClickSwapColorDepth( self, event ):
		event.Skip()

	def OnButtonClickAddImage( self, event ):
		event.Skip()

	def OnButtonClickRemoveImage( self, event ):
		event.Skip()

	def OnButtonClickAddImageAddPal( self, event ):
		event.Skip()

	def OnButtonClickExportAll( self, event ):
		event.Skip()

	def OnButtonClickPreviousAnimation( self, event ):
		event.Skip()

	def OnButtonClickNextAnimation( self, event ):
		event.Skip()

	def m_textCtrl1OnTextEnter( self, event ):
		event.Skip()

	def m_panel_animation_previewOnPaint( self, event ):
		event.Skip()

	def m_panel_animation_previewOnSize( self, event ):
		event.Skip()

	def OnButtonClickPreviousAnimationFrame( self, event ):
		event.Skip()

	def OnButtonClickNextAnimationFrame( self, event ):
		event.Skip()

	def OnTextEnterImgID( self, event ):
		event.Skip()

	def OnTextEnterFrameDur( self, event ):
		event.Skip()

	def OnTextEnterFrameID( self, event ):
		event.Skip()

	def OnButtonClickAddAFrame( self, event ):
		event.Skip()

	def OnButtonClickRemoveAFrame( self, event ):
		event.Skip()

	def m_spin_child_img_xOnSpinCtrl( self, event ):
		event.Skip()

	def m_spin_child_img_yOnSpinCtrl( self, event ):
		event.Skip()

	def m_spin_child_img_idOnSpinCtrl( self, event ):
		event.Skip()

	def m_checkBox_draw_child_imgOnCheckBox( self, event ):
		event.Skip()

	def m_button_save_child_img_posOnButtonClick( self, event ):
		event.Skip()

	def OnButtonClickAddAnimation( self, event ):
		event.Skip()

	def OnButtonClickRemoveAnimation( self, event ):
		event.Skip()

	def m_propertyGrid_varsOnPropertyGridChanged( self, event ):
		event.Skip()

	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 0 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )

###########################################################################
## Class PuzzleMultipleChoice
###########################################################################

class PuzzleMultipleChoice ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Create Multiple Choice Puzzle", pos = wx.DefaultPosition, size = wx.Size( 794,509 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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

		self.save_puzzle_button = wx.Button( self.m_panel25, wx.ID_ANY, u"Save Puzzle", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer42.Add( self.save_puzzle_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.m_panel25.SetSizer( bSizer42 )
		self.m_panel25.Layout()
		bSizer42.Fit( self.m_panel25 )
		bSizer41.Add( self.m_panel25, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel26 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel26.SetBackgroundColour( wx.Colour( 224, 224, 224 ) )

		bSizer47 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook3 = wx.Notebook( self.m_panel26, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel30 = wx.Panel( self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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
		self.m_notebook3.AddPage( self.m_panel30, u"Texts", True )
		self.m_panel31 = wx.Panel( self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer51 = wx.BoxSizer( wx.VERTICAL )

		self.m_treeCtrl4 = wx.TreeCtrl( self.m_panel31, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		bSizer51.Add( self.m_treeCtrl4, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer52 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText41 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"X:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText41.Wrap( -1 )

		bSizer52.Add( self.m_staticText41, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrl20 = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer52.Add( self.m_textCtrl20, 1, wx.ALL, 5 )

		self.m_staticText42 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Y:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText42.Wrap( -1 )

		bSizer52.Add( self.m_staticText42, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrl21 = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer52.Add( self.m_textCtrl21, 1, wx.ALL, 5 )


		bSizer51.Add( bSizer52, 0, wx.ALIGN_CENTER, 5 )

		bSizer53 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText43 = wx.StaticText( self.m_panel31, wx.ID_ANY, u"FreeButton Sprite:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		self.m_staticText43.Wrap( -1 )

		bSizer53.Add( self.m_staticText43, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrl22 = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer53.Add( self.m_textCtrl22, 0, wx.ALL, 5 )


		bSizer51.Add( bSizer53, 0, wx.ALIGN_CENTER, 5 )

		bSizer54 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox2 = wx.CheckBox( self.m_panel31, wx.ID_ANY, u"Is Solution", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		bSizer54.Add( self.m_checkBox2, 0, wx.ALL, 5 )

		self.anim_unknown_label = wx.StaticText( self.m_panel31, wx.ID_ANY, u"Animation unknown field:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.anim_unknown_label.Wrap( -1 )

		bSizer54.Add( self.anim_unknown_label, 0, wx.ALL, 5 )

		self.anim_unknown_input = wx.TextCtrl( self.m_panel31, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer54.Add( self.anim_unknown_input, 0, wx.ALL, 5 )


		bSizer51.Add( bSizer54, 0, wx.ALIGN_CENTER, 5 )


		self.m_panel31.SetSizer( bSizer51 )
		self.m_panel31.Layout()
		bSizer51.Fit( self.m_panel31 )
		self.m_notebook3.AddPage( self.m_panel31, u"Objects", False )

		bSizer47.Add( self.m_notebook3, 1, wx.EXPAND |wx.ALL, 5 )


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

