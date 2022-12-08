import wx
from formats.place import Place
from formats.filesystem import NintendoDSRom
from formats.graphics.bg import BGImage
from formats.graphics.ani import AniSprite


def scale_wx_bitmap(bitmap, width, height, scale_mode=wx.IMAGE_QUALITY_HIGH):
    # TODO: Optimize usage to store Image instead of bitmap
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, scale_mode)
    result = wx.Bitmap(image)
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
        self.Refresh(False)

    def on_paint(self, _event):

        dc = wx.BufferedPaintDC(self)
        w, h = ow, oh = self.GetSize()
        cx, cy = 0, 0
        if w / 256 > h / 192:  # Borders left and right
            w = int(h / 192 * 256)
            cx = (ow - w) // 2
        elif h / 192 > w / 256:  # Borders top and bottom
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
                              int(hintcoin.x * fw + cx), int(hintcoin.y * fh + cy))

        for plc_exit in self._place.exits:
            if plc_exit.width:
                ex_w, ex_h = self._ex_images[plc_exit.image_index].GetSize()
                dc.DrawBitmap(scale_wx_bitmap(self._ex_images[plc_exit.image_index], int(ex_w * fw), int(ex_h * fh)),
                              int(plc_exit.x * fw + cx), int(plc_exit.y * fh + cy))
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.GREEN_PEN)
                dc.DrawRectangle(int(plc_exit.x * fw + cx), int(plc_exit.y * fh + cy),
                                 int(plc_exit.width * fw), int(plc_exit.height * fh))

        for comment in self._place.comments:
            if comment.width:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(wx.BLUE_PEN)
                dc.DrawRectangle(int(comment.x * fw + cx), int(comment.y * fh + cy),
                                 int(comment.width * fw), int(comment.height * fh))

        for obj in self._place.objects:
            if obj.width:
                if obj.character_index:
                    ch_w, ch_h = self._ch_images[obj.character_index].GetSize()
                    dc.DrawBitmap(scale_wx_bitmap(self._ch_images[obj.character_index], int(ch_w * fw), int(ch_h * fh)),
                                  int(obj.x * fw + cx), int(obj.y * fh + cy))
                dc.SetPen(wx.RED_PEN)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.DrawRectangle(int(obj.x * fw + cx), int(obj.y * fh + cy), int(obj.width * fw), int(obj.height * fh))

    def on_size(self, _event):
        self.Refresh(False)
