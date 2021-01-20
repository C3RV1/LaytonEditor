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


