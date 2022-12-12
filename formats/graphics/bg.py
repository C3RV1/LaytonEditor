import logging
from typing import BinaryIO

from formats.filesystem import FileFormat
from formats.binary import BinaryReader, BinaryWriter

from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6 import QtGui
import numpy as np
import ndspy.color


class BGImage(FileFormat):
    image: np.ndarray = np.zeros((256, 192), np.uint8)
    palette: np.ndarray = np.zeros((256, 4), np.uint8)

    _compressed_default = 2

    def read_stream(self, stream: BinaryIO):
        if isinstance(stream, BinaryReader):
            rdr = stream
        else:
            rdr = BinaryReader(stream)
        rdr.seek(0)

        palette_length = rdr.read_uint32()
        self.palette = np.zeros((palette_length, 4), np.uint8)
        for color_i in range(palette_length):
            self.palette[color_i] = ndspy.color.unpack255(rdr.read_uint16())
            if color_i:
                self.palette[color_i, 3] = 255

        n_tiles = rdr.read_uint32()
        # Read tiles and assemble image
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

    def write_stream(self, stream):
        if isinstance(stream, BinaryWriter):
            wtr = stream
        else:
            wtr = BinaryWriter(stream)

        wtr.write_uint32(len(self.palette))
        for color_i in range(len(self.palette)):
            self.palette[color_i]: np.ndarray
            self.palette[color_i, 3] = 0
            wtr.write_uint16(ndspy.color.pack255(*self.palette[color_i]))
            self.palette[color_i, 3] = 255

        img_h, img_w = self.image.shape
        map_h, map_w = img_h // 8, img_w // 8

        # Get all 8x8 unique tiles
        tiles = np.asarray([self.image[y * 8:y * 8 + 8, x * 8:x * 8 + 8] for y in range(map_h) for x in range(map_w)])
        _, idx = np.unique(tiles, return_index=True, axis=0)
        tiles = tiles[np.sort(idx)]
        wtr.write_uint32(len(tiles))
        wtr.write(tiles.tobytes())

        wtr.write_uint16(map_w)
        wtr.write_uint16(map_h)

        for y in range(map_h):
            for x in range(map_w):
                # Get tile and write the index of the tile
                tile = self.image[y * 8:y * 8 + 8, x * 8:x * 8 + 8]

                # Get tile id (numpy magic lol)
                tile_id = np.where(np.all(tile.reshape((64,)) == tiles.reshape(tiles.shape[0], 64), axis=1) == True)
                wtr.write_uint16(tile_id[0][0])

    def extract_image_qt(self) -> QtGui.QPixmap:
        image = self.extract_image_pil()
        width, height = image.size
        image = image.resize((width * 2, height * 2), resample=Image.Resampling.NEAREST)
        qim = ImageQt(image)
        return QtGui.QPixmap.fromImage(qim)

    def extract_image_pil(self) -> Image.Image:
        return Image.fromarray(self.palette[self.image].astype(np.uint8), "RGBA")

    def import_image_pil(self, image: Image.Image):
        # Find out why palette breaks close to 256 colors (keeping at 200 colors for consistency w/ the game)
        # 199 colors + 1 transparent
        image = image.resize((256, 192)).convert("RGB").quantize(199, method=Image.MEDIANCUT)
        self.palette = np.zeros((min(len(image.palette.colors.keys()), 199) + 1, 4), np.uint8)
        logging.info(f"Replacing background {self._last_filename} with image of size {image.size} and palette of "
                     f"length {len(self.palette)}")
        self.palette[0] = (0, 255, 0, 0)
        for color, i in image.palette.colors.items():
            if i >= 200:
                break
            self.palette[i + 1][:3] = color[:3]
            self.palette[i + 1][3] = 255
        self.image[:] = np.asarray(image, np.uint8) + 1  # Add one to account for transparent color
