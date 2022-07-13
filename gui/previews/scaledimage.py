import wx
import time


def scale_wx_bitmap(bitmap: wx.Bitmap, width, height, nearest=False):
    image: wx.Image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_NEAREST if nearest else wx.IMAGE_QUALITY_HIGH)
    return image.ConvertToBitmap()


class ScaledImage(wx.Panel):
    _bitmap = None
    _nearest = True
    _last_click = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)
        self.Show(True)

    def load_bitmap(self, bitmap: wx.Bitmap):
        self._bitmap = bitmap
        self.Refresh()

    def clear_bitmap(self):
        self._bitmap = None
        self.Refresh()

    def on_paint(self, _event):

        dc = wx.BufferedPaintDC(self)
        w, h = ow, oh = self.GetSize()

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.GREEN_BRUSH)
        dc.DrawRectangle(0, 0, ow, oh)

        if not self._bitmap:
            return

        bw, bh = self._bitmap.GetSize()
        cx, cy = 0, 0
        if w / bw > h / bh:
            w = int(h / bh * bw)
            cx = (ow - w) // 2
        elif h / bh > w / bw:
            h = int(w / bw * bh)
            cy = (oh - h) // 2

        if not w:
            return

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.GREEN_BRUSH)
        dc.DrawRectangle(0, 0, ow, oh)

        dc.DrawBitmap(scale_wx_bitmap(self._bitmap, w, h, self._nearest), cx, cy)

    def on_size(self, _event):
        self.Refresh()

    def on_mouse(self, event: wx.MouseEvent):
        if event.LeftDClick() or event.LeftDown():
            clicked_time = time.time()
            if clicked_time - self._last_click < 0.5:
                self._nearest = not self._nearest
                self.Refresh()
                self._last_click = 0
            else:
                self._last_click = clicked_time
