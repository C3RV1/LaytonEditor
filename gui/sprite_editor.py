import wx
import wx.dataview

from formats.graphics.ani import AniSprite, Animation
from gui import generated


class SpriteEditor(generated.SpriteEditor):
    _sprite: AniSprite = None
    ase_menu: wx.Menu

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        maineditor = self.GetGrandParent()
        self.ase_menu = wx.Menu()

        def add_menu_item(menu, title, handler):
            ase_menu_item = wx.MenuItem(menu, wx.ID_ANY, title)
            menu.Append(ase_menu_item)
            maineditor.Bind(wx.EVT_MENU, handler, id=ase_menu_item.GetId())

        add_menu_item(self.ase_menu, "Add Animation", self.ase_add_animation_clicked)
        add_menu_item(self.ase_menu, "Remove Animation", self.ase_remove_animation_clicked)
        # self.ase_menu.AppendSeparator()
        # add_menu_item(self.ase_menu, "Add Frame", self.ase_add_frame_clicked)
        # add_menu_item(self.ase_menu, "Insert Frame", self.ase_insert_frame_clicked)
        # add_menu_item(self.ase_menu, "Remove Frame", self.ase_remove_frame_clicked)
        # self.ase_menu.AppendSeparator()
        # add_menu_item(self.ase_menu, "Add Image", self.ase_add_image_clicked)
        # add_menu_item(self.ase_menu, "Remove Image", self.ase_remove_image_clicked)
        # add_menu_item(self.ase_menu, "Import Image", self.ase_import_image_clicked)
        # add_menu_item(self.ase_menu, "Export Image", self.ase_export_image_clicked)

    def load_sprite(self, sprite: AniSprite):
        self._sprite = sprite
        self.ase_images_view.load_bitmap(sprite.extract_image_wx_bitmap(0))
        self.ase_images_slider.SetMax(len(sprite.images) - 1)
        self.ase_images_slider.SetValue(0)
        for var in self._sprite.variables:
            self.ase_variables_dataview.AppendItem([var, *(str(x) for x in self._sprite.variables[var])])
        for animation in self._sprite.animations:
            self.ase_animations_list.Append((animation.name,))
        self.ase_frame_slider.SetMax(0)

    def ase_images_slider_changed(self, event):
        self.ase_images_view.load_bitmap(self._sprite.extract_image_wx_bitmap(self.ase_images_slider.GetValue()))

    def ase_animations_list_selected(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetFirstSelected()]
        if animation.frames:
            self.ase_frame_slider.SetValue(0)
            self.ase_frame_slider.SetMax(len(animation.frames) - 1)
            self.ase_frame_view.load_bitmap(self._sprite.extract_image_wx_bitmap(animation.frames[0].image_index))
            self.ase_prop_image_index_spin.SetValue(animation.frames[0].image_index)
            self.ase_prop_frame_index_spin.SetValue(animation.frames[0].index)
            self.ase_prop_frame_duration_spin.SetValue(animation.frames[0].duration)
        else:
            self.ase_frame_slider.SetValue(0)
            self.ase_frame_slider.SetMax(0)
            self.ase_frame_view.clear_bitmap()
            self.ase_prop_image_index_spin.SetValue(0)
            self.ase_prop_frame_index_spin.SetValue(0)
            self.ase_prop_frame_duration_spin.SetValue(0)
        # TODO: Child Sprites

    def ase_frame_slider_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetFirstSelected()]
        frame_index = self.ase_frame_slider.GetValue()
        bitmap = self._sprite.extract_image_wx_bitmap(animation.frames[frame_index].image_index)
        self.ase_frame_view.load_bitmap(bitmap)
        self.ase_prop_image_index_spin.SetValue(animation.frames[frame_index].image_index)
        self.ase_prop_frame_index_spin.SetValue(animation.frames[frame_index].index)
        self.ase_prop_frame_duration_spin.SetValue(animation.frames[frame_index].duration)

    def ase_prop_frame_index_spin_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetFirstSelected()]
        frame_index = self.ase_frame_slider.GetValue()
        animation.frames[frame_index].index = self.ase_prop_frame_index_spin.GetValue()

    def ase_prop_image_index_spin_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetFirstSelected()]
        frame_index = self.ase_frame_slider.GetValue()
        animation.frames[frame_index].image_index = self.ase_prop_image_index_spin.GetValue()

        bitmap = self._sprite.extract_image_wx_bitmap(animation.frames[frame_index].image_index)
        self.ase_frame_view.load_bitmap(bitmap)

    def ase_prop_frame_duration_spin_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetFirstSelected()]
        frame_index = self.ase_frame_slider.GetValue()
        animation.frames[frame_index].duration = self.ase_prop_frame_duration_spin.GetValue()

    def ase_animations_list_label_edit(self, event: wx.ListEvent):
        self._sprite.animations[event.GetSelection()].name = event.GetText()

    def ase_add_animation_clicked(self, _event):
        self._sprite.animations.append(Animation("New Animation"))
        self.ase_animations_list.Append(("New Animation",))

    def ase_remove_animation_clicked(self, _event):
        index = self.ase_animations_list.GetFirstSelected()
        self.ase_animations_list.DeleteItem(index)
        del self._sprite.animations[index]

    def ase_add_frame_clicked(self, _event):
        pass

    def ase_insert_frame_clicked(self, _event):
        pass

    def ase_remove_frame_clicked(self, _event):
        pass

    def ase_add_image_clicked(self, _event):
        pass

    def ase_remove_image_clicked(self, _event):
        pass

    def ase_import_image_clicked(self, _event):
        pass

    def ase_export_image_clicked(self, _event):
        pass

    def ase_variables_dataview_edited(self, event: wx.dataview.DataViewEvent):
        col, row = event.GetColumn(), self.ase_variables_dataview.GetSelectedRow()
        if col == 0:
            self._sprite.variables = {(event.GetValue() if i == row else k): v
                                      for i, (k, v) in enumerate(self._sprite.variables.items())}
        else:
            key = list(self._sprite.variables.keys())[col]
            self._sprite.variables[key][col - 1] = int(event.GetValue(), 0)

    def enter(self):
        self.GetGrandParent().add_menu(self.ase_menu, "Sprite")

    def exit(self):
        self.GetGrandParent().remove_menu("Sprite")
        self._sprite.save()
