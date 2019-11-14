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

		self.tree_imagefiles = wx.TreeCtrl( self.m_panel_leftside, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
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
		self.m_notebook1.AddPage( self.m_panel9, u"Images", False )
		self.m_panel10 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer27 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter3 = wx.SplitterWindow( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )

		self.m_panel11 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer28 = wx.BoxSizer( wx.VERTICAL )

		bSizer_leftside1 = wx.BoxSizer( wx.VERTICAL )

		self.tree_imagefiles1 = wx.TreeCtrl( self.m_panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		bSizer_leftside1.Add( self.tree_imagefiles1, 1, wx.EXPAND|wx.ALL, 5 )

		gSizer_buttonsleft1 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button_extract1 = wx.Button( self.m_panel11, wx.ID_ANY, u"Extract", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft1.Add( self.m_button_extract1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_replacefile1 = wx.Button( self.m_panel11, wx.ID_ANY, u"Replace", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft1.Add( self.m_button_replacefile1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_extractdecom1 = wx.Button( self.m_panel11, wx.ID_ANY, u"Extract Decompressed", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft1.Add( self.m_button_extractdecom1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button231 = wx.Button( self.m_panel11, wx.ID_ANY, u"Replace Decompressed", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_buttonsleft1.Add( self.m_button231, 0, wx.ALL|wx.EXPAND, 5 )


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
		self.m_notebook1.AddPage( self.m_panel10, u"Backgrounds", True )
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


		bSizer15.Add( bSizer19, 1, wx.ALIGN_BOTTOM|wx.EXPAND, 5 )


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
		self.m_button_extractdecom1.Bind( wx.EVT_BUTTON, self.OnButtonClickExtractDecomBG )
		self.m_button231.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceDecomBG )
		self.m_button_saveimage1.Bind( wx.EVT_BUTTON, self.OnButtonClickSaveImageBG )
		self.m_button_replaceimageandpalette1.Bind( wx.EVT_BUTTON, self.OnButtonClickReplaceImageBG )
		self.m_button26.Bind( wx.EVT_BUTTON, self.OnButtonClickPatchRom )
		self.Bind( wx.EVT_MENU, self.OnMenuSelectionOpen, id = self.m_menuItem_openfile.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelectionSave, id = self.m_menuItem_savefile.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelectionSaveAs, id = self.m_menuItem_savefileas.GetId() )

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

	def OnButtonClickExtractDecomBG( self, event ):
		event.Skip()

	def OnButtonClickReplaceDecomBG( self, event ):
		event.Skip()

	def OnButtonClickSaveImageBG( self, event ):
		event.Skip()

	def OnButtonClickReplaceImageBG( self, event ):
		event.Skip()

	def OnButtonClickPatchRom( self, event ):
		event.Skip()

	def OnMenuSelectionOpen( self, event ):
		event.Skip()

	def OnMenuSelectionSave( self, event ):
		event.Skip()

	def OnMenuSelectionSaveAs( self, event ):
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 0 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )

	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 0 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )


###########################################################################
## Class ImageEdit
###########################################################################

class ImageEdit ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit Image", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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

		self.m_staticText11 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"i.jpg", wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
		self.m_staticText11.Wrap( -1 )

		bSizer21.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticText7 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Colordepth: 4bit", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticText7.Wrap( -1 )

		bSizer21.Add( self.m_staticText7, 0, wx.ALL|wx.EXPAND, 5 )

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
		self.m_panel4 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
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

		self.m_textCtrl1 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER )
		self.m_textCtrl1.SetMaxLength( 24 )
		bSizer211.Add( self.m_textCtrl1, 1, wx.ALL, 5 )

		self.m_button241 = wx.Button( self.m_panel4, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer211.Add( self.m_button241, 0, wx.ALL, 5 )


		bSizer15.Add( bSizer211, 0, wx.EXPAND, 5 )

		self.m_panel10 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel10.SetBackgroundColour( wx.Colour( 230, 230, 230 ) )

		bSizer26 = wx.BoxSizer( wx.VERTICAL )

		self.m_previewImage1 = wx.StaticBitmap( self.m_panel10, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_previewImage1.SetMinSize( wx.Size( 258,194 ) )

		bSizer26.Add( self.m_previewImage1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

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

		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button36 = wx.Button( self.m_panel4, wx.ID_ANY, u"Add Animation", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.m_button36, 1, wx.ALL, 5 )

		self.m_button37 = wx.Button( self.m_panel4, wx.ID_ANY, u"Remove Animation", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.m_button37, 1, wx.ALL, 5 )


		bSizer15.Add( bSizer35, 0, wx.EXPAND, 5 )


		self.m_panel4.SetSizer( bSizer15 )
		self.m_panel4.Layout()
		bSizer15.Fit( self.m_panel4 )
		self.m_splitter2.SplitVertically( self.m_panel3, self.m_panel4, 0 )
		bSizer19.Add( self.m_splitter2, 1, wx.EXPAND, 5 )


		bSizer18.Add( bSizer19, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer18 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button8.Bind( wx.EVT_BUTTON, self.OnButtonClickPreviousImage )
		self.m_button9.Bind( wx.EVT_BUTTON, self.OnButtonClickNextImage )
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
		self.m_button241.Bind( wx.EVT_BUTTON, self.OnButtonClickSaveAnimationName )
		self.m_button811.Bind( wx.EVT_BUTTON, self.OnButtonClickPreviousAnimationFrame )
		self.m_button911.Bind( wx.EVT_BUTTON, self.OnButtonClickNextAnimationFrame )
		self.m_textCtrl11.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnterImgID )
		self.m_textCtrl13.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnterFrameDur )
		self.m_textCtrl131.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnterFrameID )
		self.m_button34.Bind( wx.EVT_BUTTON, self.OnButtonClickAddAFrame )
		self.m_button35.Bind( wx.EVT_BUTTON, self.OnButtonClickRemoveAFrame )
		self.m_button36.Bind( wx.EVT_BUTTON, self.OnButtonClickAddAnimation )
		self.m_button37.Bind( wx.EVT_BUTTON, self.OnButtonClickRemoveAnimation )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnButtonClickPreviousImage( self, event ):
		event.Skip()

	def OnButtonClickNextImage( self, event ):
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

	def OnButtonClickSaveAnimationName( self, event ):
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

	def OnButtonClickAddAnimation( self, event ):
		event.Skip()

	def OnButtonClickRemoveAnimation( self, event ):
		event.Skip()

	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 0 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )


