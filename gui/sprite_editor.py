from formats.graphics.ani import AniSprite
from gui import generated


class SpriteEditor(generated.SpriteEditor):
    _sprite: AniSprite = None

    def load_sprite(self, sprite: AniSprite):
        self._sprite = sprite
        self.ase_images_view.load_bitmap(sprite.extract_image_wx_bitmap(0))
        self.ase_images_slider.SetMax(len(sprite.images) - 1)
        self.ase_images_slider.SetValue(0)
        for var in self._sprite.variables:
            self.ase_variables_dataview.AppendItem([var, *(str(x) for x in self._sprite.variables[var])])
        self.ase_animations_list.SetItems([ani.name for ani in self._sprite.animations])
        self.ase_frame_slider.SetMax(0)

    def ase_images_slider_changed(self, event):
        self.ase_images_view.load_bitmap(self._sprite.extract_image_wx_bitmap(self.ase_images_slider.GetValue()))

    def ase_animations_list_selected(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetSelection()]
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
        animation = self._sprite.animations[self.ase_animations_list.GetSelection()]
        frame_index = self.ase_frame_slider.GetValue()
        bitmap = self._sprite.extract_image_wx_bitmap(animation.frames[frame_index].image_index)
        self.ase_frame_view.load_bitmap(bitmap)
        self.ase_prop_image_index_spin.SetValue(animation.frames[frame_index].image_index)
        self.ase_prop_frame_index_spin.SetValue(animation.frames[frame_index].index)
        self.ase_prop_frame_duration_spin.SetValue(animation.frames[frame_index].duration)

    def ase_prop_frame_index_spin_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetSelection()]
        frame_index = self.ase_frame_slider.GetValue()
        animation.frames[frame_index].index = self.ase_prop_frame_index_spin.GetValue()

    def ase_prop_image_index_spin_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetSelection()]
        frame_index = self.ase_frame_slider.GetValue()
        animation.frames[frame_index].image_index = self.ase_prop_image_index_spin.GetValue()

        bitmap = self._sprite.extract_image_wx_bitmap(animation.frames[frame_index].image_index)
        self.ase_frame_view.load_bitmap(bitmap)

    def ase_prop_frame_duration_spin_changed(self, event):
        animation = self._sprite.animations[self.ase_animations_list.GetSelection()]
        frame_index = self.ase_frame_slider.GetValue()
        animation.frames[frame_index].duration = self.ase_prop_frame_duration_spin.GetValue()

    def enter(self):
        pass

    def exit(self):
        self._sprite.save()
