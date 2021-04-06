import wx
from formats.place import Place
from formats.filesystem import NintendoDSRom, PlzArchive
from formats.graphics.bg import BGImage
from formats.graphics.ani import AniSprite


def scale_wx_bitmap(bitmap, width, height, scale_mode=wx.IMAGE_QUALITY_HIGH):
    # TODO: Optimize usage to store Image instead of bitmap
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, scale_mode)
    result = wx.BitmapFromImage(image)
    return result


class PlaceViewer(wx.Panel):
    _place = None
    _bg_image = None
    _hc_image = None
    _ex_images = []
    _ch_images = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetMinSize((256, 192))
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Show(True)

    def load_place(self, place: Place, rom: NintendoDSRom):
        self._place = place
        self._bg_image = BGImage(f"data_lt2/bg/map/main{place.background_image_index}.arc", rom=rom) \
            .extract_image_wx_bitmap()
        self._hc_image = AniSprite("data_lt2/ani/map/hintcoin.arc", rom=rom).extract_image_wx_bitmap(0)
        self._ex_images = [AniSprite(f"data_lt2/ani/map/exit_{i}.arc", rom=rom).extract_image_wx_bitmap(0)
                           for i in range(8)]
        for obj in place.objects:
            if obj.character_index:
                self._ch_images[obj.character_index] = \
                    AniSprite(f"data_lt2/ani/eventobj/obj_{obj.character_index}.arc",
                              rom=rom).extract_image_wx_bitmap(0)
        self.Refresh()

    def on_paint(self, _event):
        dc = wx.BufferedPaintDC(self)
        w, h = ow, oh = self.GetSize()
        cx, cy = 0, 0
        if w / 256 > h / 192:
            w = int(h / 192 * 256)
            cx = (ow - w) // 2
        elif h / 192 > w / 256:
            h = int(w / 256 * 192)
            cy = (oh - h) // 2
        fw, fh = w / 256, h / 192

        if (not w) or (not h):
            return

        dc.Clear()  # TODO: Optimize with only clearing sides.
        if not self._place:
            return

        dc.DrawBitmap(scale_wx_bitmap(self._bg_image, w, h), cx, cy)

        for hintcoin in self._place.hintcoins:
            if hintcoin.index:
                hc_w, hc_h = self._hc_image.GetSize()
                dc.DrawBitmap(scale_wx_bitmap(self._hc_image, int(hc_w * fw), int(hc_h * fh)),
                              hintcoin.x * fw + cx, hintcoin.y * fh + cy)

        for plc_exit in self._place.exits:
            if plc_exit.width:
                ex_w, ex_h = self._ex_images[plc_exit.image_index].GetSize()
                dc.DrawBitmap(scale_wx_bitmap(self._ex_images[plc_exit.image_index], ex_w * fw, ex_h * fh),
                              plc_exit.x * fw + cx, plc_exit.y * fh + cy)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.GREEN_PEN)
                dc.DrawRectangle(plc_exit.x * fw + cx, plc_exit.y * fh + cy, plc_exit.width * fw, plc_exit.height * fh)

        for comment in self._place.comments:
            if comment.width:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.BLUE_PEN)
                dc.DrawRectangle(comment.x * fw + cx, comment.y * fh + cy, comment.width * fw, comment.height * fh)

        for obj in self._place.objects:
            if obj.width:
                if obj.character_index:
                    ch_w, ch_h = self._ch_images[obj.character_index].GetSize()
                    dc.DrawBitmap(scale_wx_bitmap(self._ch_images[obj.character_index], ch_w * fw, ch_h * fh),
                                  obj.x * fw + cx, obj.y * fh + cy)
                dc.SetPen(wx.RED_PEN)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.DrawRectangle(obj.x * fw + cx, obj.y * fh + cy, obj.width * fw, obj.height * fh)

    def on_size(self, _event):
        self.Refresh()
