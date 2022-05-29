from typing import BinaryIO

from formats.filesystem import FileFormat
from formats.binary import BinaryReader, BinaryWriter

from PIL import Image
import numpy as np
import ndspy.color
import wx


class BGImage(FileFormat):
    image: np.ndarray = np.zeros((256, 192), np.uint8)
    palette: np.ndarray = np.zeros((256, 4), np.uint8)

    _compressed_default = 2

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        with open("test.bin", "wb+") as f:
            f.write(rdr.read())
        rdr.seek(0)

        palette_length = rdr.read_uint32()
        for color_i in range(palette_length):
            self.palette[color_i] = ndspy.color.unpack255(rdr.read_uint16())
            if color_i:
                self.palette[color_i, 3] = 255

        n_tiles = rdr.read_uint32()
        tiles = np.frombuffer(rdr.read(n_tiles * 0x40), np.uint8).reshape((n_tiles, 8, 8))

        map_w = rdr.read_uint16()
        map_h = rdr.read_uint16()

        img_w = map_w * 8
        img_h = map_h * 8

        self.image = np.zeros((img_h, img_w), np.uint8)

        for map_y in range(map_h):
            for map_x in range(map_w):
                img_y = map_y * 8
                img_x = map_x * 8

                self.image[img_y:img_y + 8, img_x:img_x + 8] = tiles[rdr.read_uint16()]

    def write_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint32(256)
        for color_i in range(256):
            self.palette[color_i]: np.ndarray
            wtr.write_uint16(ndspy.color.pack255(*self.palette[color_i]))

        img_h, img_w = self.image.shape
        map_h, map_w = img_h // 8, img_w // 8

        tiles = np.asarray([self.image[y * 8:y * 8 + 8, x * 8:x * 8 + 8] for x in range(map_w) for y in range(map_h)])
        tiles: np.ndarray = np.unique(tiles, axis=0)
        wtr.write_uint32(len(tiles))
        wtr.write(tiles.tobytes())

        wtr.write_uint16(map_w)
        wtr.write_uint16(map_h)

        for y in range(map_h):
            for x in range(map_w):
                tile = self.image[y * 8:y * 8 + 8, x * 8:x * 8 + 8]

                tile_id = np.where(np.all(tile.reshape((64,)) == tiles.reshape(tiles.shape[0], 64), axis=1) == True)
                wtr.write_uint16(tile_id[0][0])

    def extract_image_wx_bitmap(self) -> wx.Bitmap:
        height, width = self.image.shape
        return wx.Bitmap.FromBufferRGBA(width, height, self.palette[self.image].astype(np.uint8))

    def extract_image_pil(self) -> Image.Image:
        return Image.fromarray(self.palette[self.image].astype(np.uint8), "RGBA")

    def import_image_pil(self, image: Image.Image):
        image = image.resize((256, 192)).convert("RGB").quantize(256, method=Image.MEDIANCUT)
        for color, i in image.palette.colors.items():
            self.palette[i][:3] = color[:3]
            self.palette[i][3] = 255
        self.image[:] = np.asarray(image, np.uint8)
