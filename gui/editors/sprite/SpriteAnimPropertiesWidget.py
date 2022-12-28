from PySide6 import QtWidgets
from gui.ui.sprite.AnimPropertiesWidget import AnimPropertiesWidgetUI, FrameOrders
from formats.graphics.ani import AniSprite, Animation


class AnimPropertiesWidget(AnimPropertiesWidgetUI):
    def __init__(self, frame_next_input_widgets, *args, **kwargs):
        super(AnimPropertiesWidget, self).__init__(*args, **kwargs)
        self.frame_next_input_widgets = frame_next_input_widgets
        self.sprite: AniSprite = None
        self.animation: Animation = None

    def show_next_frame_widgets(self):
        for widget in self.frame_next_input_widgets:
            widget: QtWidgets.QWidget
            widget.show()

    def hide_next_frame_widgets(self):
        for widget in self.frame_next_input_widgets:
            widget: QtWidgets.QWidget
            widget.hide()

    def set_animation(self, sprite: AniSprite, anim_idx: int):
        self.sprite = sprite
        self.animation = self.sprite.animations[anim_idx]
        self.child_x_input.setValue(self.animation.child_image_x)
        self.child_y_input.setValue(self.animation.child_image_y)
        self.child_anim_index.setValue(self.animation.child_image_animation_index)

        next_frame_indexes = [frame.next_frame_index for frame in self.animation.frames]
        frame_count = len(self.animation.frames)
        if next_frame_indexes == [(i + 1) % frame_count for i in range(frame_count)]:
            self.frame_order_input.setCurrentIndex(0)
        elif next_frame_indexes == [min(i + 1, frame_count - 1) for i in range(frame_count)]:
            self.frame_order_input.setCurrentIndex(1)
        else:
            self.frame_order_input.setCurrentIndex(2)
        self.frame_order_edit()

    def frame_order_edit(self, _index: int = 0):
        if self.frame_order_input.currentData() == FrameOrders.CUSTOM:
            self.show_next_frame_widgets()
            return
        self.hide_next_frame_widgets()
        frame_count = len(self.animation.frames)
        for i, frame in enumerate(self.animation.frames):
            if self.frame_order_input.currentData() == FrameOrders.LOOPING:
                frame.next_frame_index = (i + 1) % frame_count
            else:
                frame.next_frame_index = min(i + 1, frame_count - 1)

    def child_x_edit(self, value: int):
        self.animation.child_image_x = value

    def child_y_edit(self, value: int):
        self.animation.child_image_y = value

    def child_anim_edit(self, value: int):
        self.animation.child_image_animation_index = value
